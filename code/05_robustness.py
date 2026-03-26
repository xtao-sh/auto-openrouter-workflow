"""
05_robustness.py
Phase 3c: Robustness checks (≥5 per pre-analysis plan)
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

df['total_tokens'] = df['total_prompt_tokens'] + df['total_completion_tokens']
df['log_tokens'] = np.log(df['total_tokens'].replace(0, np.nan))

results = []

# ============================================================
# ROBUSTNESS 1: Alternative DV — log tokens
# ============================================================
print("\n=== Rob 1: Log tokens as DV ===")
df_r1 = df.dropna(subset=['log_tokens']).copy()
df_r1_panel = df_r1.set_index(['model_permaslug', 'date'])
y_r1 = df_r1_panel['log_tokens']
X_r1 = df_r1_panel[['same_firm_entry_0_7']].fillna(0)
m_r1 = PanelOLS(y_r1, X_r1, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
results.append({
    'Check': '(1) DV: Log tokens',
    'Same-firm [0,7]': f"{m_r1.params['same_firm_entry_0_7']:.4f}",
    'SE': f"({m_r1.std_errors['same_firm_entry_0_7']:.4f})",
    'N': m_r1.nobs,
    'R²w': f"{m_r1.rsquared_within:.3f}",
})
print(f"β = {m_r1.params['same_firm_entry_0_7']:.4f} (SE={m_r1.std_errors['same_firm_entry_0_7']:.4f})")

# ============================================================
# ROBUSTNESS 2: DV = market share
# ============================================================
print("\n=== Rob 2: Market share as DV ===")
df['log_share'] = np.log(df['share'].clip(lower=1e-10))
df_r2_panel = df.set_index(['model_permaslug', 'date'])
y_r2 = df_r2_panel['log_share']
X_r2 = df_r2_panel[['same_firm_entry_0_7']].fillna(0)
m_r2 = PanelOLS(y_r2, X_r2, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
results.append({
    'Check': '(2) DV: Log market share',
    'Same-firm [0,7]': f"{m_r2.params['same_firm_entry_0_7']:.4f}",
    'SE': f"({m_r2.std_errors['same_firm_entry_0_7']:.4f})",
    'N': m_r2.nobs,
    'R²w': f"{m_r2.rsquared_within:.3f}",
})
print(f"β = {m_r2.params['same_firm_entry_0_7']:.4f} (SE={m_r2.std_errors['same_firm_entry_0_7']:.4f})")

# ============================================================
# ROBUSTNESS 3: High-volume models only (>10K daily avg)
# ============================================================
print("\n=== Rob 3: High-volume models only ===")
model_avg = df.groupby('model_permaslug')['count'].mean()
hv_models = model_avg[model_avg > 10000].index
df_r3 = df[df['model_permaslug'].isin(hv_models)].copy()
df_r3_panel = df_r3.set_index(['model_permaslug', 'date'])
y_r3 = df_r3_panel['log_requests']
X_r3 = df_r3_panel[['same_firm_entry_0_7']].fillna(0)
m_r3 = PanelOLS(y_r3, X_r3, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
results.append({
    'Check': f'(3) High-volume only (>{10}K/day, N_models={len(hv_models)})',
    'Same-firm [0,7]': f"{m_r3.params['same_firm_entry_0_7']:.4f}",
    'SE': f"({m_r3.std_errors['same_firm_entry_0_7']:.4f})",
    'N': m_r3.nobs,
    'R²w': f"{m_r3.rsquared_within:.3f}",
})
print(f"β = {m_r3.params['same_firm_entry_0_7']:.4f} (SE={m_r3.std_errors['same_firm_entry_0_7']:.4f}), N_models={len(hv_models)}")

# ============================================================
# ROBUSTNESS 4: Alternative nesting — by capability tier
# ============================================================
print("\n=== Rob 4: Nested logit by capability tier ===")
df_priced = df[df['log_price'].notna() & df['log_context'].notna()].copy()

# Define capability tier: reasoning vs non-reasoning
df_priced['cap_tier'] = df_priced['supports_reasoning'].astype(int).astype(str)
tier_daily = df_priced.groupby(['date', 'cap_tier'])['count'].sum().reset_index()
tier_daily.columns = ['date', 'cap_tier', 'tier_total']
df_priced = df_priced.merge(tier_daily, on=['date', 'cap_tier'])
df_priced['within_tier_share'] = df_priced['count'] / df_priced['tier_total'].replace(0, np.nan)
df_priced['within_tier_share'] = df_priced['within_tier_share'].clip(lower=1e-10)
df_priced['log_within_tier_share'] = np.log(df_priced['within_tier_share'])

# Day-demean
demean_vars = ['lhs_berry', 'log_within_tier_share', 'log_context', 'supports_reasoning',
               'supports_tools', 'model_age', 'log_price']
for v in demean_vars:
    df_priced[f'{v}_dm'] = df_priced[v] - df_priced.groupby('day_id')[v].transform('mean')

formula_r4 = 'lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_tier_share_dm'
m_r4 = smf.ols(formula_r4, data=df_priced).fit(
    cov_type='cluster', cov_kwds={'groups': df_priced['model_permaslug']})
sigma_tier = m_r4.params['log_within_tier_share_dm']
sigma_tier_se = m_r4.bse['log_within_tier_share_dm']
print(f"σ (capability tier nesting) = {sigma_tier:.3f} (SE={sigma_tier_se:.3f})")
results.append({
    'Check': '(4) Nest by capability tier',
    'Same-firm [0,7]': f"σ_tier={sigma_tier:.3f}",
    'SE': f"({sigma_tier_se:.3f})",
    'N': int(m_r4.nobs),
    'R²w': f"{m_r4.rsquared:.3f}",
})

# ============================================================
# ROBUSTNESS 5: Alternative nesting — by price tier
# ============================================================
print("\n=== Rob 5: Nested logit by price tier ===")
df_priced['price_tier'] = pd.qcut(df_priced['price_blended'].clip(lower=1e-10),
                                   q=3, labels=['low', 'mid', 'high'], duplicates='drop')
ptier_daily = df_priced.groupby(['date', 'price_tier'])['count'].sum().reset_index()
ptier_daily.columns = ['date', 'price_tier', 'ptier_total']
df_priced = df_priced.merge(ptier_daily, on=['date', 'price_tier'], how='left')
df_priced['within_ptier_share'] = df_priced['count'] / df_priced['ptier_total'].replace(0, np.nan)
df_priced['within_ptier_share'] = df_priced['within_ptier_share'].clip(lower=1e-10)
df_priced['log_within_ptier_share'] = np.log(df_priced['within_ptier_share'])
df_priced['log_within_ptier_share_dm'] = df_priced['log_within_ptier_share'] - \
    df_priced.groupby('day_id')['log_within_ptier_share'].transform('mean')

formula_r5 = 'lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_ptier_share_dm'
m_r5 = smf.ols(formula_r5, data=df_priced.dropna(subset=['log_within_ptier_share_dm'])).fit(
    cov_type='cluster', cov_kwds={'groups': df_priced.dropna(subset=['log_within_ptier_share_dm'])['model_permaslug']})
sigma_ptier = m_r5.params['log_within_ptier_share_dm']
sigma_ptier_se = m_r5.bse['log_within_ptier_share_dm']
print(f"σ (price tier nesting) = {sigma_ptier:.3f} (SE={sigma_ptier_se:.3f})")
results.append({
    'Check': '(5) Nest by price tier',
    'Same-firm [0,7]': f"σ_price={sigma_ptier:.3f}",
    'SE': f"({sigma_ptier_se:.3f})",
    'N': int(m_r5.nobs),
    'R²w': f"{m_r5.rsquared:.3f}",
})

# ============================================================
# ROBUSTNESS 6: 7-day rolling average outcome
# ============================================================
print("\n=== Rob 6: 7-day rolling average ===")
df_sorted = df.sort_values(['model_permaslug', 'date'])
df_sorted['log_requests_7d'] = df_sorted.groupby('model_permaslug')['log_requests'].transform(
    lambda x: x.rolling(7, min_periods=3).mean())
df_r6 = df_sorted.dropna(subset=['log_requests_7d'])
df_r6_panel = df_r6.set_index(['model_permaslug', 'date'])
y_r6 = df_r6_panel['log_requests_7d']
X_r6 = df_r6_panel[['same_firm_entry_0_7']].fillna(0)
m_r6 = PanelOLS(y_r6, X_r6, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
results.append({
    'Check': '(6) 7-day rolling avg DV',
    'Same-firm [0,7]': f"{m_r6.params['same_firm_entry_0_7']:.4f}",
    'SE': f"({m_r6.std_errors['same_firm_entry_0_7']:.4f})",
    'N': m_r6.nobs,
    'R²w': f"{m_r6.rsquared_within:.3f}",
})
print(f"β = {m_r6.params['same_firm_entry_0_7']:.4f} (SE={m_r6.std_errors['same_firm_entry_0_7']:.4f})")

# ============================================================
# ROBUSTNESS 7: Exclude edge days
# ============================================================
print("\n=== Rob 7: Exclude first/last 7 days ===")
df_r7 = df[(df['date'] >= df['date'].min() + pd.Timedelta(days=7)) &
           (df['date'] <= df['date'].max() - pd.Timedelta(days=7))].copy()
df_r7_panel = df_r7.set_index(['model_permaslug', 'date'])
y_r7 = df_r7_panel['log_requests']
X_r7 = df_r7_panel[['same_firm_entry_0_7']].fillna(0)
m_r7 = PanelOLS(y_r7, X_r7, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
results.append({
    'Check': '(7) Exclude first/last 7 days',
    'Same-firm [0,7]': f"{m_r7.params['same_firm_entry_0_7']:.4f}",
    'SE': f"({m_r7.std_errors['same_firm_entry_0_7']:.4f})",
    'N': m_r7.nobs,
    'R²w': f"{m_r7.rsquared_within:.3f}",
})
print(f"β = {m_r7.params['same_firm_entry_0_7']:.4f} (SE={m_r7.std_errors['same_firm_entry_0_7']:.4f})")

# ============================================================
# ROBUSTNESS 8: Placebo — randomize entry dates
# ============================================================
print("\n=== Rob 8: Placebo (randomized entry dates) ===")
np.random.seed(42)
# Shuffle entry dates across firms
firm_dates = df.groupby('model_permaslug')['entry_date'].first().reset_index()
firm_dates['firm'] = firm_dates['model_permaslug'].str.split('/').str[0]
# Randomly reassign firms to entry dates
shuffled_firms = firm_dates['firm'].values.copy()
np.random.shuffle(shuffled_firms)
firm_dates['firm_shuffled'] = shuffled_firms

# Recompute same-firm entry with shuffled firm assignments
df_placebo = df.copy()
df_placebo['firm_shuffled'] = df_placebo['model_permaslug'].map(
    dict(zip(firm_dates['model_permaslug'], firm_dates['firm_shuffled'])))

# Recompute same_firm_entry with shuffled firms
entry_shuffled = firm_dates[['model_permaslug', 'entry_date', 'firm_shuffled']].copy()
date_firm_entries_s = {}
for _, row in entry_shuffled.iterrows():
    d = row['entry_date']
    f = row['firm_shuffled']
    if d not in date_firm_entries_s:
        date_firm_entries_s[d] = {}
    if f not in date_firm_entries_s[d]:
        date_firm_entries_s[d][f] = 0
    date_firm_entries_s[d][f] += 1

unique_placebo = df_placebo[['date', 'firm_shuffled']].drop_duplicates().reset_index(drop=True)
s07_p = np.zeros(len(unique_placebo))
for i, (d, f) in enumerate(zip(unique_placebo['date'].values, unique_placebo['firm_shuffled'].values)):
    for offset in range(0, 8):
        check_date = d - pd.Timedelta(days=offset)
        if check_date in date_firm_entries_s:
            for firm, cnt in date_firm_entries_s[check_date].items():
                if firm == f:
                    s07_p[i] += cnt
unique_placebo['same_firm_entry_0_7_placebo'] = s07_p
df_placebo = df_placebo.merge(unique_placebo, on=['date', 'firm_shuffled'], how='left')

df_p_panel = df_placebo.set_index(['model_permaslug', 'date'])
y_p = df_p_panel['log_requests']
X_p = df_p_panel[['same_firm_entry_0_7_placebo']].fillna(0)
m_p = PanelOLS(y_p, X_p, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
results.append({
    'Check': '(8) Placebo (shuffled firms)',
    'Same-firm [0,7]': f"{m_p.params['same_firm_entry_0_7_placebo']:.4f}",
    'SE': f"({m_p.std_errors['same_firm_entry_0_7_placebo']:.4f})",
    'N': m_p.nobs,
    'R²w': f"{m_p.rsquared_within:.3f}",
})
print(f"Placebo β = {m_p.params['same_firm_entry_0_7_placebo']:.4f} "
      f"(SE={m_p.std_errors['same_firm_entry_0_7_placebo']:.4f})")

# ============================================================
# ROBUSTNESS 9: Coefficient stability (Oster-style)
# ============================================================
print("\n=== Rob 9: Coefficient stability ===")
# Compare σ across specifications with increasing controls
# Short regression: σ only + day FE (demeaned)
df_oster = df_priced.copy()
df_oster['log_within_share_dm'] = df_oster['log_within_share'] - \
    df_oster.groupby('day_id')['log_within_share'].transform('mean')
df_oster['lhs_berry_dm'] = df_oster['lhs_berry'] - \
    df_oster.groupby('day_id')['lhs_berry'].transform('mean')

m_short = smf.ols('lhs_berry_dm ~ log_within_share_dm', data=df_oster).fit()
m_full = smf.ols('lhs_berry_dm ~ log_within_share_dm + log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm',
                  data=df_oster).fit()

sigma_short = m_short.params['log_within_share_dm']
r2_short = m_short.rsquared
sigma_full = m_full.params['log_within_share_dm']
r2_full = m_full.rsquared

# Oster (2019) delta calculation
# delta = (sigma_full * (r2_max - r2_full)) / ((sigma_short - sigma_full) * (r2_full - r2_short))
r2_max = min(1.0, 1.3 * r2_full)  # Common choice: R²_max = 1.3 * R²_full
if abs(sigma_short - sigma_full) > 0.001 and (r2_full - r2_short) > 0:
    delta = (sigma_full * (r2_max - r2_full)) / ((sigma_short - sigma_full) * (r2_full - r2_short))
else:
    delta = np.nan

print(f"Short σ = {sigma_short:.3f} (R² = {r2_short:.3f})")
print(f"Full σ  = {sigma_full:.3f} (R² = {r2_full:.3f})")
print(f"Oster δ = {delta:.2f} (δ > 1 suggests robust to unobservables)")

results.append({
    'Check': f'(9) Oster stability: δ={delta:.2f}',
    'Same-firm [0,7]': f"σ_short={sigma_short:.3f}, σ_full={sigma_full:.3f}",
    'SE': '',
    'N': int(m_full.nobs),
    'R²w': f"R²: {r2_short:.3f}→{r2_full:.3f}",
})

# ============================================================
# ROBUSTNESS 10: Outside option sensitivity
# ============================================================
print("\n=== Rob 10: Outside option sensitivity ===")
# Need to re-demean within-share for this sample
df_priced['log_within_share_dm2'] = df_priced['log_within_share'] - \
    df_priced.groupby('day_id')['log_within_share'].transform('mean')
for outside_pct, label in [(0.1, '10%'), (0.3, '30%'), (0.4, '40%')]:
    df_os = df_priced.copy()
    df_os['market_size_alt'] = df_os['total_inside'] / (1 - outside_pct)
    df_os['share_alt'] = df_os['count'] / df_os['market_size_alt']
    df_os['s0_alt'] = (df_os['market_size_alt'] - df_os['total_inside']) / df_os['market_size_alt']
    df_os['lhs_alt'] = np.log(df_os['share_alt'].clip(1e-10)) - np.log(df_os['s0_alt'].clip(1e-10))
    df_os['lhs_alt_dm'] = df_os['lhs_alt'] - df_os.groupby('day_id')['lhs_alt'].transform('mean')

    m_os = smf.ols('lhs_alt_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_share_dm2',
                    data=df_os).fit(cov_type='cluster', cov_kwds={'groups': df_os['model_permaslug']})
    print(f"Outside={label}: σ = {m_os.params['log_within_share_dm2']:.3f} (SE={m_os.bse['log_within_share_dm2']:.3f})")

# ============================================================
# SAVE RESULTS
# ============================================================
print("\nSaving robustness table...")
rob_table = pd.DataFrame(results)
rob_table.to_csv(OUT_TAB / "table04_robustness.csv", index=False)

# Summary comparison figure
print("Creating robustness comparison figure...")
# Compare σ across nesting structures
sigma_vals = {
    'Firm (baseline)': (0.456, 0.042),
    'Capability tier': (sigma_tier, sigma_tier_se),
    'Price tier': (sigma_ptier, sigma_ptier_se),
}

fig, ax = plt.subplots(figsize=(8, 5))
names = list(sigma_vals.keys())
vals = [v[0] for v in sigma_vals.values()]
errs = [1.96 * v[1] for v in sigma_vals.values()]
ax.barh(range(len(names)), vals, xerr=errs, color=COLORS[:3], alpha=0.8, capsize=5, edgecolor='white')
ax.set_yticks(range(len(names)))
ax.set_yticklabels(names)
ax.set_xlabel('σ (nesting parameter)')
ax.set_title('Figure 13: Nesting Parameter Across Alternative Specifications')
ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=0.5, color='gray', linestyle=':', alpha=0.5, label='σ = 0.5')
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUT_FIG / "fig13_robustness_sigma.png")
plt.close()

print("\n=== Robustness checks complete ===")
