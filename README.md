# Multi-Agent Academic Paper Workflow

A multi-agent workflow for writing and iteratively reviewing an academic economics paper, using independent AI instances for writing, quality gates, and simulated peer review.

## Paper

**"Creative Destruction in the Market for Intelligence: Demand Reallocation When New LLMs Enter"**

Using daily data on 385 models from 66 firms over 93 days on OpenRouter, we estimate a nested logit demand model and conduct event studies around model entry events. The headline finding: creative destruction operates almost exclusively through within-family upgrades — predecessors lose 24–35% of daily requests when successors launch, while cross-firm entries produce no detectable displacement.

## What This Repo Contains

| Directory | Contents |
|-----------|----------|
| `WORKFLOW_v2.md` | Paper writing workflow — 5-layer quality assurance with 4 independent critic gates |
| `WORKFLOW_REVIEW.md` | Simulated peer review workflow — 5 independent referee roles × 3 rounds |
| `paper/` | LaTeX source and PDFs for all versions (original, R1 revision, R2 revision, clean final) |
| `code/` | Python analysis scripts (data exploration, construction, regressions, robustness, heterogeneity, number verification) |
| `output/` | Regression tables (CSV), figures (PNG), identification memo, pre-analysis plan |
| `logs/` | All referee reports, editorial letters, response letters, score tracking, revision changelog |
| `logs/review/` | Complete Round 1–3 referee reports, editorial decisions, and response letters |
| `config/` | Style references and research rules |

## Workflow Design

### Phase 1: Paper Writing (WORKFLOW_v2)

1. **Data Exploration** → descriptive statistics, visualizations
2. **Research Design** → identification strategy, pre-analysis plan
3. **Empirical Analysis** → regressions, robustness checks
4. **Paper Writing** → section-by-section LaTeX generation
5. **4 Independent Critic Gates** → each section must score ≥7/10

### Phase 2: Simulated Peer Review (WORKFLOW_REVIEW)

1. **5 Independent Referees**: Field Expert, Methodologist, Writing Specialist, Policy Expert, Red Team (adversarial)
2. **Editor synthesizes** all reports into an editorial letter
3. **Response Letter** written to address each point
4. **Revisions** implemented with version tracking
5. **Up to 3 rounds** until consensus Accept

## Key Results

- Round 1: Average score 6.3/10 → Major Revision
- Round 2: Average score 7.3/10 → Minor Revision
- Round 3: Average score 7.4/10 → **Accept**
- Total referee reports generated: 13
- Key improvements: identification discussion, robustness (HonestDiD, Sun & Abraham), title and framing

## Note

Raw data (`data/`) is not included in this repository. The code and analysis scripts reference data files that would need to be obtained separately from OpenRouter's public API.
