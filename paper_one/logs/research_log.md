# Research Log — LLM API Market Economics

## Phase 0: Initialization — 2026-03-25

### Workflow Version
WORKFLOW_v2.1 (2026-03-25)

### Data Overview
- **Daily panel** (`data/master/usage_daily.csv`): 29,407 rows × 13 columns
  - 391 unique models, date range 2025-12-20 to 2026-03-24 (~94 days)
  - Variables: count (requests), prompt/completion tokens, reasoning tokens, cached tokens, tool calls, media counts
  - Highly skewed: median 2,856 req/day, mean 82,216, max 9.9M
- **Rankings snapshots** (`data/rankings/`): 11 snapshots (2026-02-03 to 2026-03-25, ~5-day intervals)
  - Each snapshot: 11 JSON files (top_models, market_share, categories, context_length, fastest_models, images, languages_natural, languages_programming, tool_calls, top_apps, top_models)
  - `top_models.json`: weekly top models by tokens, 52 weekly data points (2025-03-31 to 2026-03-23)
  - `market_share.json`: weekly market share by author (firm), 53 weekly data points
- **Model metadata** (`data/master/models_enriched_latest.csv`): 658 models × 35 attributes
  - Includes: author, context_length, created_at, features, input/output modalities, supports_reasoning, pricing info

### Data Quality Notes (from data_quality_report.md)
- Historical data is retroactively updated (NOT immutable)
- High-volume models (>10K req/day): ~4% variation, stable
- Low-volume models (<100 req/day): extremely volatile, unreliable
- Recommendation: filter >1K req/day for trend analysis, use 7-day rolling averages, exclude same-day data

### Existing Outputs
- No existing code, research design, or paper files — starting fresh
- Empty output/figures/ and output/tables/ directories

### Key Constraints
- Panel: ~94 days — cannot claim "long-term trends"
- Observational data — no natural experiment unless we find one
- Must differentiate from Fradkin (2025) and Demirer et al. (2025)

---

## Phase 2: Research Design — 2026-03-25

### Decision: Selected Candidate 1
- **Topic**: Creative destruction on a quality ladder — intra-firm cannibalization vs. cross-firm displacement
- **Rationale**: Strongest identification (within-firm event variation), clearest theory (Schumpeterian), best differentiation from Fradkin (2025) (systematic panel vs. 3 case studies)
- **Alternatives considered**: (2) Capability premium / reasoning adoption, (3) Market concentration dynamics
- **Alternative 2 rejected because**: Weaker identification — capabilities correlated with quality
- **Alternative 3 rejected because**: Too descriptive for standalone paper

### Literature search completed (Round 1)
- 10 papers identified, closest 3: Fradkin (2025), Demirer et al. (2025), Bresnahan & Greenstein (1999)
- Key differentiation from Fradkin: systematic panel analysis of ALL entries vs. 3 case studies
- Methodological refs: de Chaisemartin & D'Haultfœuille (2020), Sun & Abraham (2021) for staggered TWFE

### Files produced
- `output/research_design.md` — Full design with 3 candidates (revised R1 after Gate 1)
- `output/identification_memo.md` — ID strategy, threats, mitigations (revised R1)

---

## Gate 1 Results — 2026-03-25
- Round 1: FAIL (6.2/10). Key issues: identification too weak, no external validity discussion, theory informal.
- Round 2: PASS (7.3/10). Revised to nested logit demand + descriptive framing + external validity.
- Watchpoints: (1) instrument validity for within-group share, (2) nesting structure robustness

## Phase 3: Empirical Analysis — 2026-03-25

### Key Results
1. **Nested logit σ (OLS) = 0.456** (SE=0.042): Within-firm models are closer substitutes than cross-firm
   - IV σ = -0.149 (questionable instrument; OLS preferred per Oster δ=155)
   - σ for reasoning models = 0.578 vs non-reasoning = 0.386 → reasoning models compete more intensely within firms
   - Robust to outside option assumptions (10%-40% outside share all give σ=0.456)
   - Alternative nesting by capability tier: σ=0.999, by price tier: σ=0.992 (nearly perfect substitution within tiers)
2. **Same-family upgrade effect = -0.43** (SE=0.16, p<0.01): When a firm releases an upgrade in the same model family, the old version loses ~35% of requests. This is the KEY finding — cannibalization is concentrated in family upgrades.
3. **Cross-family and rival entry effects**: Near zero and insignificant. Different-family entries from same firm and rival entries do not displace incumbents.
4. **Market expansion**: +3-20% total requests around major entry events. Market is growing, not just redistributing.
5. **Placebo test**: Shuffled firm assignments → β ≈ 0, as expected.

### Pre-analysis plan deviations
- model_age dropped from panel specs (perfectly collinear with model+day FE as expected)
- rival_entry dropped from TWFE specs (collinear with day FE — varies only by date). Used entity+week FE spec instead.
- Added same_family vs diff_family decomposition (not pre-specified but motivated by economics)

### Files produced
- code/03_data_construction.py, code/04_baseline_regression.py, code/05_robustness.py, code/06_heterogeneity.py
- output/analysis_panel.csv (30,903 obs)
- output/tables/table02-06 CSVs
- output/figures/fig11-14

---

## Phase 2.5: Pre-Analysis Plan — 2026-03-25
- Written `output/pre_analysis_plan.md`
- Primary spec: nested logit demand (Berry 1994)
- Secondary: descriptive panel regression + event study
- 10 robustness checks planned, 4 heterogeneity dimensions
- Clustering: model-level (primary), model×week (robustness)

---
## Phase 4: Paper Writing — 2026-03-25

### Process
- Paper written section-by-section per WORKFLOW_v2 rules (8 steps)
- Each section compiled with `pdflatex -draftmode` check
- Number verification: 18/18 matches, 0 mismatches
- Word count: ~10,500 (meets ≥10,000 requirement)

### Gate 3 Results
- Round 1: PASS (8.0/10). Strong writing quality (9/10) and honesty (9.5/10). Issues: IV failure needs deeper analysis, near-unity sigma for tiers suspicious, short panel for "creative destruction" claims.
- All major/minor comments addressed in revision.

### Gate 4 Results
- Round 1: PASS (7.75/10). Must-fix items: duplicate subsection header, reconcile event counts, soften causal language, add structural validation paragraph.
- All must-fix items addressed.

---

## Phase 5: Compilation & Packaging — 2026-03-25

- LaTeX compilation: 51 pages, 0 undefined references, clean build
- Code reproducibility: All 6 scripts (01-07) run successfully from scratch
- Final self-check: All files present, all quality criteria met
- DONE.md created


