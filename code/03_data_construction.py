"""
03_data_construction.py
Phase 3a: Construct analysis panel for nested logit demand estimation
and event study analysis.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output"

# ============================================================
# 1. LOAD RAW DATA
# ============================================================
print("Loading data...")
df = pd.read_csv(DATA / "master" / "usage_daily.csv")
df['date'] = pd.to_datetime(df['date'])

# Load model metadata (JSON has pricing)
with open(DATA / "master" / "models_enriched_latest.json") as f:
    meta_raw = json.load(f)
models_list = meta_raw.get('models', [])

# ============================================================
# 2. EXTRACT MODEL CHARACTERISTICS FROM METADATA
# ============================================================
print("Extracting model characteristics...")
model_chars = []
for m in models_list:
    permaslug = m.get('permaslug', '')

    # Pricing from endpoint or v1
    price_prompt = None
    price_completion = None

    # Try endpoint pricing first
    ep = m.get('endpoint', {})
    if isinstance(ep, dict):
        pricing = ep.get('pricing', {})
        if isinstance(pricing, dict):
            price_prompt = pricing.get('prompt')
            price_completion = pricing.get('completion')

    # Fallback to v1 pricing
    if price_prompt is None:
        v1 = m.get('v1', {})
        if isinstance(v1, dict):
            v1_pricing = v1.get('pricing', {})
            if isinstance(v1_pricing, dict):
                price_prompt = v1_pricing.get('prompt')
                price_completion = v1_pricing.get('completion')

    # Convert to float
    try:
        price_prompt = float(price_prompt) if price_prompt else None
    except (ValueError, TypeError):
        price_prompt = None
    try:
        price_completion = float(price_completion) if price_completion else None
    except (ValueError, TypeError):
        price_completion = None

    # Is free model?
    is_free = ':free' in permaslug or (price_prompt == 0 and price_completion == 0)

    # Supports reasoning
    supports_reasoning = m.get('supports_reasoning', False) or False

    # Context length
    ctx = m.get('context_length', None)

    # Input modalities
    input_mod = m.get('input_modalities', [])
    supports_image = 'image' in input_mod if isinstance(input_mod, list) else False

    # Author
    author = m.get('author', permaslug.split('/')[0] if '/' in permaslug else '')

    # Created at
    created = m.get('created_at', None)

    # Features / tool support
    ep_model = ep.get('model', {}) if isinstance(ep, dict) else {}
    supported_params = ep.get('supported_parameters', []) if isinstance(ep, dict) else []
    supports_tools = 'tools' in supported_params if isinstance(supported_params, list) else False

    model_chars.append({
        'model_permaslug': permaslug,
        'author': author,
        'context_length': ctx,
        'supports_reasoning': supports_reasoning,
        'supports_tools': supports_tools,
        'supports_image': supports_image,
        'price_prompt': price_prompt,
        'price_completion': price_completion,
        'is_free': is_free,
        'created_at': created,
    })

chars_df = pd.DataFrame(model_chars)
chars_df['created_at'] = pd.to_datetime(chars_df['created_at'], errors='coerce')

# Compute blended price (50/50 weight prompt/completion as approximation)
chars_df['price_blended'] = (chars_df['price_prompt'].fillna(0) + chars_df['price_completion'].fillna(0)) / 2
chars_df['log_price'] = np.log(chars_df['price_blended'].replace(0, np.nan))
chars_df['log_context'] = np.log(chars_df['context_length'].replace(0, np.nan))

print(f"Model metadata: {len(chars_df)} models, {chars_df['price_prompt'].notna().sum()} with pricing")

# ============================================================
# 3. MERGE AND CLEAN PANEL
# ============================================================
print("Merging panel...")

# Exclude same-day data
latest_date = df['date'].max()
df = df[df['date'] < latest_date]

# Merge characteristics
panel = df.merge(chars_df, on='model_permaslug', how='left')

# Compute derived variables
panel['total_tokens'] = panel['total_prompt_tokens'] + panel['total_completion_tokens']
panel['has_reasoning_usage'] = panel['total_native_tokens_reasoning'] > 0
panel['has_tool_usage'] = panel['total_tool_calls'] > 0

# ============================================================
# 4. COMPUTE MARKET SIZE AND SHARES
# ============================================================
print("Computing market shares...")

# Daily total (inside goods)
daily_total = panel.groupby('date')['count'].sum().reset_index()
daily_total.columns = ['date', 'total_inside']

# For outside option: use top_models weekly data to estimate total market
# Load weekly data for a rough market size proxy
try:
    with open(DATA / "rankings" / "latest" / "top_models.json") as f:
        tm = json.load(f)
except FileNotFoundError:
    with open(DATA / "rankings" / "20260325" / "top_models.json") as f:
        tm = json.load(f)

# Use the latest few weeks to estimate market size multiplier
# Total tokens from rankings / total tokens from our panel → multiplier
# For simplicity, use a fixed outside option = 20% of market (conservative)
# This follows standard practice in demand estimation when outside option is uncertain

panel = panel.merge(daily_total, on='date')
# Market size M_t = total_inside / 0.8 (assuming 80% inside share)
panel['market_size'] = panel['total_inside'] / 0.80
panel['outside_count'] = panel['market_size'] - panel['total_inside']

# Model share
panel['share'] = panel['count'] / panel['market_size']
panel['share'] = panel['share'].clip(lower=1e-10)  # avoid log(0)

# Outside share
panel['s0'] = panel['outside_count'] / panel['market_size']
panel['s0'] = panel['s0'].clip(lower=1e-10)

# Within-firm share
firm_daily = panel.groupby(['date', 'author_x' if 'author_x' in panel.columns else 'author'])['count'].sum().reset_index()
author_col = 'author_x' if 'author_x' in panel.columns else 'author'
firm_daily.columns = ['date', 'firm', 'firm_total']
panel['firm'] = panel['model_permaslug'].str.split('/').str[0]
panel = panel.merge(firm_daily.rename(columns={'firm': 'firm_merge'}),
                    left_on=['date', 'firm'], right_on=['date', 'firm_merge'], how='left')
panel['within_firm_share'] = panel['count'] / panel['firm_total'].replace(0, np.nan)
panel['within_firm_share'] = panel['within_firm_share'].clip(lower=1e-10)

# Berry inversion LHS
panel['lhs_berry'] = np.log(panel['share']) - np.log(panel['s0'])
panel['log_within_share'] = np.log(panel['within_firm_share'])

# ============================================================
# 5. IDENTIFY ENTRY EVENTS
# ============================================================
print("Identifying entry events...")

# First appearance of each model
first_seen = panel.groupby('model_permaslug')['date'].min().reset_index()
first_seen.columns = ['model_permaslug', 'entry_date']

panel = panel.merge(first_seen, on='model_permaslug')

# Model age (days since entry)
panel['model_age'] = (panel['date'] - panel['entry_date']).dt.days
panel['model_age_sq'] = panel['model_age'] ** 2

# For each model-day, count same-firm entries in [t-7, t] and rival entries
entry_dates = first_seen.copy()
entry_dates['firm_entry'] = entry_dates['model_permaslug'].str.split('/').str[0]

# Create entry event indicators
def count_entries_in_window(row, entry_df, window_start, window_end, same_firm=True):
    """Count model entries for same firm or rivals in a window."""
    mask = (entry_df['entry_date'] >= row['date'] + pd.Timedelta(days=window_start)) & \
           (entry_df['entry_date'] <= row['date'] + pd.Timedelta(days=window_end))
    if same_firm:
        mask = mask & (entry_df['firm_entry'] == row['firm'])
        # Exclude the model itself
        mask = mask & (entry_df['model_permaslug'] != row['model_permaslug'])
    else:
        mask = mask & (entry_df['firm_entry'] != row['firm'])
    return mask.sum()

# For efficiency, precompute entry counts per firm per day
print("Computing entry event indicators (this may take a moment)...")

# Create a date × firm entry count table
date_range = pd.date_range(panel['date'].min(), panel['date'].max())
entry_by_firm_date = entry_dates.groupby(['firm_entry', 'entry_date']).size().reset_index(name='n_entries')

# For each day, count entries in windows
all_dates = panel[['date']].drop_duplicates()
all_firms = panel[['firm']].drop_duplicates()

# Simpler approach: for each date, count entries in windows
entry_dates_set = entry_dates[['entry_date', 'firm_entry', 'model_permaslug']].copy()

# Pre-compute for each date: same-firm entries [0,7] and [8,30], rival entries [0,7] and [8,30]
date_firm_entries = {}
for _, row in entry_dates_set.iterrows():
    d = row['entry_date']
    f = row['firm_entry']
    if d not in date_firm_entries:
        date_firm_entries[d] = {}
    if f not in date_firm_entries[d]:
        date_firm_entries[d][f] = 0
    date_firm_entries[d][f] += 1

def compute_entry_counts(dates, firms, entry_dates_dict):
    """Vectorized entry count computation."""
    same_0_7 = np.zeros(len(dates))
    same_8_30 = np.zeros(len(dates))
    rival_0_7 = np.zeros(len(dates))
    rival_8_30 = np.zeros(len(dates))

    for i, (d, f) in enumerate(zip(dates, firms)):
        for offset in range(0, 8):
            check_date = d - pd.Timedelta(days=offset)
            if check_date in entry_dates_dict:
                for firm, cnt in entry_dates_dict[check_date].items():
                    if firm == f:
                        same_0_7[i] += cnt
                    else:
                        rival_0_7[i] += cnt
        for offset in range(8, 31):
            check_date = d - pd.Timedelta(days=offset)
            if check_date in entry_dates_dict:
                for firm, cnt in entry_dates_dict[check_date].items():
                    if firm == f:
                        same_8_30[i] += cnt
                    else:
                        rival_8_30[i] += cnt

    return same_0_7, same_8_30, rival_0_7, rival_8_30

# Use vectorized approach on unique date-firm combinations
unique_df = panel[['date', 'firm']].drop_duplicates().reset_index(drop=True)
s07, s830, r07, r830 = compute_entry_counts(
    unique_df['date'].values, unique_df['firm'].values, date_firm_entries
)
unique_df['same_firm_entry_0_7'] = s07
unique_df['same_firm_entry_8_30'] = s830
unique_df['rival_entry_0_7'] = r07
unique_df['rival_entry_8_30'] = r830

panel = panel.merge(unique_df, on=['date', 'firm'], how='left')

# ============================================================
# 6. INSTRUMENTS FOR NESTED LOGIT
# ============================================================
print("Computing instruments...")

# BLP-style instruments: count of other models in same firm, count of rival models
models_per_firm_date = panel.groupby(['date', 'firm'])['model_permaslug'].nunique().reset_index()
models_per_firm_date.columns = ['date', 'firm', 'n_own_models']

total_models_per_date = panel.groupby('date')['model_permaslug'].nunique().reset_index()
total_models_per_date.columns = ['date', 'n_total_models']

panel = panel.merge(models_per_firm_date, on=['date', 'firm'], how='left')
panel = panel.merge(total_models_per_date, on='date', how='left')
panel['n_rival_models'] = panel['n_total_models'] - panel['n_own_models']

# Characteristics-based instruments (BLP style): sum of rival characteristics
# Average rival context length, rival reasoning share
rival_chars = panel.groupby('date').agg(
    total_reasoning_models=('supports_reasoning', 'sum'),
    avg_context_all=('log_context', 'mean'),
).reset_index()

panel = panel.merge(rival_chars, on='date', suffixes=('', '_agg'))

# ============================================================
# 7. SAMPLE RESTRICTIONS
# ============================================================
print("Applying sample restrictions...")

# Record cleaning steps
cleaning_log = []

n_before = len(panel)
# Remove models with < 1000 total requests (too noisy)
model_totals = panel.groupby('model_permaslug')['count'].sum()
keep_models = model_totals[model_totals >= 1000].index
panel = panel[panel['model_permaslug'].isin(keep_models)]
n_after = len(panel)
cleaning_log.append(f"Step 1: Remove models with <1000 total requests: {n_before} → {n_after} obs ({n_before - n_after} removed, {len(model_totals) - len(keep_models)} models dropped)")

n_before = len(panel)
# Remove first 3 days (panel may start mid-crawl)
panel = panel[panel['date'] >= panel['date'].min() + pd.Timedelta(days=3)]
n_after = len(panel)
cleaning_log.append(f"Step 2: Remove first 3 days of panel: {n_before} → {n_after} obs")

n_before = len(panel)
# Remove observations with count=0
panel = panel[panel['count'] > 0]
n_after = len(panel)
cleaning_log.append(f"Step 3: Remove zero-count observations: {n_before} → {n_after} obs")

# Log dependent variable
panel['log_requests'] = np.log(panel['count'])
panel['log_tokens'] = np.log(panel['total_tokens'].replace(0, np.nan))

# ============================================================
# 8. FINAL VARIABLE SELECTION AND SAVE
# ============================================================
print("Saving analysis panel...")

# Select analysis variables
analysis_vars = [
    'model_permaslug', 'firm', 'date', 'count', 'log_requests',
    'total_tokens', 'log_tokens', 'total_prompt_tokens', 'total_completion_tokens',
    'total_native_tokens_reasoning', 'total_native_tokens_cached', 'total_tool_calls',
    'share', 's0', 'within_firm_share', 'lhs_berry', 'log_within_share',
    'model_age', 'model_age_sq', 'entry_date',
    'same_firm_entry_0_7', 'same_firm_entry_8_30',
    'rival_entry_0_7', 'rival_entry_8_30',
    'context_length', 'log_context', 'supports_reasoning', 'supports_tools',
    'supports_image', 'price_prompt', 'price_completion', 'price_blended',
    'log_price', 'is_free',
    'n_own_models', 'n_rival_models', 'n_total_models',
    'total_reasoning_models',
    'market_size', 'total_inside',
]

# Keep only available columns
available = [c for c in analysis_vars if c in panel.columns]
analysis = panel[available].copy()

analysis.to_csv(OUT / "analysis_panel.csv", index=False)
print(f"Saved analysis_panel.csv: {analysis.shape}")

# ============================================================
# 9. DATA CLEANING LOG
# ============================================================
cleaning_doc = f"""# Data Cleaning Log

## Raw Data
- Source: data/master/usage_daily.csv
- Initial observations: {df.shape[0]}
- Initial models: {df['model_permaslug'].nunique()}

## Cleaning Steps
"""
for step in cleaning_log:
    cleaning_doc += f"- {step}\n"

cleaning_doc += f"""
## Final Sample
- Observations: {len(analysis)}
- Unique models: {analysis['model_permaslug'].nunique()}
- Unique firms: {analysis['firm'].nunique()}
- Date range: {analysis['date'].min().date()} to {analysis['date'].max().date()}
- Models with pricing: {analysis['price_prompt'].notna().sum()} obs ({analysis[analysis['price_prompt'].notna()]['model_permaslug'].nunique()} models)
- Free models: {analysis[analysis['is_free']==True]['model_permaslug'].nunique()}
- Reasoning models: {analysis[analysis['supports_reasoning']==True]['model_permaslug'].nunique()}

## Entry Events
- Total entry events in sample: {len(first_seen[first_seen['model_permaslug'].isin(keep_models)])}
- Entry events after sample start: {len(first_seen[(first_seen['model_permaslug'].isin(keep_models)) & (first_seen['entry_date'] > analysis['date'].min())])}

## Outside Option
- Assumed inside share: 80% (outside option = 20% of market)
- Rationale: OpenRouter captures a substantial share of multi-model API traffic,
  but enterprise direct-contract usage is not observed. 20% outside option is conservative.
  Robustness: will vary between 10% and 40%.
"""

with open(OUT / "data_cleaning_log.md", 'w') as f:
    f.write(cleaning_doc)

print("\n=== Data construction complete ===")
print(f"Analysis panel: {analysis.shape}")
print(f"Entry events: {len(first_seen[first_seen['model_permaslug'].isin(keep_models)])}")
