# Research Design — LLM API Market Economics (Revised after Gate 1 Round 1)

## Date: 2026-03-25 | Revision: R1

---

## Selected Research Question

**Title**: Creative Destruction in the Market for Intelligence: Demand Reallocation When New LLMs Enter

**Research Question**: When a new LLM enters the market, how is demand reallocated across three channels: intra-firm cannibalization, cross-firm displacement, and market expansion? What model and market characteristics predict the composition of this reallocation?

**Positioning**: This paper provides a **descriptive decomposition** of demand reallocation patterns following model entry events, disciplined by a **nested logit demand model** that estimates substitution patterns from cross-sectional variation in model characteristics and usage shares. We do not claim clean causal identification of entry effects. Instead, we document stylized facts about the speed, magnitude, and composition of creative destruction in a rapidly evolving technology market.

---

## Theoretical Framework (Formalized)

### Nested Logit Demand Model

We model app $i$'s choice of LLM $m$ on day $t$ using a two-level nested logit. Models are nested within firms (groups $g = 1, ..., G$ for each firm), with an outside option (not using OpenRouter / using a model not in our sample).

**Utility**:
$$u_{imt} = \delta_{mt} + \zeta_{ig(m)t} + (1 - \sigma)\varepsilon_{imt}$$

where:
- $\delta_{mt} = \mathbf{x}_{mt}'\beta - \alpha p_m + \xi_{mt}$ is the mean utility of model $m$ on day $t$
- $\mathbf{x}_{mt}$ includes model characteristics (quality proxies, capabilities, age)
- $p_m$ is the per-token price
- $\xi_{mt}$ is the unobserved quality
- $\zeta_{ig(m)t}$ is the nest-level shock (common to all models of the same firm)
- $\sigma \in [0,1)$ is the within-nest correlation (nesting parameter)
- $\varepsilon_{imt}$ is Type-I extreme value

**Market Shares** (Berry, 1994):
$$\ln(s_{mt}) - \ln(s_{0t}) = \mathbf{x}_{mt}'\beta - \alpha p_m + \sigma \ln(s_{m|g,t}) + \xi_{mt}$$

where $s_{mt}$ is model $m$'s market share on day $t$, $s_{0t}$ is the outside option share, and $s_{m|g,t}$ is model $m$'s within-firm (within-nest) share.

**Substitution Patterns**: The nested logit generates richer substitution than logit:
- Within-firm substitution: $\frac{\partial s_{mt}}{\partial \delta_{m't}} \propto \frac{\sigma}{1-\sigma} s_{m'|g,t}$ for $m, m'$ in same firm
- Cross-firm substitution: $\frac{\partial s_{mt}}{\partial \delta_{m't}} \propto s_{m't}$ for $m, m'$ in different firms
- A higher $\sigma$ means more substitution within firms relative to across firms

**Key Advantage**: This structure identifies substitution patterns from **cross-sectional variation** in shares and characteristics, not from exogenous entry timing. The nesting parameter $\sigma$ directly measures the degree to which within-firm models are closer substitutes.

### Decomposition Framework

When new model $m'$ from firm $j$ enters at time $\tau$, we decompose the change in total demand:

1. **Intra-firm cannibalization**: $\Delta D_{jt}^{own} = \sum_{m \in \mathcal{M}_j \setminus \{m'\}} (D_{m,\tau+k} - D_{m,\tau-1})$
2. **Cross-firm displacement**: $\Delta D_{t}^{rival} = \sum_{k \neq j} \sum_{m \in \mathcal{M}_k} (D_{m,\tau+k} - D_{m,\tau-1})$
3. **Market expansion**: $\Delta D_{t}^{total} - \Delta D_{t}^{own} - \Delta D_{t}^{rival} - D_{m',\tau+k}$

The nested logit provides model-implied decompositions via own- and cross-elasticities.

### Testable Hypotheses
- **H1 (Cannibalization dominance)**: Intra-firm cannibalization accounts for a larger share of demand reallocation than cross-firm displacement ($\sigma > 0.5$ in the nested logit, implying within-firm models are closer substitutes)
- **H2 (Quality-dependent displacement)**: Cross-firm displacement is concentrated among quality-adjacent models. We test this by interacting entry effects with quality distance.
- **H3 (Capability-driven expansion)**: Entry of models with novel capabilities (reasoning, tool calling) generates larger market expansion than incremental quality improvements. We test this by comparing decomposition shares across entry types.

---

## Empirical Strategy

### A. Nested Logit Demand Estimation
1. Estimate Berry (1994) nested logit: $\ln(s_{mt}) - \ln(s_{0t}) = \mathbf{x}_{mt}'\beta - \alpha p_m + \sigma \ln(s_{m|g,t}) + \xi_{mt}$
2. Include model characteristics: context length (log), supports_reasoning dummy, supports_tool_calls dummy, model age (days since release), firm dummies
3. Price: input + output token prices (from model metadata)
4. Outside option: total OpenRouter traffic estimated from top_models weekly data minus observed model traffic
5. Endogeneity of $\ln(s_{m|g,t})$: instrument with number of competing models in the same firm (BLP-style)
6. Day fixed effects to absorb time-varying market size

### B. Event Study (Descriptive, Not Causal)
1. Identify all model entry events (first appearance in panel)
2. For each entry event, track usage of same-firm and competitor models in [-14, +30] day window
3. Compute raw demand reallocation decomposition (three channels)
4. Report event-by-event heterogeneity
5. **Explicitly framed as descriptive**: "We document the following patterns in demand reallocation around model entry events..."

### C. Panel Regression (Descriptive)
$$\ln(D_{mt}) = \alpha_m + \delta_t + \beta_1 \cdot \text{SameFirmEntry}_{mt} + \beta_2 \cdot \text{CrossFirmEntry}_{mt} + \gamma \cdot \text{ModelAge}_{mt} + \varepsilon_{mt}$$
- Acknowledged as descriptive correlation, not causal
- Used to document systematic patterns across many entry events

---

## External Validity Discussion (Required)

OpenRouter is an aggregator platform that attracts developers valuing model-switching flexibility. This means:
- **Overstates displacement/cannibalization**: Users on OpenRouter can switch models trivially (same API endpoint), so we likely observe an upper bound on displacement
- **Understates stickiness**: Enterprise customers with direct API contracts (not on OpenRouter) face higher switching costs
- **Market expansion may be understated**: New users may go directly to providers, bypassing OpenRouter
- **Calibration**: We will attempt to bound OpenRouter's share of total API traffic using publicly available data (model provider traffic estimates, OpenRouter's stated user base of >1M users)

---

## Closest Papers + Marginal Contribution

1. **Fradkin (2025)** "Demand for LLMs" — 3 case study model releases on OpenRouter. *Our contribution*: (a) Systematic analysis of ALL entries with panel methods; (b) Nested logit demand model that estimates substitution elasticities; (c) Formal three-channel decomposition.
2. **Demirer et al. (2025)** "Emerging Market for Intelligence" NBER WP 34608 — 6 market structure facts, including price elasticity ~1 and market dynamism. *Our contribution*: We explain the mechanism behind market dynamism — decomposing demand reallocation into three channels and estimating substitution patterns.
3. **Bresnahan & Greenstein (1999)** "Technological Competition and the Structure of the Computer Industry" — Platform displacement in computing over decades. *Our contribution*: High-frequency (daily) evidence that creative destruction in the LLM market operates on a timescale of days to weeks, not years.

---

## Data Feasibility: ✅ Strong
- Daily model-level usage panel: 29K obs, 389 models, 66 firms, 93 days
- Model metadata with characteristics: context_length, supports_reasoning, pricing
- Weekly rankings with firm-level market shares (52 weeks, longer than our panel)
- Multiple entry events (~50+) during sample period
- Rich usage features: requests, tokens (prompt/completion/reasoning/cached), tool calls
