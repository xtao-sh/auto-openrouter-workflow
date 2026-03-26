---
## Referee Report — Round 2 — Field Expert

**Date**: 2026-03-26

### 修改评估

- **R1 Major Comment 1**: Discrete-choice framework inconsistent with multihoming behavior.
  - 作者回应: Accepted
  - 修改质量: Satisfactory
  - 备注: The revised paper adds a substantive "Multihoming" paragraph in the Discussion (Section 7.1) that explicitly names the problem---within-developer portfolio allocation misattributed as between-developer preference heterogeneity---and cites Gentzkow (2007). The Related Literature section now integrates Gentzkow's complementarity framework with a clear statement that a multiple-discrete-choice model is the appropriate future extension. The authors also acknowledge the direction of bias (inflating sigma). I would have preferred at least a back-of-envelope estimate of how much of within-firm usage might come from multi-model pipelines, but the conceptual treatment is now adequate.

- **R1 Major Comment 2**: "Creative destruction" framing too strong for the evidence.
  - 作者回应: Accepted
  - 修改质量: Excellent
  - 备注: This is the most successful revision. The abstract now leads with "quality-ladder cannibalization" rather than "creative destruction." The Discussion introduces the Schumpeter Mark I vs. Mark II distinction, explicitly noting the finding maps onto Mark II creative accumulation rather than Mark I displacement. The three competing explanations for the cross-firm null---horizontal differentiation, growth-phase masking, information frictions---are laid out cleanly with distinct policy implications for each. The new engagement with Desai (2001), Draganska & Jain (2005), and Aghion & Howitt (1992) is genuine, not perfunctory. This comment has been fully addressed.

- **R1 Major Comment 3**: IV failure deserves more treatment and OLS sigma needs better bounding.
  - 作者回应: Accepted
  - 修改质量: Satisfactory
  - 备注: Three new paragraphs address this. The "Oster bound and simultaneity" paragraph explicitly states that the Oster framework does not address the mechanical simultaneity concern. The "Direction and magnitude of OLS bias" paragraph provides a rough calibration placing the bias at 0.05--0.15 and offers an honest range of [0.25, 0.50]. The Hausman-type IV exploration (sigma approximately 0.35, SE approximately 0.12) is reported transparently. The paper now treats 0.46 as "a plausible upper bound." My one remaining concern is that the honest range is presented without a formal derivation, but the qualitative improvement is substantial.

- **R1 Major Comment 4**: Alternative nesting results (sigma > 0.99) are likely mechanical.
  - 作者回应: Accepted
  - 修改质量: Excellent
  - 备注: The revised text is unambiguous: "We treat these boundary estimates as mechanical artifacts rather than substantive findings." No further action needed.

- **R1 Major Comment 5**: Family-upgrade event study underpowered.
  - 作者回应: Accepted
  - 修改质量: Satisfactory (with reservation)
  - 备注: The event study figure is now explicitly framed as "illustrative rather than confirmatory." New paragraphs acknowledge the need for permutation inference, wild cluster bootstrap, and leave-one-event-out analysis. However, none of these analyses have actually been implemented. The paper now contains five paragraphs that each acknowledge a necessary analysis and promise it for the "next revision." While the transparency is commendable, there is a limit to how many promissory notes a single revision can accumulate without delivering actual results.

- **R1 Major Comment 6**: Outside option construction needs more scrutiny.
  - 作者回应: Partially Accepted
  - 修改质量: Insufficient
  - 备注: Implied own-price elasticities are now reported (-0.5 to -1.5), but the more substantive request---how the price coefficient and elasticities vary with the outside option assumption---has not been addressed. This remains an open item, though minor relative to other concerns.

### Cross-Referee 反馈

- **同意的意见**:
  - Referee 2 (Methods): Pre-trends are the most critical issue. I agree completely. The revised paper's handling of this is a major improvement.
  - Referee 3 (Writing): The Introduction was too long and too front-loaded. The revision from 8 to 6 paragraphs and the removal of standard errors from the Introduction is an improvement.
  - Referee 4 (Policy): The external validity limitation is consequential. The new paragraph on external validity does a reasonable job mapping findings to generalizability.
  - Red Team: The product-life-cycle alternative explanation is directly supported by the pre-trend t = -2.75. The revision acknowledges this but cannot rule it out without implementing HonestDiD.

- **不同意的意见**:
  - Referee 4 (Policy), Major Comment 4: I agree with the editor's dismissal of the SSNIP test request. The paper is an empirical demand analysis, not an antitrust filing.
  - Referee 4 (Policy), R1 score of 4.8/10: Too harsh. The paper is not attempting to be a policy document.

- **受启发发现的新问题**:
  - The positive rival-entry coefficient (0.001, SE = 0.0003 in Table 3 Column 2) is significant. If day FEs absorb aggregate demand, this should be zero unless rival entry has within-day cross-model variation. Warrants a sentence of explanation.
  - The accumulated inventory of unimplemented analyses in Section 6.3 creates a presentation issue.

### 逐项评分（更新后）

1. **文献定位与边际贡献：7.0/10 ↑** (was 6.0) — Engagement with product line management literature, Aghion & Howitt, Gentzkow, and Hagiu & Wright substantially strengthens positioning. Mark I vs. Mark II distinction genuinely integrated.

2. **制度背景准确性：7.5/10 ↑** (was 7.0) — New external validity discussion and multihoming paragraph improve institutional honesty. Family-upgrade classification endogeneity now explicitly treated.

3. **研究问题重要性：8.0/10 →** (was 8.0) — Unchanged. Question remains important. Reframing aligns scope more honestly.

4. **结果经济学解读：6.5/10 ↑** (was 5.0) — Largest improvement. Three explanations for cross-firm null well-articulated. "Concordance" downgraded to "qualitative consistency." Non-sigma coefficients discussed. However, pre-trend issue means -0.43's interpretation remains uncertain without HonestDiD.

5. **前沿文献对话：7.0/10 ↑** (was 5.0) — Engagement now substantive. Gentzkow, Desai, Draganska, Aghion & Howitt all genuinely integrated.

### 总分：7.2/10

### 剩余问题（如有）

1. **Unimplemented quantitative analyses.** HonestDiD bias correction, Sun & Abraham robust estimator, permutation inference, wild cluster bootstrap, leave-one-event-out, and PPML all remain undelivered. HonestDiD and permutation inference are the most consequential: without the former, the paper cannot determine whether -0.43 survives bias correction; without the latter, it cannot establish that the result is not driven by panel structure.

2. **Outside option sensitivity for the price coefficient.** Paper reports sigma is invariant but not whether alpha or implied elasticities also vary. Minor but unresolved.

3. **Rival entry coefficient.** The positive and significant rival-entry coefficient warrants a sentence of explanation.

### 总体建议：MINOR REVISION

The revision represents substantial and genuine improvement across all dimensions. The reframing to quality-ladder cannibalization is fully successful. The literature engagement is now appropriate. The honest range for sigma, the Oster-simultaneity distinction, the degradation of near-unity nesting estimates, and the pre-trend reporting are all handled well.

The reason I recommend Minor Revision rather than Accept is entirely about the unimplemented quantitative analyses. A minor revision that implements HonestDiD and permutation inference---and adjusts the quantitative claims if necessary---would bring this paper to an acceptable standard. No further conceptual, framing, or literature changes are needed.
