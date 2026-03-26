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

Five layers of quality assurance, each targeting a specific weakness of single-agent generation:

1. **Disciplinary norm anchoring** — Forced identification memo before any regression
2. **Independent critic gates** — 4 gates with separate AI instances (not self-review), quantitative scoring, fail → rewrite
3. **Pre-registration** — Pre-analysis plan written before regressions, deviations must be explained
4. **Number verification** — Automated cross-check of every statistic in the paper against output files
5. **Hard quantitative thresholds** — ≥20 citations, ≥5 robustness checks, 0 fabricated references, 100% number match

### Phase 2: Simulated Peer Review (WORKFLOW_REVIEW)

Simulates a top-tier economics journal R&R process with 5 independent referee roles:

| Role | Focus |
|------|-------|
| Field Expert | Literature positioning, institutional accuracy |
| Methods Expert | Causal identification, econometric specification |
| Writing Expert | Narrative structure, AI writing artifacts |
| Policy Expert | Policy implications, external validity |
| Red Team | Attacks weakest assumptions, designs "killer tests" |

Key design choices:
- Each referee is a fully independent AI instance (separate context window)
- Opinions are triaged (Must Fix / Should Fix / Consider / Decline) before revision
- Referees who accept exit subsequent rounds; others continue
- Red team activates automatically when average score < threshold

### Score Trajectory

| Stage | Score | Key Event |
|-------|-------|-----------|
| Gate 1 R1 | 6.2 FAIL | Causal claims too strong → repositioned as descriptive |
| Gate 2 R1 | 6.6 FAIL | IV failed → alternative approach |
| Gate 3 | 8.0 PASS | |
| Gate 4 | 7.75 PASS | |
| Review R1 | 5.85 Major Revision | Pre-trends hidden, framework challenged |
| Review R2 | 7.03 Minor Revision | Conceptual work done, pending computation |
| Review R3 | 7.43 **Accept** | All quantitative tests passed, unanimous accept |

## What's NOT Included

- **Raw data** — The underlying OpenRouter usage data is proprietary and not included
- **API keys or credentials**

The code and output files are included to demonstrate the workflow, but the analysis cannot be reproduced without the original data.

## Implementation

The workflow was implemented using [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Anthropic Claude Opus) with task sub-agents for referee isolation. Each referee operates in its own context window via Claude Code's sub-agent system.

## License

MIT
