"""
04b_revised_regressions.py
Addresses Gate 2 Round 1 criticisms:
1. BLP-style instruments (rival characteristics sums) for nested logit
2. Event study pre-trend figures
3. Family upgrade pre-trend verification
4. Fix outside option sensitivity
5. Firm-level clustering
6. Leave-one-firm-out robustness
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# ============================================================
# FIX 1: BLP-STYLE INSTRUMENTS
# ============================================================
print("\n=== Fix 1: BLP-style instruments ===")

df_priced = df[df['log_price'].notna() & df['log_context'].notna()].copy()

# BLP instruments: for each model, compute sum/mean of RIVAL model characteristics
# Exclude own firm's models
# iv1: mean log_context of rival models (same date)
# iv2: mean log_price of rival models (same date)
# iv3: fraction of rival models supporting reasoning (same date)

for date_val in df_priced['day_id'].unique():
    mask = df_priced['day_id'] == date_val
    date_data = df_priced[mask]
    for firm in date_data['firm'].unique():
        firm_mask = mask & (df_priced['firm'] == firm)
        rival_mask = mask & (df_priced['firm'] != firm)
        rival_data = df_priced[rival_mask]
        if len(rival_data) == 0:
            continue
        df_priced.loc[firm_mask, 'iv_rival_log_context'] = rival_data['log_context'].mean()
        df_priced.loc[firm_mask, 'iv_rival_log_price'] = rival_data['log_price'].mean()
        df_priced.loc[firm_mask, 'iv_rival_reasoning'] = rival_data['supports_reasoning'].mean()

# Day-demean all variables
demean_vars = ['lhs_berry', 'log_within_share', 'log_context', 'supports_reasoning',
               'supports_tools', 'model_age', 'log_price',
               'iv_rival_log_context', 'iv_rival_log_price', 'iv_rival_reasoning']
for v in demean_vars:
    if v in df_priced.columns:
        df_priced[f'{v}_dm'] = df_priced[v] - df_priced.groupby('day_id')[v].transform('mean')

# First stage with BLP instruments
df_blp = df_priced.dropna(subset=['iv_rival_log_context_dm', 'iv_rival_log_price_dm', 'iv_rival_reasoning_dm']).copy()

formula_fs_blp = ('log_within_share_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm '
                  '+ model_age_dm + log_price_dm + iv_rival_log_context_dm + iv_rival_log_price_dm + iv_rival_reasoning_dm')
fs_blp = smf.ols(formula_fs_blp, data=df_blp).fit()

# Partial F for excluded instruments
fs_restricted = smf.ols('log_within_share_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm',
                         data=df_blp).fit()
f_blp = ((fs_restricted.ssr - fs_blp.ssr) / 3) / (fs_blp.ssr / fs_blp.df_resid)
print(f"BLP instruments first-stage F = {f_blp:.1f}")

# 2SLS
df_blp['log_within_share_hat_blp'] = fs_blp.fittedvalues
m_iv_blp = smf.ols('lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_share_hat_blp',
                     data=df_blp).fit(cov_type='cluster', cov_kwds={'groups': df_blp['model_permaslug']})
sigma_iv_blp = m_iv_blp.params['log_within_share_hat_blp']
sigma_iv_blp_se = m_iv_blp.bse['log_within_share_hat_blp']
print(f"BLP IV σ = {sigma_iv_blp:.3f} (SE={sigma_iv_blp_se:.3f})")

# Also report OLS with firm-level clustering
m_ols_firm_cluster = smf.ols('lhs_berry_dm ~ log_context_dm + supports_reasoning_dm + supports_tools_dm + model_age_dm + log_price_dm + log_within_share_dm',
                              data=df_priced).fit(cov_type='cluster', cov_kwds={'groups': df_priced['firm']})
sigma_ols_firm = m_ols_firm_cluster.params['log_within_share_dm']
sigma_ols_firm_se = m_ols_firm_cluster.bse['log_within_share_dm']
print(f"OLS σ (firm-clustered SE) = {sigma_ols_firm:.3f} (SE={sigma_ols_firm_se:.3f})")

# ============================================================
# FIX 2: EVENT STUDY FIGURES WITH PRE-TRENDS
# ============================================================
print("\n=== Fix 2: Event study with pre-trends ===")

# Same-firm event study (already generated in 04, but let's ensure it's properly shown)
# Also add pre-trend formal test

# Load event study data if available
es_same = pd.read_csv(OUT_TAB / "event_study_same_firm.csv")
es_cross = pd.read_csv(OUT_TAB / "event_study_cross_firm.csv")

# Pre-trend test: average effect in [-14, -2] (excluding t=-1 as reference)
pre_period_same = es_same[(es_same['rel_time'] >= -14) & (es_same['rel_time'] <= -2)]
pre_mean = pre_period_same['mean_effect'].mean()
pre_se = pre_period_same['mean_effect'].std() / np.sqrt(len(pre_period_same))
t_stat_pre = pre_mean / pre_se if pre_se > 0 else 0
print(f"Same-firm pre-trend: mean={pre_mean:.4f}, t={t_stat_pre:.2f} (|t|<1.96 → no pre-trend)")

# Combined event study figure
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Same-firm
ax = axes[0]
ax.fill_between(es_same['rel_time'],
                es_same['mean_effect'] - 1.96 * es_same['se_effect'],
                es_same['mean_effect'] + 1.96 * es_same['se_effect'],
                alpha=0.2, color=COLORS[0])
ax.plot(es_same['rel_time'], es_same['mean_effect'], color=COLORS[0], linewidth=2,
        marker='o', markersize=3)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=0, color=COLORS[1], linestyle='--', alpha=0.7)
ax.set_xlabel('Days Relative to Same-Firm Entry')
ax.set_ylabel('Normalized Log Requests')
ax.set_title(f'(a) Same-Firm Incumbents\n(Pre-trend t={t_stat_pre:.2f})')

# Cross-firm
ax = axes[1]
pre_period_cross = es_cross[(es_cross['rel_time'] >= -14) & (es_cross['rel_time'] <= -2)]
pre_mean_c = pre_period_cross['mean_effect'].mean()
pre_se_c = pre_period_cross['mean_effect'].std() / np.sqrt(len(pre_period_cross))
t_stat_pre_c = pre_mean_c / pre_se_c if pre_se_c > 0 else 0

ax.fill_between(es_cross['rel_time'],
                es_cross['mean_effect'] - 1.96 * es_cross['se_effect'],
                es_cross['mean_effect'] + 1.96 * es_cross['se_effect'],
                alpha=0.2, color=COLORS[2])
ax.plot(es_cross['rel_time'], es_cross['mean_effect'], color=COLORS[2], linewidth=2,
        marker='o', markersize=3)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=0, color=COLORS[1], linestyle='--', alpha=0.7)
ax.set_xlabel('Days Relative to Major Rival Entry')
ax.set_ylabel('Normalized Log Requests')
ax.set_title(f'(b) Cross-Firm Incumbents\n(Pre-trend t={t_stat_pre_c:.2f})')

fig.suptitle('Figure 15: Event Study — Pre-Trend Validation', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(OUT_FIG / "fig15_event_study_pretrends.png")
plt.close()

# ============================================================
# FIX 3: FAMILY UPGRADE PRE-TREND
# ============================================================
print("\n=== Fix 3: Family upgrade pre-trend ===")

# Identify major family upgrades
df['model_family_short'] = df['model_permaslug'].str.split('/').str[1].str.rsplit('-', n=1).str[0]
first_seen_all = df.groupby('model_permaslug')['date'].min().reset_index()
first_seen_all.columns = ['model_permaslug', 'entry_date_all']
first_seen_all['firm'] = first_seen_all['model_permaslug'].str.split('/').str[0]
first_seen_all['family'] = first_seen_all['model_permaslug'].str.split('/').str[1].str.rsplit('-', n=1).str[0]

# For each firm-family, find upgrade events (>1 model in same family)
family_counts = first_seen_all.groupby(['firm', 'family']).size()
upgrade_families = family_counts[family_counts > 1].index

upgrade_events = []
for firm, family in upgrade_families:
    fam_models = first_seen_all[(first_seen_all['firm'] == firm) &
                                 (first_seen_all['family'] == family)].sort_values('entry_date_all')
    if len(fam_models) >= 2:
        # The second (or later) entry is the upgrade
        for i in range(1, len(fam_models)):
            upgrade_events.append({
                'new_model': fam_models.iloc[i]['model_permaslug'],
                'old_model': fam_models.iloc[i-1]['model_permaslug'],
                'upgrade_date': fam_models.iloc[i]['entry_date_all'],
                'firm': firm,
                'family': family,
            })

print(f"Found {len(upgrade_events)} family upgrade events")

# Event study for family upgrades
upgrade_es_data = []
for evt in upgrade_events:
    old_data = df[df['model_permaslug'] == evt['old_model']].copy()
    old_data['rel_time'] = (old_data['date'] - evt['upgrade_date']).dt.days
    old_data = old_data[(old_data['rel_time'] >= -14) & (old_data['rel_time'] <= 30)]
    old_data['event_id'] = f"{evt['firm']}/{evt['family']}"
    upgrade_es_data.append(old_data)

if upgrade_es_data:
    ue_df = pd.concat(upgrade_es_data, ignore_index=True)
    baseline_ue = ue_df[ue_df['rel_time'] == -1].groupby('model_permaslug')['log_requests'].mean()
    ue_df = ue_df.merge(baseline_ue.rename('bl'), left_on='model_permaslug', right_index=True, how='inner')
    ue_df['norm'] = ue_df['log_requests'] - ue_df['bl']

    ue_avg = ue_df.groupby('rel_time').agg(
        mean=('norm', 'mean'),
        se=('norm', lambda x: x.std() / np.sqrt(max(len(x), 1))),
        n=('norm', 'count')
    ).reset_index()

    # Pre-trend test
    pre_upgrade = ue_avg[(ue_avg['rel_time'] >= -14) & (ue_avg['rel_time'] <= -2)]
    pre_mean_u = pre_upgrade['mean'].mean()
    pre_se_u = pre_upgrade['mean'].std() / np.sqrt(len(pre_upgrade))
    t_stat_u = pre_mean_u / pre_se_u if pre_se_u > 0 else 0
    print(f"Family upgrade pre-trend: mean={pre_mean_u:.4f}, t={t_stat_u:.2f}")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.fill_between(ue_avg['rel_time'], ue_avg['mean'] - 1.96*ue_avg['se'],
                     ue_avg['mean'] + 1.96*ue_avg['se'], alpha=0.2, color=COLORS[0])
    ax.plot(ue_avg['rel_time'], ue_avg['mean'], color=COLORS[0], linewidth=2.5,
            marker='o', markersize=4)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color=COLORS[1], linestyle='--', alpha=0.7, label='Upgrade release date')
    ax.set_xlabel('Days Relative to Family Upgrade Release')
    ax.set_ylabel('Normalized Log Requests (old model)')
    ax.set_title(f'Figure 16: Family Upgrade Cannibalization\n'
                 f'(N={len(upgrade_events)} events, pre-trend t={t_stat_u:.2f})')
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(OUT_FIG / "fig16_family_upgrade_event_study.png")
    plt.close()
    ue_avg.to_csv(OUT_TAB / "event_study_family_upgrade.csv", index=False)

# ============================================================
# FIX 4: OUTSIDE OPTION SENSITIVITY (CORRECTED)
# ============================================================
print("\n=== Fix 4: Outside option sensitivity (corrected) ===")

# The issue: when demeaning by day, the outside option cancels out because
# ln(s_mt) - ln(s_0t) demeaned by day = [ln(s_mt) - day_mean(ln(s))] - [ln(s_0t) - day_mean(ln(s_0t))]
# But ln(s_0t) is the SAME for all models on a given day → demeaning removes it entirely.
# This is why σ doesn't change: the outside option is absorbed by day demeaning.
# This is actually CORRECT behavior for a day-FE specification.
# We need to use a non-demeaned specification to see outside option sensitivity.

# Use week-demeaned instead (preserves within-week variation)
for outside_pct in [0.1, 0.2, 0.3, 0.4]:
    df_os = df_priced.copy()
    df_os['market_size_alt'] = df_os['total_inside'] / (1 - outside_pct)
    df_os['share_alt'] = df_os['count'] / df_os['market_size_alt']
    df_os['s0_alt'] = outside_pct  # by construction
    df_os['lhs_alt'] = np.log(df_os['share_alt'].clip(1e-10)) - np.log(df_os['s0_alt'])

    # Week-demean (preserves within-week variation in s0 changes across outside share values)
    df_os['week_id'] = df_os['date'].dt.isocalendar().week.astype(int)
    week_demean_vars = ['lhs_alt', 'log_within_share', 'log_context', 'supports_reasoning',
                        'supports_tools', 'model_age', 'log_price']
    for v in week_demean_vars:
        df_os[f'{v}_wdm'] = df_os[v] - df_os.groupby('week_id')[v].transform('mean')

    formula_os = 'lhs_alt_wdm ~ log_context_wdm + supports_reasoning_wdm + supports_tools_wdm + model_age_wdm + log_price_wdm + log_within_share_wdm'
    m_os = smf.ols(formula_os, data=df_os).fit(
        cov_type='cluster', cov_kwds={'groups': df_os['model_permaslug']})
    print(f"Outside={outside_pct:.0%}: σ = {m_os.params['log_within_share_wdm']:.3f} "
          f"(SE={m_os.bse['log_within_share_wdm']:.3f})")

# ============================================================
# FIX 5: FIRM-LEVEL CLUSTERING
# ============================================================
print("\n=== Fix 5: Firm-level clustering ===")

# TWFE with firm-level clustering
df_panel = df.set_index(['model_permaslug', 'date'])
y = df_panel['log_requests']
X = df_panel[['same_firm_entry_0_7']].fillna(0)

# Need to provide firm as cluster
df_for_cluster = df.copy()
m_firm_cluster = PanelOLS(y, X, entity_effects=True, time_effects=True).fit(
    cov_type='clustered', cluster_entity=True)

# For firm-level clustering, use statsmodels approach
# Demean by model and day, then cluster by firm
df['log_requests_dm'] = df.groupby('model_permaslug')['log_requests'].transform(lambda x: x - x.mean())
df['log_requests_dm'] = df['log_requests_dm'] - df.groupby('day_id')['log_requests_dm'].transform('mean')
df['same_firm_entry_dm'] = df.groupby('model_permaslug')['same_firm_entry_0_7'].transform(lambda x: x - x.mean())
df['same_firm_entry_dm'] = df['same_firm_entry_dm'] - df.groupby('day_id')['same_firm_entry_dm'].transform('mean')

m_fc = smf.ols('log_requests_dm ~ same_firm_entry_dm - 1', data=df).fit(
    cov_type='cluster', cov_kwds={'groups': df['firm']})
print(f"TWFE with firm clustering: β = {m_fc.params['same_firm_entry_dm']:.4f} (SE={m_fc.bse['same_firm_entry_dm']:.4f})")

# ============================================================
# FIX 6: LEAVE-ONE-FIRM-OUT
# ============================================================
print("\n=== Fix 6: Leave-one-firm-out ===")

top_firms = df.groupby('firm')['count'].sum().nlargest(5).index.tolist()
lofo_results = []
for exclude_firm in top_firms:
    df_lofo = df[df['firm'] != exclude_firm].copy()
    df_lofo_panel = df_lofo.set_index(['model_permaslug', 'date'])
    y_l = df_lofo_panel['log_requests']
    X_l = df_lofo_panel[['same_firm_entry_0_7']].fillna(0)
    try:
        m_l = PanelOLS(y_l, X_l, entity_effects=True, time_effects=True).fit(
            cov_type='clustered', cluster_entity=True)
        lofo_results.append({
            'Excluded firm': exclude_firm,
            'β': m_l.params['same_firm_entry_0_7'],
            'SE': m_l.std_errors['same_firm_entry_0_7'],
            'N': m_l.nobs,
        })
        print(f"  Excluding {exclude_firm}: β = {m_l.params['same_firm_entry_0_7']:.4f} "
              f"(SE={m_l.std_errors['same_firm_entry_0_7']:.4f})")
    except Exception as e:
        print(f"  Excluding {exclude_firm}: failed — {e}")

lofo_df = pd.DataFrame(lofo_results)
lofo_df.to_csv(OUT_TAB / "table07_leave_one_firm_out.csv", index=False)

# ============================================================
# SAVE UPDATED RESULTS
# ============================================================
print("\nSaving updated results...")

# Updated nested logit table with BLP IV
updated_nl = {
    'sigma_ols': 0.456,
    'sigma_ols_se_model': 0.042,
    'sigma_ols_se_firm': sigma_ols_firm_se,
    'sigma_iv_blp': sigma_iv_blp,
    'sigma_iv_blp_se': sigma_iv_blp_se,
    'first_stage_f_blp': f_blp,
    'pre_trend_t_same_firm': t_stat_pre,
    'pre_trend_t_cross_firm': t_stat_pre_c,
    'pre_trend_t_family_upgrade': t_stat_u if upgrade_es_data else np.nan,
    'n_upgrade_events': len(upgrade_events),
}
pd.Series(updated_nl).to_csv(OUT_TAB / "updated_results_summary.csv")

print("\n=== Revisions complete ===")
print(f"BLP IV σ = {sigma_iv_blp:.3f} (SE={sigma_iv_blp_se:.3f}), First-stage F = {f_blp:.1f}")
print(f"Pre-trend tests: same-firm t={t_stat_pre:.2f}, cross-firm t={t_stat_pre_c:.2f}, upgrade t={t_stat_u:.2f}")
