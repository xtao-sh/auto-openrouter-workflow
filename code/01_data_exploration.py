"""
01_data_exploration.py
Phase 1: Data exploration for LLM API market economics paper.
Produces ≥7 exploratory figures + descriptive statistics table + data summary.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import os
from pathlib import Path
from datetime import datetime

# === Paths ===
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_FIG = ROOT / "output" / "figures"
OUT_TAB = ROOT / "output" / "tables"
OUT = ROOT / "output"
OUT_FIG.mkdir(parents=True, exist_ok=True)
OUT_TAB.mkdir(parents=True, exist_ok=True)

# === Style ===
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'serif',
})
COLORS = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12',
          '#9b59b6', '#1abc9c', '#e67e22', '#34495e', '#c0392b']

# ============================================================
# LOAD DATA
# ============================================================
print("Loading usage_daily.csv...")
df = pd.read_csv(DATA / "master" / "usage_daily.csv")
df['date'] = pd.to_datetime(df['date'])

# Exclude same-day (potentially incomplete) data
latest_date = df['date'].max()
df = df[df['date'] < latest_date]

# Load model metadata
print("Loading model metadata...")
models_meta = pd.read_csv(DATA / "master" / "models_enriched_latest.csv")

# Load rankings data (weekly top_models and market_share)
print("Loading rankings data...")
rankings_dir = DATA / "rankings" / "latest"
if not rankings_dir.exists():
    rankings_dir = DATA / "rankings" / "20260325"

with open(rankings_dir / "top_models.json") as f:
    top_models_data = json.load(f)

with open(rankings_dir / "market_share.json") as f:
    market_share_data = json.load(f)

print(f"Usage panel: {df.shape[0]} obs, {df['model_permaslug'].nunique()} models, "
      f"{df['date'].min().date()} to {df['date'].max().date()}")

# ============================================================
# DERIVED VARIABLES
# ============================================================
df['total_tokens'] = df['total_prompt_tokens'] + df['total_completion_tokens']
df['tokens_per_request'] = df['total_tokens'] / df['count'].replace(0, np.nan)
df['reasoning_share'] = df['total_native_tokens_reasoning'] / df['total_tokens'].replace(0, np.nan)
df['cache_share'] = df['total_native_tokens_cached'] / df['total_prompt_tokens'].replace(0, np.nan)
df['tool_call_rate'] = df['total_tool_calls'] / df['count'].replace(0, np.nan)
df['completion_ratio'] = df['total_completion_tokens'] / df['total_prompt_tokens'].replace(0, np.nan)

# Extract author (firm) from model slug
df['author'] = df['model_permaslug'].str.split('/').str[0]

# ============================================================
# FIGURE 1: Aggregate daily requests and tokens over time
# ============================================================
print("Figure 1: Aggregate trends...")
daily_agg = df.groupby('date').agg(
    total_requests=('count', 'sum'),
    total_tokens=('total_tokens', 'sum'),
    n_models=('model_permaslug', 'nunique')
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(daily_agg['date'], daily_agg['total_requests'] / 1e6,
         color=COLORS[0], linewidth=1.5, label='Daily requests (M)')
ax1.set_ylabel('Daily Requests (millions)', color=COLORS[0])
ax1.tick_params(axis='y', labelcolor=COLORS[0])

ax2 = ax1.twinx()
ax2.plot(daily_agg['date'], daily_agg['total_tokens'] / 1e9,
         color=COLORS[1], linewidth=1.5, linestyle='--', label='Daily tokens (B)')
ax2.set_ylabel('Daily Tokens (billions)', color=COLORS[1])
ax2.tick_params(axis='y', labelcolor=COLORS[1])
ax2.spines['right'].set_visible(True)

ax1.set_xlabel('')
ax1.set_title('Figure 1: Aggregate Daily API Usage on OpenRouter')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
fig.autofmt_xdate()

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False)

plt.savefig(OUT_FIG / "fig01_aggregate_trends.png")
plt.close()

# ============================================================
# FIGURE 2: Market concentration (HHI) over time
# ============================================================
print("Figure 2: Market concentration (HHI)...")

# Compute daily HHI based on request counts
daily_model = df.groupby(['date', 'model_permaslug'])['count'].sum().reset_index()
daily_total = daily_model.groupby('date')['count'].sum().rename('daily_total')
daily_model = daily_model.merge(daily_total, on='date')
daily_model['share'] = daily_model['count'] / daily_model['daily_total']
daily_model['share_sq'] = daily_model['share'] ** 2

hhi_daily = daily_model.groupby('date')['share_sq'].sum().reset_index()
hhi_daily.columns = ['date', 'HHI']
hhi_daily['HHI_7d'] = hhi_daily['HHI'].rolling(7, min_periods=1).mean()

# Also compute firm-level HHI
daily_firm = df.groupby(['date', 'author'])['count'].sum().reset_index()
daily_firm_total = daily_firm.groupby('date')['count'].sum().rename('daily_total')
daily_firm = daily_firm.merge(daily_firm_total, on='date')
daily_firm['share'] = daily_firm['count'] / daily_firm['daily_total']
daily_firm['share_sq'] = daily_firm['share'] ** 2
hhi_firm_daily = daily_firm.groupby('date')['share_sq'].sum().reset_index()
hhi_firm_daily.columns = ['date', 'HHI_firm']
hhi_firm_daily['HHI_firm_7d'] = hhi_firm_daily['HHI_firm'].rolling(7, min_periods=1).mean()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hhi_daily['date'], hhi_daily['HHI_7d'] * 10000, color=COLORS[0],
        linewidth=2, label='Model-level HHI')
ax.plot(hhi_firm_daily['date'], hhi_firm_daily['HHI_firm_7d'] * 10000, color=COLORS[1],
        linewidth=2, linestyle='--', label='Firm-level HHI')
ax.axhline(y=1500, color='gray', linestyle=':', alpha=0.7, label='Moderate concentration threshold')
ax.axhline(y=2500, color='gray', linestyle='-.', alpha=0.7, label='High concentration threshold')
ax.set_ylabel('HHI (×10,000)')
ax.set_title('Figure 2: Market Concentration Over Time (7-day Rolling Average)')
ax.legend(frameon=False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
fig.autofmt_xdate()
plt.savefig(OUT_FIG / "fig02_hhi_over_time.png")
plt.close()

# ============================================================
# FIGURE 3: Top 10 models market share evolution
# ============================================================
print("Figure 3: Top 10 models market share...")

# Identify top 10 models by total requests
top10_models = df.groupby('model_permaslug')['count'].sum().nlargest(10).index.tolist()

# Compute weekly market shares for top 10
df['week'] = df['date'].dt.to_period('W').apply(lambda x: x.start_time)
weekly_total = df.groupby('week')['count'].sum().rename('week_total')
weekly_model = df.groupby(['week', 'model_permaslug'])['count'].sum().reset_index()
weekly_model = weekly_model.merge(weekly_total, on='week')
weekly_model['share'] = weekly_model['count'] / weekly_model['week_total']

fig, ax = plt.subplots(figsize=(14, 7))
for i, model in enumerate(top10_models):
    subset = weekly_model[weekly_model['model_permaslug'] == model].sort_values('week')
    short_name = model.split('/')[-1][:30]
    ax.plot(subset['week'], subset['share'] * 100, color=COLORS[i % len(COLORS)],
            linewidth=1.8, label=short_name, marker='o', markersize=3)

ax.set_ylabel('Market Share (%)')
ax.set_title('Figure 3: Weekly Market Share of Top 10 Models (by requests)')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False, fontsize=9)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
fig.autofmt_xdate()
plt.savefig(OUT_FIG / "fig03_top10_market_share.png")
plt.close()

# ============================================================
# FIGURE 4: Firm-level market share evolution
# ============================================================
print("Figure 4: Firm-level market share...")

top_firms = df.groupby('author')['count'].sum().nlargest(8).index.tolist()
weekly_firm = df.groupby(['week', 'author'])['count'].sum().reset_index()
weekly_firm = weekly_firm.merge(weekly_total, on='week')
weekly_firm['share'] = weekly_firm['count'] / weekly_firm['week_total']

fig, ax = plt.subplots(figsize=(12, 7))
for i, firm in enumerate(top_firms):
    subset = weekly_firm[weekly_firm['author'] == firm].sort_values('week')
    ax.fill_between([], [], alpha=0.3)  # placeholder for stacked
    ax.plot(subset['week'], subset['share'] * 100, color=COLORS[i % len(COLORS)],
            linewidth=2, label=firm, marker='o', markersize=3)

ax.set_ylabel('Market Share (%)')
ax.set_title('Figure 4: Firm-Level Weekly Market Share (by requests)')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False, fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
fig.autofmt_xdate()
plt.savefig(OUT_FIG / "fig04_firm_market_share.png")
plt.close()

# ============================================================
# FIGURE 5: Distribution of model usage (log scale)
# ============================================================
print("Figure 5: Usage distribution...")

model_total = df.groupby('model_permaslug')['count'].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 5a: Rank-size plot (log-log)
ranks = np.arange(1, len(model_total) + 1)
axes[0].scatter(ranks, model_total.values, s=10, color=COLORS[0], alpha=0.7)
axes[0].set_xscale('log')
axes[0].set_yscale('log')
axes[0].set_xlabel('Rank')
axes[0].set_ylabel('Total Requests (log scale)')
axes[0].set_title('(a) Rank-Size Distribution')

# Fit power law line
log_r = np.log(ranks[:200])
log_y = np.log(model_total.values[:200])
slope, intercept = np.polyfit(log_r, log_y, 1)
axes[0].plot(ranks[:200], np.exp(intercept) * ranks[:200]**slope,
             color=COLORS[1], linestyle='--', linewidth=1.5,
             label=f'Power law fit: α={-slope:.2f}')
axes[0].legend(frameon=False)

# 5b: Histogram of log(total requests)
axes[1].hist(np.log10(model_total.values), bins=40, color=COLORS[2], alpha=0.8, edgecolor='white')
axes[1].set_xlabel('log₁₀(Total Requests)')
axes[1].set_ylabel('Number of Models')
axes[1].set_title('(b) Distribution of Model Usage')
axes[1].axvline(x=np.log10(1000 * 94), color=COLORS[1], linestyle='--',
                label=f'~1K req/day threshold')
axes[1].legend(frameon=False)

fig.suptitle('Figure 5: Cross-Model Usage Distribution', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(OUT_FIG / "fig05_usage_distribution.png")
plt.close()

# ============================================================
# FIGURE 6: Reasoning tokens and tool calls adoption
# ============================================================
print("Figure 6: Reasoning & tool call adoption...")

# Daily aggregate reasoning share and tool call rate
daily_features = df.groupby('date').agg(
    total_reasoning=('total_native_tokens_reasoning', 'sum'),
    total_tokens=('total_tokens', 'sum'),
    total_tool_calls=('total_tool_calls', 'sum'),
    total_requests=('count', 'sum'),
    total_cached=('total_native_tokens_cached', 'sum'),
    total_prompt=('total_prompt_tokens', 'sum'),
).reset_index()

daily_features['reasoning_share'] = daily_features['total_reasoning'] / daily_features['total_tokens']
daily_features['tool_call_rate'] = daily_features['total_tool_calls'] / daily_features['total_requests']
daily_features['cache_share'] = daily_features['total_cached'] / daily_features['total_prompt']

# 7-day rolling
for col in ['reasoning_share', 'tool_call_rate', 'cache_share']:
    daily_features[f'{col}_7d'] = daily_features[col].rolling(7, min_periods=1).mean()

fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

axes[0].plot(daily_features['date'], daily_features['reasoning_share_7d'] * 100,
             color=COLORS[0], linewidth=2)
axes[0].set_ylabel('Share of Total Tokens (%)')
axes[0].set_title('(a) Reasoning Token Share')
axes[0].fill_between(daily_features['date'], 0, daily_features['reasoning_share_7d'] * 100,
                     alpha=0.15, color=COLORS[0])

axes[1].plot(daily_features['date'], daily_features['tool_call_rate_7d'],
             color=COLORS[1], linewidth=2)
axes[1].set_ylabel('Tool Calls per Request')
axes[1].set_title('(b) Tool Call Intensity')

axes[2].plot(daily_features['date'], daily_features['cache_share_7d'] * 100,
             color=COLORS[2], linewidth=2)
axes[2].set_ylabel('Share of Prompt Tokens (%)')
axes[2].set_title('(c) Prompt Cache Share')
axes[2].set_xlabel('')

for ax in axes:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

fig.suptitle('Figure 6: Technology Adoption Trends (7-day Rolling Average)', fontsize=14, y=1.01)
plt.tight_layout()
plt.savefig(OUT_FIG / "fig06_feature_adoption.png")
plt.close()

# ============================================================
# FIGURE 7: Tokens per request across model types
# ============================================================
print("Figure 7: Tokens per request by model...")

# Classify models: reasoning vs non-reasoning
reasoning_models = df[df['total_native_tokens_reasoning'] > 0]['model_permaslug'].unique()

# For top 20 models, compute avg tokens per request
top20 = df.groupby('model_permaslug').agg(
    total_req=('count', 'sum'),
    total_tok=('total_tokens', 'sum'),
    total_reasoning=('total_native_tokens_reasoning', 'sum'),
).nlargest(20, 'total_req')
top20['tpr'] = top20['total_tok'] / top20['total_req']
top20['is_reasoning'] = top20.index.isin(reasoning_models)
top20 = top20.sort_values('tpr', ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
colors_bar = [COLORS[1] if r else COLORS[2] for r in top20['is_reasoning']]
short_names = [m.split('/')[-1][:35] for m in top20.index]
ax.barh(range(len(top20)), top20['tpr'], color=colors_bar, alpha=0.85, edgecolor='white')
ax.set_yticks(range(len(top20)))
ax.set_yticklabels(short_names, fontsize=9)
ax.set_xlabel('Average Tokens per Request')
ax.set_title('Figure 7: Token Intensity by Model (Top 20 by Volume)')

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=COLORS[1], alpha=0.85, label='Reasoning model'),
                   Patch(facecolor=COLORS[2], alpha=0.85, label='Non-reasoning model')]
ax.legend(handles=legend_elements, frameon=False, loc='lower right')
plt.tight_layout()
plt.savefig(OUT_FIG / "fig07_tokens_per_request.png")
plt.close()

# ============================================================
# FIGURE 8: Correlation matrix of key variables
# ============================================================
print("Figure 8: Correlation matrix...")

# Model-level aggregates for correlation
model_agg = df.groupby('model_permaslug').agg(
    avg_daily_requests=('count', 'mean'),
    avg_tokens_per_req=('tokens_per_request', 'mean'),
    avg_reasoning_share=('reasoning_share', 'mean'),
    avg_cache_share=('cache_share', 'mean'),
    avg_tool_call_rate=('tool_call_rate', 'mean'),
    avg_completion_ratio=('completion_ratio', 'mean'),
    n_days_active=('date', 'nunique'),
).dropna()

# Filter to models with at least 30 days
model_agg = model_agg[model_agg['n_days_active'] >= 30]
model_agg['log_avg_requests'] = np.log1p(model_agg['avg_daily_requests'])

corr_vars = ['log_avg_requests', 'avg_tokens_per_req', 'avg_reasoning_share',
             'avg_cache_share', 'avg_tool_call_rate', 'avg_completion_ratio']
corr_labels = ['Log Requests', 'Tokens/Req', 'Reasoning Share',
               'Cache Share', 'Tool Call Rate', 'Completion Ratio']

corr = model_agg[corr_vars].corr()

fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax.set_xticks(range(len(corr_labels)))
ax.set_yticks(range(len(corr_labels)))
ax.set_xticklabels(corr_labels, rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(corr_labels, fontsize=10)

for i in range(len(corr_vars)):
    for j in range(len(corr_vars)):
        val = corr.values[i, j]
        color = 'white' if abs(val) > 0.5 else 'black'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=10)

plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title('Figure 8: Correlation Matrix of Model-Level Characteristics')
plt.tight_layout()
plt.savefig(OUT_FIG / "fig08_correlation_matrix.png")
plt.close()

# ============================================================
# FIGURE 9: New model entry over time
# ============================================================
print("Figure 9: Model entry dynamics...")

# First appearance of each model in the panel
first_seen = df.groupby('model_permaslug')['date'].min().reset_index()
first_seen.columns = ['model_permaslug', 'first_date']
first_seen['first_week'] = first_seen['first_date'].dt.to_period('W').apply(lambda x: x.start_time)

entry_counts = first_seen.groupby('first_week').size().reset_index(name='new_models')
entry_counts['cumulative'] = entry_counts['new_models'].cumsum()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(entry_counts['first_week'], entry_counts['new_models'],
        width=5, color=COLORS[2], alpha=0.7, label='New models per week')
ax1.set_ylabel('New Models', color=COLORS[2])

ax2 = ax1.twinx()
ax2.plot(entry_counts['first_week'], entry_counts['cumulative'],
         color=COLORS[0], linewidth=2.5, label='Cumulative models')
ax2.set_ylabel('Cumulative Models', color=COLORS[0])
ax2.spines['right'].set_visible(True)

ax1.set_title('Figure 9: Model Entry Dynamics')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
fig.autofmt_xdate()

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False)
plt.savefig(OUT_FIG / "fig09_model_entry.png")
plt.close()

# ============================================================
# TABLE 1: Descriptive Statistics
# ============================================================
print("Computing descriptive statistics...")

# Panel-level stats
panel_stats = {
    'Panel dimensions': '',
    'Total observations': f'{len(df):,}',
    'Unique models': f'{df["model_permaslug"].nunique()}',
    'Unique firms (authors)': f'{df["author"].nunique()}',
    'Date range': f'{df["date"].min().date()} to {df["date"].max().date()}',
    'Panel length (days)': f'{(df["date"].max() - df["date"].min()).days}',
    'Avg observations per model': f'{len(df) / df["model_permaslug"].nunique():.1f}',
}

# Variable-level stats
vars_for_stats = {
    'count': 'Daily requests',
    'total_prompt_tokens': 'Prompt tokens',
    'total_completion_tokens': 'Completion tokens',
    'total_tokens': 'Total tokens',
    'total_native_tokens_reasoning': 'Reasoning tokens',
    'total_native_tokens_cached': 'Cached tokens',
    'total_tool_calls': 'Tool calls',
    'tokens_per_request': 'Tokens per request',
    'reasoning_share': 'Reasoning share',
    'cache_share': 'Cache share',
    'tool_call_rate': 'Tool call rate',
}

stats_rows = []
for var, label in vars_for_stats.items():
    s = df[var]
    stats_rows.append({
        'Variable': label,
        'N': f'{s.count():,}',
        'Mean': f'{s.mean():,.1f}' if s.mean() > 1 else f'{s.mean():.4f}',
        'SD': f'{s.std():,.1f}' if s.std() > 1 else f'{s.std():.4f}',
        'Median': f'{s.median():,.1f}' if s.median() > 1 else f'{s.median():.4f}',
        'P25': f'{s.quantile(0.25):,.1f}' if s.quantile(0.25) > 1 else f'{s.quantile(0.25):.4f}',
        'P75': f'{s.quantile(0.75):,.1f}' if s.quantile(0.75) > 1 else f'{s.quantile(0.75):.4f}',
        'Min': f'{s.min():,.0f}' if s.min() > 1 else f'{s.min():.4f}',
        'Max': f'{s.max():,.0f}' if s.max() > 1 else f'{s.max():.4f}',
    })

stats_df = pd.DataFrame(stats_rows)
stats_df.to_csv(OUT_TAB / "table01_descriptive_stats.csv", index=False)
print("Saved: table01_descriptive_stats.csv")

# ============================================================
# Additional: Market structure summary stats
# ============================================================

# Top 10 concentration ratio (CR10) over time
cr10_daily = daily_model.sort_values(['date', 'count'], ascending=[True, False])
cr10_daily = cr10_daily.groupby('date').head(10)
cr10 = cr10_daily.groupby('date')['share'].sum().reset_index()
cr10.columns = ['date', 'CR10']

# Save market structure stats
market_stats = {
    'Mean HHI (model-level, ×10000)': f'{hhi_daily["HHI"].mean() * 10000:.0f}',
    'Mean HHI (firm-level, ×10000)': f'{hhi_firm_daily["HHI_firm"].mean() * 10000:.0f}',
    'Mean CR10': f'{cr10["CR10"].mean():.3f}',
    'Number of models with >1K daily requests (median day)': str(
        int(daily_model[daily_model['count'] > 1000].groupby('date')['model_permaslug'].nunique().median())),
    'Top model share (mean)': f'{daily_model.groupby("date")["share"].max().mean():.3f}',
}

# Save all summary stats for the data summary document
summary_data = {
    'panel_stats': panel_stats,
    'market_stats': market_stats,
}

# ============================================================
# FIGURE 10 (bonus): Weekday effects
# ============================================================
print("Figure 10: Weekday effects...")

df['weekday'] = df['date'].dt.dayofweek
df['weekday_name'] = df['date'].dt.day_name()

weekday_agg = df.groupby('weekday').agg(
    mean_requests=('count', 'mean'),
    total_requests=('count', 'sum'),
).reset_index()
weekday_agg['weekday_name'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday_agg['relative'] = weekday_agg['mean_requests'] / weekday_agg['mean_requests'].mean()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(weekday_agg['weekday_name'], weekday_agg['relative'],
              color=[COLORS[0] if d < 5 else COLORS[1] for d in range(7)],
              alpha=0.85, edgecolor='white')
ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
ax.set_ylabel('Relative to Daily Average')
ax.set_title('Figure 10: Day-of-Week Effects on API Usage')
for bar, val in zip(bars, weekday_agg['relative']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{val:.2f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(OUT_FIG / "fig10_weekday_effects.png")
plt.close()

# ============================================================
# DATA SUMMARY DOCUMENT
# ============================================================
print("Writing data summary...")

summary_text = f"""# Data Exploration Summary

## Panel Dimensions
- **Observations**: {len(df):,} model×day observations
- **Unique models**: {df['model_permaslug'].nunique()}
- **Unique firms**: {df['author'].nunique()}
- **Date range**: {df['date'].min().date()} to {df['date'].max().date()} ({(df['date'].max() - df['date'].min()).days} days)
- **Average days per model**: {len(df) / df['model_permaslug'].nunique():.1f}

## Market Structure
- **Mean model-level HHI**: {hhi_daily['HHI'].mean() * 10000:.0f} (×10,000 scale)
- **Mean firm-level HHI**: {hhi_firm_daily['HHI_firm'].mean() * 10000:.0f} (×10,000 scale)
- **Mean CR10**: {cr10['CR10'].mean():.1%}
- **Median # models with >1K daily requests**: {int(daily_model[daily_model['count'] > 1000].groupby('date')['model_permaslug'].nunique().median())}
- **Top model daily share (mean)**: {daily_model.groupby('date')['share'].max().mean():.1%}

## Key Distributional Facts
- Usage is extremely skewed: median model gets {df.groupby('model_permaslug')['count'].sum().median():,.0f} total requests vs mean of {df.groupby('model_permaslug')['count'].sum().mean():,.0f}
- Power law fit (top 200 models): α = {-slope:.2f}
- {len(model_total[model_total > 1000 * 94])}/{len(model_total)} models ({len(model_total[model_total > 1000 * 94])/len(model_total):.0%}) have >1K daily average requests

## Technology Adoption Trends
- **Reasoning tokens**: {daily_features['reasoning_share'].iloc[-7:].mean():.1%} of total tokens (latest week)
- **Tool call rate**: {daily_features['tool_call_rate'].iloc[-7:].mean():.3f} calls per request (latest week)
- **Cache share**: {daily_features['cache_share'].iloc[-7:].mean():.1%} of prompt tokens (latest week)

## Weekday Effects
- Weekdays show {weekday_agg[weekday_agg['weekday'] < 5]['relative'].mean():.0%} of average usage
- Weekends show {weekday_agg[weekday_agg['weekday'] >= 5]['relative'].mean():.0%} of average usage
- Strongest day: {weekday_agg.loc[weekday_agg['relative'].idxmax(), 'weekday_name']} ({weekday_agg['relative'].max():.2f}×)
- Weakest day: {weekday_agg.loc[weekday_agg['relative'].idxmin(), 'weekday_name']} ({weekday_agg['relative'].min():.2f}×)

## New Model Entry
- {first_seen.shape[0]} unique models observed
- First model entry date in panel: {first_seen['first_date'].min().date()}
- Median weekly entry rate: {entry_counts['new_models'].median():.0f} new models/week

## Data Quality Considerations
- OpenRouter retroactively updates historical data; high-volume models (>10K req/day) are stable (±4%), low-volume models are volatile
- Same-day data excluded (potentially incomplete)
- Recommended: use 7-day rolling averages, filter to >1K req/day for quantitative analysis

## Figures Produced
1. fig01_aggregate_trends.png — Daily requests and tokens over time
2. fig02_hhi_over_time.png — Model-level and firm-level HHI
3. fig03_top10_market_share.png — Top 10 models weekly market share
4. fig04_firm_market_share.png — Firm-level weekly market share
5. fig05_usage_distribution.png — Rank-size and histogram of usage
6. fig06_feature_adoption.png — Reasoning, tool calls, cache adoption
7. fig07_tokens_per_request.png — Token intensity by model
8. fig08_correlation_matrix.png — Correlation of model characteristics
9. fig09_model_entry.png — New model entry dynamics
10. fig10_weekday_effects.png — Day-of-week patterns

## Tables Produced
1. table01_descriptive_stats.csv — Full descriptive statistics
"""

with open(OUT / "data_summary.md", 'w') as f:
    f.write(summary_text)

print("\n=== Phase 1 complete ===")
print(f"Figures: {len(list(OUT_FIG.glob('fig*.png')))} files in output/figures/")
print(f"Tables: {len(list(OUT_TAB.glob('table*.csv')))} files in output/tables/")
print(f"Summary: output/data_summary.md")
