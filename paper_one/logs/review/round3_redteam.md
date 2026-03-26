---
## Red Team Report — Round 3 (Final)

**Date**: 2026-03-26
**Round 2 assessment**: Partially survives challenge | **R2 Recommendation**: MINOR REVISION

---

### 杀手检验结果

**杀手检验 1: Roth (2022) HonestDiD 前趋势偏误校正 -- RESOLVED.**

The test is now implemented. beta_corrected = -0.28 (95% CI: [-0.52, -0.04]). The result: approximately one-third of the naive -0.43 coefficient is attributable to pre-existing predecessor decline. The confidence interval excludes zero. The qualitative finding survives; the quantitative claim is honestly attenuated from 35% to a 24-35% range.

This was my most critical killer test. The outcome is the moderate scenario: the effect shrinks but does not disappear. The paper handles this honestly -- the Abstract says "24-35%" rather than the original "35%," and the lower bound is explicitly attributed to the HonestDiD correction. The paper does not bury the attenuation or minimize it. The strategic concern I raised in R2 -- that the authors might be deferring the test because they feared it would eliminate the effect -- is resolved: they ran the test and reported an inconvenient result transparently.

**杀手检验 2: 基于能力重叠的替代分类 -- PARTIALLY RESOLVED (accepted limitation).**

This test remains unimplemented. The paper continues to rely on naming-convention-based classification, and the Limitations paragraph on "Family-upgrade classification endogeneity" (line 674) remains the only engagement. However, the leave-one-event-out analysis partially addresses the underlying concern: if the classification were capturing noise rather than signal, the jackknife would show high sensitivity to individual events, with some reclassifiable events producing large changes. The tight IQR [-0.45, -0.39] suggests the classification is picking up a real pattern, not an artifact of a few mislabeled events.

I accept this as a residual limitation rather than a blocking deficiency. The capability-overlap classification would be a valuable extension for future work, but the current classification is adequate given the supporting diagnostics.

**杀手检验 3: 日期置换推断 -- RESOLVED.**

Implemented. p_perm = 0.032 from 1,000 within-firm permutations. The permutation distribution is centered at zero (SD = 0.18), and only 32 of 1,000 draws produced |beta| >= 0.43. The family-upgrade displacement is not a chance alignment of upgrade dates with unrelated demand fluctuations. The distribution-free p-value is somewhat less extreme than the parametric result, confirming mild over-rejection -- which the paper correctly interprets as consistent with having 43 events rather than an asymptotic sample.

This was the second most critical killer test. The result confirms that the inference is sound even without relying on asymptotic approximations.

### 替代解释的处理

**产品生命周期 / 反向因果**: The HonestDiD correction directly quantifies how much of the effect could be attributed to pre-existing decline. The answer: roughly one-third. The remaining two-thirds (beta_corrected = -0.28) survives. The paper appropriately treats this as a lower bound rather than dismissing the pre-trend.

**增长掩盖 cross-firm displacement**: Unchanged from R2. This remains a structural limitation of the 93-day panel. The three-explanation framework (horizontal differentiation, growth-phase masking, information frictions) is the correct analytical response.

**分类伪影**: Partially mitigated by the leave-one-event-out analysis, which shows the result is not driven by a few potentially mislabeled events. The tight jackknife IQR provides indirect evidence that the classification captures real displacement.

### 综合评估：论文能否经受住挑战？Yes -- with known limitations.

The paper's R2 structural problem -- "a well-crafted promissory note" with zero new empirical analyses -- is fully resolved. Four computational analyses are now implemented, all supporting the qualitative finding while honestly attenuating the quantitative claim. The two killer tests that were most likely to challenge the headline number (HonestDiD and permutation inference) both produce results consistent with real but attenuated displacement. The pre-registered Sun & Abraham estimator is delivered. The leave-one-event-out rules out single-event dependence.

The remaining vulnerabilities are structural and cannot be resolved through further revision:
- The capability-overlap classification is infeasible without benchmark data.
- The 93-day panel cannot test whether the cross-firm null is permanent or growth-phase-specific.
- Revenue weighting is not possible with current data.
- Model deprecation counts are not available.

These are limitations of the research setting, not of the paper's analytical execution. The paper acknowledges all of them clearly.

### 总体建议：ACCEPT

The path from R1 to R3 demonstrates a revision process that works. R1 identified critical deficiencies (misrepresented pre-trends, missing robustness checks, overclaimed framing). R2 resolved the textual and conceptual issues while deferring computation. R3 delivers the computation. The result is a paper that honestly reports a 24-35% displacement effect, validated by four independent diagnostic frameworks, with all major caveats and alternative explanations clearly articulated. The paper can withstand adversarial scrutiny. I support acceptance.
