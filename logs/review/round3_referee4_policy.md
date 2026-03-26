---
## Round 3 Report — Policy & Relevance (Referee 4)

**Date**: 2026-03-26
**Round 2 score**: 6.5/10 | **R2 Recommendation**: MINOR REVISION

---

### 修改评估

My R2 report identified five remaining issues, of which the first (unimplemented robustness checks) was by far the most consequential. I evaluate the revision against each.

**Issue 1: Unimplemented robustness checks undermining quantitative claims -- RESOLVED.**
All four required analyses are now implemented and reported in Section 4.3:
- HonestDiD: beta_corrected = -0.28 (CI: [-0.52, -0.04]). The 35% headline is now honestly bounded to 24-35%.
- Permutation: p_perm = 0.032. The family-upgrade displacement is unlikely to be a chance alignment.
- Sun & Abraham: beta_SA = -0.38 (SE = 0.19). Heterogeneous timing does not bias the result.
- Leave-one-event-out: range [-0.31, -0.52]. Not driven by any single event.

From a policy perspective, this is the critical improvement. A policymaker can now cite the 24-35% range with the understanding that the lower bound accounts for pre-trend bias and the upper bound is the naive estimate. The permutation p-value and Sun & Abraham confirmation provide the inferential backing that was missing in R2.

**Issue 2: Back-of-the-envelope pre-trend adjustment -- SUPERSEDED.**
The HonestDiD correction directly provides what the back-of-the-envelope calculation would have approximated. The corrected beta = -0.28 quantifies the pre-trend adjustment more rigorously than a linear extrapolation would. This concern is fully resolved.

**Issue 3: Which events drive the result -- RESOLVED.**
The leave-one-event-out analysis identifies that 5 events from 3 firms (OpenAI, Anthropic, Google) contribute disproportionately. The GPT-4o upgrade is the most influential single event. The paper honestly reports this concentration as a feature of market structure. For a policymaker, this is useful: the displacement dynamic is primarily identified from major-firm upgrades, which are exactly the events most relevant for antitrust and competition analysis.

**Issue 4: Model deprecation -- NOT ADDRESSED.**
The paper still does not report how many of the 43 events involve provider-side deprecation. The Limitations paragraph acknowledges this but does not attempt even a rough count. This remains a gap, though it is minor relative to the resolved items.

**Issue 5: Revenue-weighted analysis -- NOT ADDRESSED.**
The paper still relies on request counts. This is a data limitation that cannot be resolved with current data and is appropriately flagged in the Limitations section (line 682).

### 逐项评分（最终）

1. **政策相关性：8.0/10 ↑** (was 7.5) -- The 24-35% range, backed by HonestDiD and permutation inference, is now a citable policy statistic. The three-explanation framework for the cross-firm null (from R2) combined with the robustness checks gives a policymaker a complete picture: within-family displacement is real and bounded, cross-firm displacement is absent, and the finding is robust to the major econometric concerns.

2. **外部有效性：6.5/10 ↑** (was 6.0) -- Modest improvement. The robustness checks do not directly address external validity, but the leave-one-event-out analysis showing concentration among major-firm events is informative: the pattern is identified from the most policy-relevant events (frontier model upgrades by top firms). The external validity paragraph from R2 remains adequate.

3. **机制清晰度：7.5/10 ↑** (was 7.0) -- The four robustness checks, taken together, strengthen the mechanistic interpretation. HonestDiD confirms the displacement is not entirely a pre-trend artifact; Sun & Abraham confirms it is not a TWFE artifact; the leave-one-event-out confirms it is not driven by a single event. The quality-ladder cannibalization mechanism is now empirically grounded rather than merely asserted.

4. **福利含义：6.0/10 ↑** (was 5.5) -- Marginal improvement. The honest range 24-35% gives a more precise input for welfare calculations, but the paper still does not discuss whether within-family cannibalization is welfare-improving or welfare-reducing. The Arrow (1962) replacement effect is mentioned but its welfare implications remain undeveloped. This is a structural limitation of the paper's scope.

5. **研究持久价值：7.0/10 ↑** (was 6.5) -- The full robustness suite makes the paper's estimates more durable. Future work will cite the 24-35% range as a baseline rather than dismissing the 35% figure as uncorrected.

### 总分：7.0/10

### 总体建议：ACCEPT

The four required computational analyses are implemented and resolve the primary concern from my R2 report. Two secondary issues (deprecation counts, revenue weighting) remain unaddressed but are not blocking -- they reflect data limitations rather than analytical omissions. The external validity (6.5) and welfare implications (6.0) dimensions remain below 7.5, but these reflect the structural scope of the paper (single platform, 93 days, no supply-side model) rather than remediable deficiencies. All dimensions that can be improved through revision have been improved. The paper's policy contribution -- a bounded, robustness-checked estimate of within-family displacement in LLM markets -- is now citable and defensible. I support acceptance.
