# Pre-Analysis Plan

## Date: 2026-03-25
## Project: Creative Destruction in the Market for Intelligence

---

## 1. Main Regression Equations

### Specification 1: Nested Logit Demand (Primary)

$$\ln(s_{mt}) - \ln(s_{0t}) = \beta_1 \ln(\text{context\_length}_m) + \beta_2 \text{reasoning}_m + \beta_3 \text{tool\_calls}_m + \beta_4 \text{age}_{mt} + \beta_5 \text{age}_{mt}^2 - \alpha \cdot p_m + \sigma \ln(s_{m|g,t}) + \delta_t + \xi_{mt}$$

where:
- $s_{mt}$: model $m$'s share of total requests on day $t$
- $s_{0t}$: outside option share on day $t$
- $s_{m|g,t}$: model $m$'s share within firm $g$ on day $t$
- $\sigma$: nesting parameter (key parameter of interest)
- $\delta_t$: day fixed effects
- $p_m$: average per-token price (input + output weighted)

### Specification 2: Entry Event Panel Regression (Descriptive)

$$\ln(D_{mt}) = \alpha_m + \delta_t + \beta_1 \cdot \text{SameFirmEntry}_{mt}^{[0,7]} + \beta_2 \cdot \text{SameFirmEntry}_{mt}^{[8,30]} + \beta_3 \cdot \text{RivalEntry}_{mt}^{[0,7]} + \beta_4 \cdot \text{RivalEntry}_{mt}^{[8,30]} + \gamma \cdot \text{ModelAge}_{mt} + \varepsilon_{mt}$$

### Specification 3: Event Study (Descriptive)

$$\ln(D_{mt}) = \alpha_m + \delta_t + \sum_{k=-14}^{30} \beta_k^{own} \cdot \mathbb{1}[\text{SameFirmEntry at } t-k] + \sum_{k=-14}^{30} \beta_k^{rival} \cdot \mathbb{1}[\text{RivalEntry at } t-k] + \varepsilon_{mt}$$

---

## 2. Variable Definitions

### Dependent Variables
| Variable | Definition | Construction | Source |
|----------|-----------|--------------|--------|
| $\ln(D_{mt})$ | Log daily requests | $\ln(\text{count}_{mt} + 1)$ | usage_daily.csv |
| $s_{mt}$ | Market share | $\text{count}_{mt} / \sum_m \text{count}_{mt}$ | usage_daily.csv |
| $\ln(s_{mt}) - \ln(s_{0t})$ | Log share ratio | Berry inversion LHS | Computed |

### Core Independent Variables
| Variable | Definition | Source of variation |
|----------|-----------|-------------------|
| $\ln(s_{m|g,t})$ | Within-firm share | Cross-sectional + time variation |
| SameFirmEntry | # new models from same firm in window | Entry events |
| RivalEntry | # new models from rival firms in window | Entry events |
| $p_m$ | Per-token price | Model metadata (time-invariant) |

### Control Variables
| Variable | Inclusion rationale |
|----------|-------------------|
| $\ln(\text{context\_length})$ | Captures model capability / vertical quality dimension |
| $\text{reasoning}_m$ | Binary: model produces reasoning tokens. Captures capability differentiation |
| $\text{tool\_calls}_m$ | Binary: model supports tool calling. Captures horizontal differentiation |
| $\text{age}_{mt}$ | Days since model first appeared. Captures lifecycle effects |
| $\text{age}_{mt}^2$ | Quadratic age term for non-linear lifecycle |
| Day FE ($\delta_t$) | Absorbs aggregate demand shocks, day-of-week, trends |
| Model FE ($\alpha_m$) | Absorbs time-invariant model characteristics (in panel specs) |

### Fixed Effects
| Specification | FE structure | Rationale |
|--------------|-------------|-----------|
| Nested logit | Day FE only | Cross-sectional model variation needed for β estimation |
| Panel regression | Model + Day FE | Within-model variation over time |
| Event study | Model + Day FE | Within-model variation over time |

### Clustering
- **Primary**: Cluster standard errors at **model level** (unit of observation persistence)
- **Rationale**: Serial correlation within a model's time series. 389 clusters — sufficient for cluster-robust inference.
- **Robustness**: Two-way clustering by model × week (to account for cross-model correlation within weeks)

---

## 3. Sample Construction

1. Start with full panel: 29,084 obs (389 models × ~75 avg days)
2. **Exclude same-day data** (potentially incomplete per data quality report)
3. **Filter**: Keep models with ≥ 1,000 total requests over the sample (removes extremely low-volume noise)
4. **Define outside option**: Total daily market size from weekly top_models data, interpolated to daily
5. **Entry events**: Model's first appearance date in the panel. Major events defined as models reaching top-50 by total requests within 7 days of entry.

---

## 4. Expected Results

### Nesting parameter σ
- **Expected**: σ ∈ [0.3, 0.7]
- **Interpretation**: σ > 0.5 means within-firm substitution dominates cross-firm → cannibalization > displacement
- **If σ ≈ 0**: Models are essentially independent products (unlikely given data patterns)
- **If σ ≈ 1**: Extreme within-firm substitution, new model fully replaces old (possible for same-family upgrades)

### Entry effects (H1: Cannibalization)
- **Expected sign**: β₁ (SameFirmEntry) < 0
- **Expected magnitude**: 10-30% decline in same-firm incumbent usage within 7 days
- **Economic reasoning**: Same-firm models share API infrastructure, brand trust, pricing tiers → easy switching

### Entry effects (H2: Cross-firm displacement)
- **Expected sign**: β₃ (RivalEntry) < 0 but smaller than β₁
- **Expected magnitude**: 2-10% decline in rival model usage
- **If null**: Would suggest market is expanding faster than displacing → positive for competition

### Market expansion (H3)
- **Expected**: Total market grows around entry events, especially for novel-capability models
- **If not found**: Would suggest LLM market is a fixed pie being redistributed → concerning for competition

### If results deviate from expectations:
- Null cannibalization → models within firm may serve different niches (horizontal not vertical differentiation)
- Large cross-firm displacement → market more competitive than expected, lower switching costs
- No market expansion → demand saturation, mature market dynamics

---

## 5. Robustness Checks (≥ 5)

| # | Check | Tests which threat | Description |
|---|-------|-------------------|-------------|
| 1 | Alternative DV: log tokens instead of log requests | DV definition sensitivity | Tokens capture intensity differently from count |
| 2 | Alternative DV: market share instead of log level | Market expansion confounding | Share normalizes by daily total |
| 3 | Restrict to high-volume models (>10K daily avg) | Data quality / measurement error | Per data quality report, these are most stable |
| 4 | Alternative nesting: by capability tier | Nesting misspecification | Nest by reasoning/non-reasoning instead of by firm |
| 5 | Alternative nesting: by price tier | Nesting misspecification | Nest by price quartile instead of by firm |
| 6 | 7-day rolling average outcomes | Daily noise | Smooths day-level fluctuations |
| 7 | Exclude first/last 7 days of panel | Edge effects | Panel boundaries may have incomplete data |
| 8 | Placebo: randomize entry dates | Pre-trend / spurious correlation | If results persist with random dates → spurious |
| 9 | Oster (2019) coefficient stability bounds | Omitted variable bias | Assess sensitivity to unobservables |
| 10 | Two-way clustered SEs (model × week) | Inference robustness | Cross-model correlation within weeks |

---

## 6. Heterogeneity Analysis (≥ 3 dimensions)

| Dimension | Subgroups | Motivation |
|-----------|----------|-----------|
| 1. Entry type | Same-family upgrade vs. new product line | Arrow's replacement effect: upgrades should cannibalize more |
| 2. Model capability | Reasoning vs. non-reasoning models | Novel capabilities may expand market more |
| 3. Firm size | Top-5 firms vs. smaller firms | Large firms may face more cannibalization (larger portfolio) |
| 4. Model age | Young (<30 days) vs. mature (>30 days) incumbent | Newer models may be more vulnerable to displacement |

---
