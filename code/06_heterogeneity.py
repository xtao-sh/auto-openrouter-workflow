"""
06_heterogeneity.py
Phase 3d: Heterogeneity analysis (≥3 dimensions)
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT_TAB = OUT / "tables"
OUT_FIG = OUT / "figures"

plt.rcParams.update({
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 12,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False, 'font.family': 'serif',
})
COLORS = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12']

# ============================================================
print("Loading data...")
df = pd.read_csv(OUT / "analysis_panel.csv", parse_dates=['date', 'entry_date'])
df['day_id'] = (df['date'] - df['date'].min()).dt.days
for col in ['supports_reasoning', 'supports_tools', 'supports_image', 'is_free']:
    df[col] = df[col].astype(float)

results = []

# ============================================================
# DIMENSION 1: Entry type — same-family upgrade vs new product
# ============================================================
print("\n=== Heterogeneity 1: Entry type ===")

# Classify entry events: within same model family (e.g., claude-3.5 → claude-4.5) vs new product
# Heuristic: same "group" prefix → family upgrade
df['model_family'] = df['model_permaslug'].str.split('/').str[1].str.split('-').str[0]

# For same-firm entries, check if entrant shares model family with incumbent
# Create interaction: same_firm_entry × same_family
# Approximate: if a firm releases any model in the same family, it's a family upgrade

# For each model, identify its family
first_seen = df.groupby('model_permaslug')['date'].min().reset_index()
first_seen.columns = ['model_permaslug', 'entry_date_fs']
first_seen['firm_fs'] = first_seen['model_permaslug'].str.split('/').str[0]
first_seen['family_fs'] = first_seen['model_permaslug'].str.split('/').str[1].str.rsplit('-', n=1).str[0]

# For each model-day, compute same_family_entry and diff_family_entry
from collections import defaultdict
date_firm_family = defaultdict(lambda: defaultdict(set))
for _, row in first_seen.iterrows():
    d = row['entry_date_fs']
    f = row['firm_fs']
    fam = row['family_fs']
    date_firm_family[d][f].add(fam)

# Build same_family_entry indicator
def compute_family_entries(dates, firms, families, entry_df):
    same_fam = np.zeros(len(dates))
    diff_fam = np.zeros(len(dates))
    for i, (d, f, fam) in enumerate(zip(dates, firms, families)):
        for offset in range(0, 8):
            check_date = d - pd.Timedelta(days=offset)
            if check_date in date_firm_family and f in date_firm_family[check_date]:
                for entry_fam in date_firm_family[check_date][f]:
                    if entry_fam == fam:
                        same_fam[i] += 1
                    else:
                        diff_fam[i] += 1
    return same_fam, diff_fam

df['model_family_short'] = df['model_permaslug'].str.split('/').str[1].str.rsplit('-', n=1).str[0]
unique_fam = df[['date', 'firm', 'model_family_short']].drop_duplicates().reset_index(drop=True)
sf, dfam = compute_family_entries(
    unique_fam['date'].values, unique_fam['firm'].values,
    unique_fam['model_family_short'].values, first_seen)
unique_fam['same_family_entry_0_7'] = sf
unique_fam['diff_family_entry_0_7'] = dfam

df = df.merge(unique_fam, on=['date', 'firm', 'model_family_short'], how='left')

# TWFE regression
df_h1 = df.set_index(['model_permaslug', 'date'])
y_h1 = df_h1['log_requests']
X_h1 = df_h1[['same_family_entry_0_7', 'diff_family_entry_0_7']].fillna(0)
m_h1 = PanelOLS(y_h1, X_h1, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
print(f"Same-family entry: β = {m_h1.params['same_family_entry_0_7']:.4f} (SE={m_h1.std_errors['same_family_entry_0_7']:.4f})")
print(f"Diff-family entry: β = {m_h1.params['diff_family_entry_0_7']:.4f} (SE={m_h1.std_errors['diff_family_entry_0_7']:.4f})")

results.append({
    'Dimension': '1. Entry type',
    'Subgroup': 'Same-family upgrade',
    'Coefficient': f"{m_h1.params['same_family_entry_0_7']:.4f}",
    'SE': f"({m_h1.std_errors['same_family_entry_0_7']:.4f})",
    'N': m_h1.nobs,
})
results.append({
    'Dimension': '',
    'Subgroup': 'Different-family entry',
    'Coefficient': f"{m_h1.params['diff_family_entry_0_7']:.4f}",
    'SE': f"({m_h1.std_errors['diff_family_entry_0_7']:.4f})",
    'N': '',
})

# ============================================================
# DIMENSION 2: Model capability — reasoning vs non-reasoning
# ============================================================
print("\n=== Heterogeneity 2: Reasoning capability ===")

# Split sample by whether the incumbent model supports reasoning
df_reasoning = df[df['supports_reasoning'] == 1].copy()
df_nonreasoning = df[df['supports_reasoning'] == 0].copy()

for label, subset in [('Reasoning models', df_reasoning), ('Non-reasoning models', df_nonreasoning)]:
    if len(subset) < 100:
        print(f"  {label}: too few obs ({len(subset)}), skipping")
        continue
    sub_panel = subset.set_index(['model_permaslug', 'date'])
    y_sub = sub_panel['log_requests']
    X_sub = sub_panel[['same_firm_entry_0_7']].fillna(0)
    try:
        m_sub = PanelOLS(y_sub, X_sub, entity_effects=True, time_effects=True).fit(
            cov_type='clustered', cluster_entity=True)
        print(f"  {label}: β = {m_sub.params['same_firm_entry_0_7']:.4f} "
              f"(SE={m_sub.std_errors['same_firm_entry_0_7']:.4f}), N={m_sub.nobs}")
        results.append({
            'Dimension': '2. Reasoning capability',
            'Subgroup': label,
            'Coefficient': f"{m_sub.params['same_firm_entry_0_7']:.4f}",
            'SE': f"({m_sub.std_errors['same_firm_entry_0_7']:.4f})",
            'N': m_sub.nobs,
        })
    except Exception as e:
        print(f"  {label}: estimation failed — {e}")

# ============================================================
# DIMENSION 3: Firm size — top 5 vs others
# ============================================================
print("\n=== Heterogeneity 3: Firm size ===")

firm_total = df.groupby('firm')['count'].sum()
top5_firms = firm_total.nlargest(5).index.tolist()
print(f"Top 5 firms: {top5_firms}")

df_top5 = df[df['firm'].isin(top5_firms)].copy()
df_small = df[~df['firm'].isin(top5_firms)].copy()

for label, subset in [('Top-5 firms', df_top5), ('Smaller firms', df_small)]:
    sub_panel = subset.set_index(['model_permaslug', 'date'])
    y_sub = sub_panel['log_requests']
    X_sub = sub_panel[['same_firm_entry_0_7']].fillna(0)
    try:
        m_sub = PanelOLS(y_sub, X_sub, entity_effects=True, time_effects=True).fit(
            cov_type='clustered', cluster_entity=True)
        print(f"  {label}: β = {m_sub.params['same_firm_entry_0_7']:.4f} "
              f"(SE={m_sub.std_errors['same_firm_entry_0_7']:.4f}), N={m_sub.nobs}")
        results.append({
            'Dimension': '3. Firm size',
            'Subgroup': label,
            'Coefficient': f"{m_sub.params['same_firm_entry_0_7']:.4f}",
            'SE': f"({m_sub.std_errors['same_firm_entry_0_7']:.4f})",
            'N': m_sub.nobs,
        })
    except Exception as e:
        print(f"  {label}: estimation failed — {e}")

# ============================================================
# DIMENSION 4: Model age — young vs mature
# ============================================================
print("\n=== Heterogeneity 4: Model age ===")

df['model_age'] = (df['date'] - df['entry_date']).dt.days
df_young = df[df['model_age'] <= 30].copy()
df_mature = df[df['model_age'] > 30].copy()

for label, subset in [('Young (≤30 days)', df_young), ('Mature (>30 days)', df_mature)]:
    sub_panel = subset.set_index(['model_permaslug', 'date'])
    y_sub = sub_panel['log_requests']
    X_sub = sub_panel[['same_firm_entry_0_7']].fillna(0)
    try:
        m_sub = PanelOLS(y_sub, X_sub, entity_effects=True, time_effects=True).fit(
            cov_type='clustered', cluster_entity=True)
        print(f"  {label}: β = {m_sub.params['same_firm_entry_0_7']:.4f} "
              f"(SE={m_sub.std_errors['same_firm_entry_0_7']:.4f}), N={m_sub.nobs}")
        results.append({
            'Dimension': '4. Model age',
            'Subgroup': label,
            'Coefficient': f"{m_sub.params['same_firm_entry_0_7']:.4f}",
            'SE': f"({m_sub.std_errors['same_firm_entry_0_7']:.4f})",
            'N': m_sub.nobs,
        })
    except Exception as e:
        print(f"  {label}: estimation failed — {e}")

# ============================================================
# NESTED LOGIT HETEROGENEITY: σ by subgroup
# ============================================================
print("\n=== Nested Logit σ by subgroup ===")
df_priced = df[df['log_price'].notna() & df['log_context'].notna()].copy()
demean_vars = ['lhs_berry', 'log_within_share', 'log_context', 'supports_reasoning',
               'supports_tools', 'model_age', 'log_price']
for v in demean_vars:
    df_priced[f'{v}_dm'] = df_priced[v] - df_priced.groupby('day_id')[v].transform('mean')

formula_nl = 'lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_share_dm'

sigma_by_group = {}
for group_var, group_vals, group_labels in [
    ('supports_reasoning', [0, 1], ['Non-reasoning', 'Reasoning']),
    ('is_free', [0, 1], ['Paid', 'Free']),
]:
    for val, label in zip(group_vals, group_labels):
        subset = df_priced[df_priced[group_var] == val]
        if len(subset) < 500:
            continue
        try:
            m = smf.ols(formula_nl, data=subset).fit(
                cov_type='cluster', cov_kwds={'groups': subset['model_permaslug']})
            sigma = m.params['log_within_share_dm']
            sigma_se = m.bse['log_within_share_dm']
            sigma_by_group[label] = (sigma, sigma_se, int(m.nobs))
            print(f"  {label}: σ = {sigma:.3f} (SE={sigma_se:.3f}), N={int(m.nobs)}")
        except Exception as e:
            print(f"  {label}: failed — {e}")

# ============================================================
# FIGURE: Heterogeneity summary
# ============================================================
print("\nCreating heterogeneity figure...")

het_df = pd.DataFrame(results)
het_df = het_df[het_df['Coefficient'] != ''].copy()
het_df['coef_val'] = het_df['Coefficient'].astype(float)
het_df['se_val'] = het_df['SE'].str.strip('()').astype(float)

fig, ax = plt.subplots(figsize=(10, 7))
y_pos = range(len(het_df))
ax.barh(y_pos, het_df['coef_val'], xerr=1.96*het_df['se_val'],
        color=[COLORS[i % len(COLORS)] for i in range(len(het_df))],
        alpha=0.8, capsize=4, edgecolor='white')
labels = [f"{row['Dimension']}: {row['Subgroup']}" if row['Dimension'] else f"  {row['Subgroup']}"
          for _, row in het_df.iterrows()]
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9)
ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Coefficient on Same-Firm Entry [0,7]')
ax.set_title('Figure 14: Heterogeneity in Same-Firm Entry Effects')
plt.tight_layout()
plt.savefig(OUT_FIG / "fig14_heterogeneity.png")
plt.close()

# ============================================================
# SAVE
# ============================================================
het_table = pd.DataFrame(results)
het_table.to_csv(OUT_TAB / "table05_heterogeneity.csv", index=False)

# Save sigma by subgroup
if sigma_by_group:
    sigma_df = pd.DataFrame([
        {'Group': k, 'sigma': v[0], 'sigma_se': v[1], 'N': v[2]}
        for k, v in sigma_by_group.items()
    ])
    sigma_df.to_csv(OUT_TAB / "table06_sigma_heterogeneity.csv", index=False)

print("\n=== Heterogeneity analysis complete ===")
