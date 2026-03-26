"""
04_baseline_regression.py
Phase 3b: Baseline regressions — nested logit demand + entry panel + event study.
Uses linearmodels for panel FE and statsmodels for cross-sectional specs.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS
from linearmodels.iv import IV2SLS
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
# LOAD DATA
# ============================================================
print("Loading analysis panel...")
df = pd.read_csv(OUT / "analysis_panel.csv", parse_dates=['date', 'entry_date'])
df['day_id'] = (df['date'] - df['date'].min()).dt.days

# Ensure numeric types
for col in ['supports_reasoning', 'supports_tools', 'supports_image', 'is_free']:
    df[col] = df[col].astype(float)

print(f"Panel: {df.shape[0]} obs, {df['model_permaslug'].nunique()} models")

# ============================================================
# SPECIFICATION 1: NESTED LOGIT DEMAND
# ============================================================
print("\n=== Specification 1: Nested Logit ===")

# Use demeaned approach: absorb day FE by demeaning within day
df_priced = df[df['log_price'].notna() & df['log_context'].notna()].copy()
print(f"Priced sample: {len(df_priced)} obs, {df_priced['model_permaslug'].nunique()} models")

# Day-demean all variables (absorb day FE)
demean_vars = ['lhs_berry', 'log_within_share', 'log_context', 'supports_reasoning',
               'supports_tools', 'model_age', 'log_price']
for v in demean_vars:
    day_mean = df_priced.groupby('day_id')[v].transform('mean')
    df_priced[f'{v}_dm'] = df_priced[v] - day_mean

# Spec 1a: Standard logit (no nesting) — day-demeaned OLS
formula_1a = 'lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm'
model_1a = smf.ols(formula_1a, data=df_priced).fit(
    cov_type='cluster', cov_kwds={'groups': df_priced['model_permaslug']})
print("\nSpec 1a (Logit, demeaned):")
print(model_1a.summary().tables[1])

# Spec 1b: Nested logit OLS
formula_1b = 'lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_share_dm'
model_1b = smf.ols(formula_1b, data=df_priced).fit(
    cov_type='cluster', cov_kwds={'groups': df_priced['model_permaslug']})
sigma_ols = model_1b.params['log_within_share_dm']
sigma_ols_se = model_1b.bse['log_within_share_dm']
print(f"\nSpec 1b (Nested OLS): σ = {sigma_ols:.3f} (SE={sigma_ols_se:.3f})")

# Spec 1c: Nested logit IV — instrument log_within_share with n_own_models, n_rival_models
print("\nSpec 1c (Nested IV)...")
df_iv = df_priced.dropna(subset=['n_own_models', 'n_rival_models']).copy()

# Day-demean instruments too
for v in ['n_own_models', 'n_rival_models']:
    day_mean = df_iv.groupby('day_id')[v].transform('mean')
    df_iv[f'{v}_dm'] = df_iv[v] - day_mean

# First stage
formula_fs = 'log_within_share_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + n_own_models_dm + n_rival_models_dm'
first_stage = smf.ols(formula_fs, data=df_iv).fit()

# Check first-stage F
from statsmodels.stats.diagnostic import linear_harvey_collier
# Manual partial F-test for excluded instruments
formula_fs_restricted = 'log_within_share_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm'
fs_restricted = smf.ols(formula_fs_restricted, data=df_iv).fit()
f_stat = ((fs_restricted.ssr - first_stage.ssr) / 2) / (first_stage.ssr / first_stage.df_resid)
print(f"First-stage partial F = {f_stat:.1f}")

# Predict log_within_share_dm from first stage
df_iv['log_within_share_hat'] = first_stage.fittedvalues

# Second stage
formula_2s = 'lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_share_hat'
model_1c = smf.ols(formula_2s, data=df_iv).fit(
    cov_type='cluster', cov_kwds={'groups': df_iv['model_permaslug']})
sigma_iv = model_1c.params['log_within_share_hat']
sigma_iv_se = model_1c.bse['log_within_share_hat']
print(f"IV σ = {sigma_iv:.3f} (SE={sigma_iv_se:.3f})")
iv_success = True

# ============================================================
# SPECIFICATION 2: ENTRY PANEL REGRESSION (TWFE)
# ============================================================
print("\n=== Specification 2: Entry Panel Regression (TWFE) ===")

df_panel = df.set_index(['model_permaslug', 'date'])
y2 = df_panel['log_requests']

# Note: model_age is absorbed by entity + time FE (linear in both).
# rival_entry varies only by date → absorbed by time FE.
# Same-firm entry varies by firm×date → identified after TWFE.
# Strategy: (A) TWFE with same-firm entry only (rival absorbed by day FE)
#           (B) Entity FE only (no time FE) to also estimate rival effects
#           (C) Both windows, entity FE + week FE (preserves daily variation)

# Spec 2a: TWFE — same-firm entry only (rival entry absorbed by day FE)
X2a = df_panel[['same_firm_entry_0_7']].fillna(0)
model_2a = PanelOLS(y2, X2a, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)
print(f"\nSpec 2a (TWFE): same_firm_entry_0_7 = {model_2a.params['same_firm_entry_0_7']:.4f} "
      f"(SE={model_2a.std_errors['same_firm_entry_0_7']:.4f})")

# Spec 2b: Entity FE + week FE (allows rival entry estimation)
df_panel_temp = df_panel.copy()
df_panel_temp['week_id'] = pd.to_datetime(df_panel_temp.index.get_level_values('date')).isocalendar().week.values
# Construct week dummies manually in X
week_dummies = pd.get_dummies(df_panel_temp['week_id'], prefix='wk', drop_first=True, dtype=float)
X2b_base = df_panel[['same_firm_entry_0_7', 'rival_entry_0_7']].fillna(0)
X2b = pd.concat([X2b_base, week_dummies.set_index(X2b_base.index)], axis=1)
model_2b = PanelOLS(y2, X2b, entity_effects=True, time_effects=False).fit(
    cov_type='clustered', cluster_entity=True)
print(f"Spec 2b (entity+week FE): same_firm = {model_2b.params['same_firm_entry_0_7']:.4f}, "
      f"rival = {model_2b.params['rival_entry_0_7']:.4f}")

# Spec 2c: TWFE with short + medium windows for same-firm
X2c = df_panel[['same_firm_entry_0_7', 'same_firm_entry_8_30']].fillna(0)
model_2c = PanelOLS(y2, X2c, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)

print(f"\nSpec 2c (TWFE short+medium):")
for v in ['same_firm_entry_0_7', 'same_firm_entry_8_30']:
    print(f"  {v}: {model_2c.params[v]:.4f} (SE={model_2c.std_errors[v]:.4f})")

# ============================================================
# SPECIFICATION 3: EVENT STUDY
# ============================================================
print("\n=== Specification 3: Event Study ===")

# Identify top entry events
panel_start = df['date'].min() + pd.Timedelta(days=7)
late_entrants = df[df['entry_date'] > panel_start].groupby('model_permaslug')['count'].sum()
top_entrants = late_entrants.nlargest(10).index.tolist()
print(f"Top 10 entry events: {[e.split('/')[-1][:25] for e in top_entrants]}")

# Same-firm event study
event_study_data = []
for entrant in top_entrants:
    entrant_firm = entrant.split('/')[0]
    entrant_entry = df[df['model_permaslug'] == entrant]['entry_date'].iloc[0]

    incumbents = df[(df['firm'] == entrant_firm) &
                    (df['entry_date'] < entrant_entry) &
                    (df['model_permaslug'] != entrant)]
    for inc in incumbents['model_permaslug'].unique():
        inc_data = df[df['model_permaslug'] == inc].copy()
        inc_data['rel_time'] = (inc_data['date'] - entrant_entry).dt.days
        inc_data = inc_data[(inc_data['rel_time'] >= -14) & (inc_data['rel_time'] <= 30)]
        inc_data['entrant'] = entrant
        inc_data['incumbent'] = inc
        event_study_data.append(inc_data)

if event_study_data:
    es_df = pd.concat(event_study_data, ignore_index=True)
    baseline = es_df[es_df['rel_time'] == -1].groupby('incumbent')['log_requests'].mean()
    es_df = es_df.merge(baseline.rename('baseline_lr'), left_on='incumbent', right_index=True)
    es_df['norm_lr'] = es_df['log_requests'] - es_df['baseline_lr']

    es_avg = es_df.groupby('rel_time').agg(
        mean_effect=('norm_lr', 'mean'),
        se_effect=('norm_lr', lambda x: x.std() / np.sqrt(max(len(x), 1))),
        n_obs=('norm_lr', 'count')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.fill_between(es_avg['rel_time'],
                     es_avg['mean_effect'] - 1.96 * es_avg['se_effect'],
                     es_avg['mean_effect'] + 1.96 * es_avg['se_effect'],
                     alpha=0.2, color=COLORS[0])
    ax.plot(es_avg['rel_time'], es_avg['mean_effect'], color=COLORS[0], linewidth=2,
            marker='o', markersize=4)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color=COLORS[1], linestyle='--', alpha=0.7, label='Entry date')
    ax.set_xlabel('Days Relative to Same-Firm New Model Entry')
    ax.set_ylabel('Log Requests (normalized to t = −1)')
    ax.set_title('Figure 11: Same-Firm Incumbent Response to New Model Entry')
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(OUT_FIG / "fig11_event_study_same_firm.png")
    plt.close()
    es_avg.to_csv(OUT_TAB / "event_study_same_firm.csv", index=False)
    print("Same-firm event study saved.")

# Cross-firm event study
cross_data = []
for entrant in top_entrants[:5]:
    entrant_firm = entrant.split('/')[0]
    entrant_entry = df[df['model_permaslug'] == entrant]['entry_date'].iloc[0]

    rivals = df[(df['firm'] != entrant_firm) & (df['entry_date'] < entrant_entry)]
    top_rivals = rivals.groupby('model_permaslug')['count'].sum().nlargest(10).index

    for rv in top_rivals:
        rv_data = df[df['model_permaslug'] == rv].copy()
        rv_data['rel_time'] = (rv_data['date'] - entrant_entry).dt.days
        rv_data = rv_data[(rv_data['rel_time'] >= -14) & (rv_data['rel_time'] <= 30)]
        rv_data['entrant'] = entrant
        rv_data['incumbent'] = rv
        cross_data.append(rv_data)

if cross_data:
    ce_df = pd.concat(cross_data, ignore_index=True)
    baseline_ce = ce_df[ce_df['rel_time'] == -1].groupby('incumbent')['log_requests'].mean()
    ce_df = ce_df.merge(baseline_ce.rename('baseline_lr'), left_on='incumbent', right_index=True)
    ce_df['norm_lr'] = ce_df['log_requests'] - ce_df['baseline_lr']

    ce_avg = ce_df.groupby('rel_time').agg(
        mean_effect=('norm_lr', 'mean'),
        se_effect=('norm_lr', lambda x: x.std() / np.sqrt(max(len(x), 1))),
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.fill_between(ce_avg['rel_time'],
                     ce_avg['mean_effect'] - 1.96 * ce_avg['se_effect'],
                     ce_avg['mean_effect'] + 1.96 * ce_avg['se_effect'],
                     alpha=0.2, color=COLORS[2])
    ax.plot(ce_avg['rel_time'], ce_avg['mean_effect'], color=COLORS[2], linewidth=2,
            marker='o', markersize=4)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color=COLORS[1], linestyle='--', alpha=0.7, label='Rival entry date')
    ax.set_xlabel('Days Relative to Major Rival Model Entry')
    ax.set_ylabel('Log Requests (normalized to t = −1)')
    ax.set_title('Figure 12: Cross-Firm Response to Major Rival Entry')
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(OUT_FIG / "fig12_event_study_cross_firm.png")
    plt.close()
    ce_avg.to_csv(OUT_TAB / "event_study_cross_firm.csv", index=False)
    print("Cross-firm event study saved.")

# ============================================================
# ECONOMIC SIGNIFICANCE
# ============================================================
print("\n=== Economic Significance ===")

beta_same = model_2c.params['same_firm_entry_0_7']
beta_same_se = model_2c.std_errors['same_firm_entry_0_7']
beta_rival = model_2b.params['rival_entry_0_7']
beta_rival_se = model_2b.std_errors['rival_entry_0_7']
sd_same = df['same_firm_entry_0_7'].std()
sd_rival = df['rival_entry_0_7'].std()

print(f"σ (OLS) = {sigma_ols:.3f} (SE={sigma_ols_se:.3f})")
print(f"σ (IV)  = {sigma_iv:.3f} (SE={sigma_iv_se:.3f})")
print(f"First-stage F = {f_stat:.1f}")
print(f"\nSame-firm entry [0,7]: β = {beta_same:.4f} (SE={beta_same_se:.4f})")
print(f"  SD of same_firm_entry = {sd_same:.3f}")
print(f"  1-SD effect: {beta_same * sd_same:.4f} → {(np.exp(beta_same * sd_same)-1)*100:.1f}%")
print(f"\nRival entry [0,7]: β = {beta_rival:.6f} (SE={beta_rival_se:.6f})")
print(f"  SD of rival_entry = {sd_rival:.3f}")
print(f"  1-SD effect: {beta_rival * sd_rival:.4f} → {(np.exp(beta_rival * sd_rival)-1)*100:.1f}%")

# Market expansion: total market around top entries
print("\n=== Market Expansion Around Entry Events ===")
daily_total = df.groupby('date')['count'].sum().reset_index()
daily_total.columns = ['date', 'total_requests']

for entrant in top_entrants[:5]:
    entry_d = df[df['model_permaslug'] == entrant]['entry_date'].iloc[0]
    pre = daily_total[(daily_total['date'] >= entry_d - pd.Timedelta(days=7)) &
                      (daily_total['date'] < entry_d)]['total_requests'].mean()
    post = daily_total[(daily_total['date'] >= entry_d) &
                       (daily_total['date'] < entry_d + pd.Timedelta(days=7))]['total_requests'].mean()
    change = (post / pre - 1) * 100 if pre > 0 else np.nan
    print(f"  {entrant.split('/')[-1][:30]}: pre={pre/1e6:.1f}M → post={post/1e6:.1f}M ({change:+.1f}%)")

# ============================================================
# SAVE ALL RESULTS
# ============================================================
print("\nSaving tables...")

# Table 2: Nested Logit
rows = []
for v, label in [('log_context_dm', 'Log context length'),
                  ('supports_reasoning_dm', 'Reasoning capability'),
                  ('supports_tools_dm', 'Tool call support'),
                  ('model_age_dm', 'Model age (days)'),
                  ('log_price_dm', 'Log price')]:
    row = {'Variable': label}
    row['(1) Logit'] = f"{model_1a.params.get(v, np.nan):.4f}"
    row['(1) SE'] = f"({model_1a.bse.get(v, np.nan):.4f})"
    row['(2) NL-OLS'] = f"{model_1b.params.get(v, np.nan):.4f}"
    row['(2) SE'] = f"({model_1b.bse.get(v, np.nan):.4f})"
    v_iv = v.replace('_dm', '_dm') if v != 'log_within_share_dm' else 'log_within_share_hat'
    row['(3) NL-IV'] = f"{model_1c.params.get(v, np.nan):.4f}"
    row['(3) SE'] = f"({model_1c.bse.get(v, np.nan):.4f})"
    rows.append(row)

# σ row
rows.append({
    'Variable': 'σ (nesting parameter)',
    '(1) Logit': '—',
    '(1) SE': '',
    '(2) NL-OLS': f"{sigma_ols:.4f}",
    '(2) SE': f"({sigma_ols_se:.4f})",
    '(3) NL-IV': f"{sigma_iv:.4f}",
    '(3) SE': f"({sigma_iv_se:.4f})",
})

# Footer rows
rows.append({'Variable': 'N', '(1) Logit': str(int(model_1a.nobs)),
             '(1) SE': '', '(2) NL-OLS': str(int(model_1b.nobs)),
             '(2) SE': '', '(3) NL-IV': str(int(model_1c.nobs)), '(3) SE': ''})
rows.append({'Variable': 'R²', '(1) Logit': f"{model_1a.rsquared:.3f}",
             '(1) SE': '', '(2) NL-OLS': f"{model_1b.rsquared:.3f}",
             '(2) SE': '', '(3) NL-IV': '', '(3) SE': ''})
rows.append({'Variable': 'Day FE', '(1) Logit': 'Yes', '(1) SE': '',
             '(2) NL-OLS': 'Yes', '(2) SE': '', '(3) NL-IV': 'Yes', '(3) SE': ''})
rows.append({'Variable': 'First-stage F', '(1) Logit': '', '(1) SE': '',
             '(2) NL-OLS': '', '(2) SE': '', '(3) NL-IV': f"{f_stat:.1f}", '(3) SE': ''})

table2 = pd.DataFrame(rows)
table2.to_csv(OUT_TAB / "table02_nested_logit.csv", index=False)

# Table 3: Entry Panel
rows3 = []
for v, label in [('same_firm_entry_0_7', 'Same-firm entry [0,7]'),
                  ('same_firm_entry_8_30', 'Same-firm entry [8,30]'),
                  ('rival_entry_0_7', 'Rival entry [0,7]')]:
    row = {'Variable': label}
    for spec_name, model in [('(1)', model_2a), ('(2)', model_2b), ('(3)', model_2c)]:
        if v in model.params.index:
            row[f'{spec_name} Coef'] = f"{model.params[v]:.4f}"
            row[f'{spec_name} SE'] = f"({model.std_errors[v]:.4f})"
        else:
            row[f'{spec_name} Coef'] = ''
            row[f'{spec_name} SE'] = ''
    rows3.append(row)

for label, val_fn in [('N', lambda m: str(m.nobs)),
                       ('R² (within)', lambda m: f"{m.rsquared_within:.3f}"),
                       ('Model FE', lambda m: 'Yes'),
                       ('Day FE', lambda m: 'Yes'),
                       ('Clustering', lambda m: 'Model')]:
    row = {'Variable': label}
    for spec_name, model in [('(1)', model_2a), ('(2)', model_2b), ('(3)', model_2c)]:
        row[f'{spec_name} Coef'] = val_fn(model)
        row[f'{spec_name} SE'] = ''
    rows3.append(row)

table3 = pd.DataFrame(rows3)
table3.to_csv(OUT_TAB / "table03_entry_panel.csv", index=False)

# Save economic significance
econ = {
    'sigma_ols': sigma_ols, 'sigma_ols_se': sigma_ols_se,
    'sigma_iv': sigma_iv, 'sigma_iv_se': sigma_iv_se,
    'first_stage_f': f_stat,
    'beta_same_0_7': beta_same, 'beta_same_0_7_se': beta_same_se,
    'beta_rival_0_7': beta_rival, 'beta_rival_0_7_se': beta_rival_se,
    'sd_same': sd_same, 'sd_rival': sd_rival,
    'one_sd_same_pct': (np.exp(beta_same * sd_same) - 1) * 100,
    'one_sd_rival_pct': (np.exp(beta_rival * sd_rival) - 1) * 100,
    'n_obs_panel': int(model_2c.nobs), 'n_models': df['model_permaslug'].nunique(),
}
pd.Series(econ).to_csv(OUT_TAB / "economic_significance.csv")

print("\n=== Baseline regressions complete ===")
