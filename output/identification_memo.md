# Identification Memo (Revised R1)

## Research Question
When a firm releases a new LLM on OpenRouter, what fraction of demand shifts come from intra-firm cannibalization, cross-firm displacement, and market expansion?

## Causal Mechanism
A new model's entry shifts the choice set available to consumers. Because models within the same firm are closer substitutes (shared API conventions, brand trust, pricing tiers), we expect intra-firm cannibalization to dominate. Cross-firm displacement depends on quality proximity. Market expansion occurs when new capabilities attract previously unserved demand.

## Core Regression Equation

### Baseline (model-level panel):
$$\ln(D_{mt}) = \alpha_m + \delta_t + \beta_1 \cdot \text{SameFirmEntry}_{mt} + \beta_2 \cdot \text{CrossFirmEntry}_{mt} + \mathbf{X}_{mt}'\gamma + \varepsilon_{mt}$$

where:
- $D_{mt}$: daily requests for model $m$ on day $t$
- $\alpha_m$: model fixed effects (absorb time-invariant model characteristics)
- $\delta_t$: day fixed effects (absorb market-wide shocks, day-of-week, trends)
- $\text{SameFirmEntry}_{mt}$: number of new models released by model $m$'s firm in a window around $t$
- $\text{CrossFirmEntry}_{mt}$: number of new models released by other firms
- $\mathbf{X}_{mt}$: time-varying controls (e.g., model age in days)

### Event Study Design:
$$\ln(D_{mt}) = \alpha_m + \delta_t + \sum_{k=-14}^{30} \beta_k^{own} \cdot \mathbb{1}[\tau_j^{own} = t - k] + \sum_{k=-14}^{30} \beta_k^{rival} \cdot \mathbb{1}[\tau^{rival} = t - k] + \varepsilon_{mt}$$

where $\tau_j^{own}$ is the date of a new model release by the same firm, and $\tau^{rival}$ is the nearest major competitor release.

## Core Identification Assumption
**Timing exogeneity**: Conditional on model and time fixed effects, the exact date of a new model release is uncorrelated with unobserved demand shocks to incumbent models.

**Justification**: Model development takes months; the exact release date is determined by engineering milestones, not by short-run demand fluctuations for existing models. The TWFE (two-way fixed effects) structure absorbs model-specific demand levels and common time trends.

**What this rules out**: Reverse causality where a decline in existing model demand causes the firm to rush a new release. While firms may respond to competitive pressure, the response time (months of development) is long relative to our daily panel frequency.

## Three Largest Identification Threats

### Threat 1: Correlated demand shocks (confounding)
**Problem**: A technology breakthrough (e.g., better training data, new architecture) could simultaneously cause both the model release AND shifts in demand for existing models.
**Mitigation**:
- Day fixed effects absorb market-wide shocks
- The event study design allows visual inspection of pre-trends — if incumbent model usage was already declining before the new model's release, our estimates may be biased
- Placebo test: use the date of model announcement (if available) vs. actual release

### Threat 2: Heterogeneous treatment effects with staggered adoption
**Problem**: With multiple entry events at different dates, standard TWFE can give biased estimates (de Chaisemartin & D'Haultfœuille, 2020; Goodman-Bacon, 2021).
**Mitigation**:
- Use Sun & Abraham (2021) interaction-weighted estimator as robustness
- Stack the events: create separate event-level datasets and estimate pooled event studies
- Report event-by-event heterogeneity

### Threat 3: Market expansion confounded with time trends
**Problem**: The LLM market is growing rapidly (~20% over our sample), making it hard to distinguish genuine market expansion from new model entry from secular growth.
**Mitigation**:
- Day fixed effects absorb common growth trends
- Compare market-level usage growth in weeks WITH major model releases vs. weeks WITHOUT
- Use model share (not level) as an alternative outcome — this normalizes by market size
- Back-of-envelope: calculate expected growth from trend, then attribute residual to entry

## Positioning (Revised after Gate 1 Round 1)

Given the identification threats — particularly the endogeneity of entry timing — this paper adopts a **dual strategy**:

1. **Structural demand estimation (nested logit)**: Identifies substitution patterns from cross-sectional variation in shares and characteristics. Does NOT require exogenous entry timing. The nesting parameter σ directly measures within-firm vs. cross-firm substitutability.

2. **Descriptive event-study decomposition**: Documents demand reallocation patterns around entry events. Explicitly framed as descriptive, not causal. Complements the structural estimates by showing dynamic adjustment patterns.

We are honest about limitations:
- Event studies are descriptive, not causal
- Nested logit substitution patterns are identified from share variation, not from experiments
- OpenRouter over-represents flexible/multi-homing developers (upper bound on displacement)
- 93-day panel limits long-run conclusions

The contribution is a **well-disciplined descriptive decomposition** of creative destruction in a novel market, not a clean causal estimate.
