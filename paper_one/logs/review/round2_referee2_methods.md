---
## Referee Report -- Round 2 -- Econometrician

**Date**: 2026-03-26
**Paper**: "Creative Destruction in the Market for Intelligence: Demand Reallocation When New LLMs Enter"
**Referee**: R2 (Econometrician)
**Round 1 score**: 5.8/10 (Major Revision)

---

### 修改评估

I organize this assessment around my six R1 Major Comments, evaluating each revision in turn.

#### R1 Major Comment 1: Pre-trends are significant and the paper misrepresents them.

**R1 demand**: Report pre-trend t-statistics prominently; explain the discrepancy with qualitative claims; conduct Roth (2022) HonestDiD bias correction.

**Assessment: Substantially addressed in text, but key computational analysis deferred.**

This was the most serious issue in R1, and the revision takes it seriously. The authors have (a) prominently reported all three pre-trend t-statistics in the body of the paper (Section 6.3, lines 518--522), including the damning t = -2.75 for the family-upgrade specification; (b) deleted all contradictory language ("no evidence of differential pre-trends") from the manuscript; (c) added substantive discussion of two interpretations (reverse causality and anticipation effects, lines 520--521); and (d) added an explicit paragraph acknowledging that the HonestDiD correction has not been implemented, with an honest caveat that "if the bias-corrected coefficient shrinks substantially or the corrected confidence interval includes zero, the quantitative claim of 35% displacement would require downward revision" (line 522).

The textual honesty here is exemplary. The revision no longer misrepresents its own test statistics, and the two-interpretation framework (reverse causality versus anticipation) is a genuine analytical contribution. The Abstract and Conclusion have been appropriately softened ("pre-trend tests and small event counts warrant caution in interpreting the magnitudes causally," line 45).

However, the HonestDiD bias correction itself remains unimplemented. This was flagged as a "Must Fix" by the editor. The authors' candid acknowledgment that this is a limitation, and their explicit statement of what a bad result would mean for their claims, partially mitigates the omission---but it does not eliminate it. The -0.43 coefficient's causal interpretation remains indeterminate until the correction is performed. I view this as an acceptable deferral for this revision given the thoroughness of the textual discussion, but it must appear in the final version. This keeps my assessment at "substantially addressed" rather than "fully addressed."

**Score impact**: Identification credibility moves from 5/10 to 6.5/10. The honest reporting is a major improvement; the missing correction prevents a higher score.

---

#### R1 Major Comment 2: OLS sigma = 0.46 lacks a credible identification strategy.

**R1 demand**: Attempt alternative IVs (Hausman-type, leave-out shares); estimate bounds under different bias assumptions; discuss what the IV result implies; acknowledge that Oster does not address simultaneity.

**Assessment: Well addressed within realistic constraints.**

The revision adds three important paragraphs in Section 6.1 (lines 403--405). First, the "Oster bound and simultaneity" paragraph (line 403) explicitly states that the Oster framework "does not address the specific simultaneity concern at issue here" -- a direct correction of the R1 paper's implicit conflation. This alone is a significant improvement. Second, the "Direction and magnitude of OLS bias" paragraph (line 405) provides a rough calibration: if demand shocks account for half the within-day variance of within-firm share, the bias is on the order of 0.05--0.15, placing sigma in [0.30, 0.40]. The honest range of [0.25, 0.50] is reported with appropriate caveats. Third, the Hausman-type IV exploration is reported (sigma approximately 0.35, SE approximately 0.12), with an honest acknowledgment that 93 days provides insufficient time-series variation for precision.

The reframing of sigma as an upper bound rather than a point estimate, and the emphasis that "the qualitative finding -- sigma meaningfully positive, indicating closer within-firm substitution -- as the robust conclusion" (line 405), is precisely what I asked for. The paper no longer treats 0.46 as a precise structural parameter. The IV failure discussion (lines 399--401) is also improved: the new text explains why product-line breadth violates the exclusion restriction in LLM markets in a way that is informative about market structure, not just a methodological inconvenience.

What remains missing: leave-out shares (excluding model m from its firm's total) as an alternative instrument were not attempted. The paper also does not formally discuss what the IV result of -0.15 implies about the correlation structure between the instrument and unobservables -- specifically, the positive sign of cov(Z, xi) that would be needed to generate the negative sigma estimate. These are second-order issues given the overall quality of the revision.

**Score impact**: Model specification moves from 6/10 to 7.5/10. The bias direction calibration and honest range are substantial contributions.

---

#### R1 Major Comment 3: Family-upgrade result relies on 43 events with no permutation inference.

**R1 demand**: Permutation inference p-value; wild cluster bootstrap; leave-one-event-out sensitivity.

**Assessment: Acknowledged and flagged, but none implemented.**

The revision adds three dedicated paragraphs (lines 526--528) that explicitly acknowledge the need for permutation inference, wild cluster bootstrap, and leave-one-event-out analysis. Each paragraph correctly describes what the test would do and why it matters. The event study figure is now explicitly described as "illustrative rather than confirmatory" (line 530), and the Limitations section adds a paragraph on "Small number of family-upgrade events" (line 670).

However, none of these analyses have been performed. The response letter characterizes all three as "标记为下一轮修改优先事项" (flagged for next revision). For a Round 2 review, this is a concern. The editor's Must Fix list included "Conduct permutation inference for the family-upgrade coefficient (1,000+ random reassignments of upgrade dates). Report wild cluster bootstrap p-values." These are computationally straightforward exercises -- 1,000 permutations of 43 dates can be run in minutes -- and their absence after a revision round suggests either resource constraints or a deliberate deferral strategy.

That said, the intellectual groundwork is laid. The paper's verbal caveats are sufficiently strong that a reader will not be misled about the fragility of the inference. The question is whether the journal's standards require the computation itself, or whether the honest acknowledgment suffices. My view: the permutation inference and leave-one-event-out analysis must be present in a published version. For this revision, the acknowledgment is adequate but this remains a binding "Minor Revision" item.

**Score impact**: Standard errors and inference moves from 5/10 to 6.5/10. The honest framing helps, but the missing computations limit the improvement.

---

#### R1 Major Comment 4: Near-unity nesting parameters are mechanical artifacts.

**R1 demand**: Drop these results, estimate multi-level nested logit, or clearly flag as uninformative.

**Assessment: Fully addressed.**

The revision completely rewrites the discussion of alternative nesting structures (line 563). The near-unity estimates are now explicitly labeled "mechanical artifacts rather than substantive findings." The paper provides a clear explanation of why coarse grouping produces boundary estimates ("each group contains enormous heterogeneity... which mechanically pushes sigma toward the boundary"). The paper no longer draws substantive conclusions from these estimates, and the text "we do not draw substantive conclusions from these near-unity estimates" is unambiguous.

This is exactly what I asked for. The multi-level nested logit suggestion is noted as desirable but infeasible given sample size, which is a reasonable practical constraint. The paper handles this limitation cleanly.

**Score impact**: This comment is resolved. No residual concern.

---

#### R1 Major Comment 5: Sun & Abraham (2021) staggered TWFE estimator not implemented.

**R1 demand**: Implement the pre-registered robust estimator for the family-upgrade specification.

**Assessment: Acknowledged but not implemented.**

The revision adds a dedicated paragraph (line 524) acknowledging that the Sun & Abraham estimator was pre-specified but not yet implemented, and another paragraph in the robustness section (line 604) repeating this acknowledgment. The paper correctly notes that the TWFE concern is less consequential for the aggregate null but substantive for the family-upgrade coefficient of -0.43.

As with Major Comment 3, the acknowledgment is honest but the computation is absent. The Sun & Abraham estimator is available as an R or Stata package and is not computationally demanding for 43 events. This is a pre-registered analysis, and its continued absence after a revision round is a notable gap. The paper's own pre-analysis plan commits to this check, and the deviation is documented (Appendix Section C), but documentation of a deviation is not the same as remediation.

For the specific case of the family-upgrade coefficient, the concern is real: with 43 events at different times, different event cohorts may exhibit different treatment effects (e.g., early-sample upgrades in a period of rapid growth versus late-sample upgrades in a slower period). If TWFE assigns negative weights to some cohort-specific effects, the -0.43 estimate could be substantially biased. The paper cannot know whether this is the case without running the estimator.

**Score impact**: Robustness moves from 6/10 to 7.0/10. The conceptual acknowledgment and the improved suite of other robustness checks (bias calibration, honest range for sigma) help, but the missing computation limits the score.

---

#### R1 Major Comment 6: Entry variable conflates qualitatively different events.

**R1 demand**: Weight entry events by initial uptake; distinguish major from minor entries; report binary indicator.

**Assessment: Partially addressed through decomposition, but not through reweighting.**

The family-upgrade indicator (binary, 0/1) effectively addresses the binary-versus-count concern for the key result. The decomposition into same-family upgrades versus different-family entries is the paper's strongest analytical move and directly separates the "consequential" from "inconsequential" entries.

However, the broader issue -- that the aggregate same-firm entry count (SD = 8.4) treats all entries equally -- is not addressed by weighting or by distinguishing major launches from minor variants. The response letter indicates this is "留待下轮" (deferred). Given that the aggregate coefficient is null and the interesting action is in the family-upgrade decomposition (which is binary), this is a lower-priority concern than in R1. I no longer view it as a Major Comment issue.

**Score impact**: Marginal improvement. The decomposition effectively addresses the concern for the key result.

---

### Cross-Referee 反馈

#### Response to Referee 1 (Field Expert) concerns

Referee 1's core concern about the discrete-choice / multihoming tension is now addressed through a dedicated "Multihoming" paragraph in the Discussion (line 638). The paper cites Gentzkow (2007) appropriately and explicitly discusses how multihoming inflates the nesting parameter. The acknowledgment that "a full multiple-discrete-choice model a la Gentzkow is beyond the scope of this paper" is appropriately framed. The "creative destruction" reframing requested by both R1 and R4 is handled well: the Mark I vs. Mark II discussion (Section 3.3, line 168; Section 7.1, lines 618--620) is substantive and well-integrated.

#### Response to Referee 3 (Writing) concerns

The Introduction has been reduced from 8 to approximately 6 paragraphs. The Abstract is now split into three paragraphs with clearer structure. The non-sigma coefficients in Table 2 receive substantially expanded discussion (line 407), including economic interpretation of the reasoning sign, tool-call sign flip, and model-age half-life. This addresses one of my R1 Minor Comments as well. The Conclusion (lines 688--692) is tighter and ends with a genuinely bold conjecture about stable oligopolistic structure. Figures 2 and 9 are not modified (acknowledged as deferred), which is acceptable for this round.

#### Response to Referee 4 (Policy) concerns

The three explanations for the cross-firm null (horizontal differentiation, growth-phase masking, information frictions) are now explicitly distinguished (lines 624--632). This was a consensus demand from R1 and R4, and the implementation is clean. The external validity discussion (line 664) now maps findings to three market segments (API developers, enterprise, consumer-facing), as R4 requested. The market definition / SSNIP test request was appropriately dismissed by the editor, and the authors follow this guidance.

#### Response to Red Team concerns

The red team's three killer tests (HonestDiD, capability-overlap classification, date permutation) all remain unimplemented but are honestly flagged. The alternative explanation framework (product life cycle vs. creative destruction) is now incorporated into the pre-trend discussion. The red team's concern about classification endogeneity is addressed in a new Limitations paragraph (line 674).

### Observations on the revision's overall character

The revision is characterized by exceptional intellectual honesty combined with limited computational follow-through. Nearly every textual concern has been addressed -- often with precise, substantive additions that improve the paper's analytical content. But three "Must Fix" computational tasks (HonestDiD, Sun & Abraham, permutation inference) remain unimplemented after a full revision round. The paper effectively contains a series of IOUs for analyses the authors acknowledge are necessary. This is unusual: typically a revision either performs the demanded analysis or argues convincingly that it is unnecessary. This paper does neither -- it agrees the analyses are essential and then does not perform them.

The response letter's characterization of these as "下一轮修改优先事项" (next-round priorities) suggests the authors may have been working under time or computational constraints. The quality of the textual revisions suggests these are capable authors who understand the methodological issues deeply. The question for this review is whether the honest acknowledgment of limitations compensates sufficiently for the missing computations.

My judgment: it does, partially. The paper in its current form is more trustworthy than the R1 version because it does not overclaim. A reader of this revision will correctly understand that the -0.43 coefficient has pre-trend concerns, that sigma = 0.46 is an upper bound, and that the inference is based on few events without distribution-free validation. But a published paper should not contain promissory notes for analyses the author agrees are necessary. The computations must appear before final acceptance.

---

### 逐项评分（更新后）

1. **识别策略可信度: 6.5/10 ↑** (was 5/10) -- The honest reporting of pre-trend t-statistics and the two-interpretation framework (reverse causality vs. anticipation) are substantial improvements. The OLS bias calibration and honest range [0.25, 0.50] for sigma are appropriate. The Oster/simultaneity distinction is now clearly drawn. However, HonestDiD remains unimplemented, and the causal interpretation of -0.43 is still indeterminate. The improvement reflects better honesty, not better identification.

2. **计量模型设定: 7.5/10 ↑** (was 6/10) -- The Hausman-type IV attempt, the bias direction calibration, the reframing of sigma as an upper bound, and the expanded discussion of non-sigma coefficients all improve this dimension. The Oster-vs-simultaneity clarification demonstrates methodological command. The model specification is now presented with appropriate uncertainty rather than false precision.

3. **标准误与推断: 6.5/10 ↑** (was 5/10) -- Pre-trend t-statistics are now reported honestly. The event study is explicitly framed as illustrative. But permutation inference, wild cluster bootstrap, and leave-one-event-out remain unimplemented -- all three were flagged as "Must Fix" by the editor. Firm-level clustering for the nested logit is still not reported alongside model-level clustering. The improvement reflects better reporting and framing, not stronger inference.

4. **稳健性检验: 7.0/10 ↑** (was 6/10) -- The bias calibration for sigma, the Hausman-type IV exploration, the near-unity nesting downgrade, and the expanded robustness discussion are all improvements. The Sun & Abraham estimator remains missing (pre-registered, promised, not delivered). The placebo test and leave-one-firm-out sensitivity are well-presented. The missing staggered-TWFE check limits the score.

5. **统计 vs 经济显著性: 7.5/10 ↑** (was 7/10) -- Already a strength in R1, now enhanced by the economic interpretation of non-sigma coefficients (model-age half-life of 30 days, context-length elasticity, tool-call sign flip explanation), the three-explanation framework for the cross-firm null, and the more careful framing of the structural comparison as "qualitative consistency" rather than "mutual validation."

6. **内生性讨论: 8.0/10 ↑** (was 7/10) -- This is now the paper's strongest methodological dimension. The Oster-vs-simultaneity distinction, the pre-trend two-interpretation framework, the family-upgrade classification endogeneity paragraph, the model deprecation paragraph, and the multihoming discussion collectively represent an unusually thorough and honest treatment of endogeneity. The paper's intellectual integrity on this dimension is genuinely impressive.

---

### 总分: 7.2/10

Improved from 5.8/10 in R1. The revision demonstrates substantial intellectual engagement with every major criticism and produces a paper that is far more honest about its limitations. The 1.4-point improvement reflects genuine analytical contributions (bias calibration, three-explanation framework, Mark I/II integration) and the elimination of misrepresentations (pre-trend claims). The score is held below 7.5 by the unimplemented computational analyses (HonestDiD, Sun & Abraham, permutation inference) that both the editor and this referee flagged as "Must Fix."

---

### 剩余问题

**Must appear before acceptance (Minor Revision items):**

1. **Implement Roth (2022) HonestDiD bias correction.** The textual framework is in place; the computation must follow. If the bias-corrected confidence interval includes zero, the Abstract and Conclusion must be revised accordingly. This is a non-negotiable pre-acceptance requirement.

2. **Implement Sun & Abraham (2021) or Callaway & Sant'Anna (2021) estimator for the family-upgrade specification.** This was pre-registered. The continued absence after two rounds is not acceptable for a published paper. If the robust estimator produces a materially different coefficient, the paper must discuss the discrepancy.

3. **Conduct permutation inference (1,000+ reassignments) and report the permutation p-value for the family-upgrade coefficient.** This is computationally trivial and provides distribution-free inference that does not rely on asymptotic approximations with 43 events.

4. **Conduct leave-one-event-out analysis and report the range of the family-upgrade coefficient.** If 2--3 events drive the result, this must be stated prominently.

**Should address (would strengthen the paper):**

5. Report firm-level clustered standard errors for the nested logit alongside model-level clustering. The R1 results summary showed the SE nearly doubles (from 0.042 to 0.074), which changes the confidence interval for sigma materially.

6. Report the Oster R-max assumption used for the delta = 155 calculation. Standard practice is R-max = 1.3 * R-tilde or min(2 * R-tilde, 1).

7. Address Figures 2 and 9 left-censoring artifacts, at minimum with prominent notes.

8. Wild cluster bootstrap p-values for the family-upgrade coefficient, as a complement to the permutation inference.

---

### 总体建议: MINOR REVISION

The paper has improved substantially from R1 to R2. The textual revisions are thorough, analytically sophisticated, and honest to a degree that is unusual in my reviewing experience. The core descriptive finding -- quality-ladder cannibalization as the dominant mode of demand reallocation -- is clearly stated, appropriately caveated, and robust across the specifications that have been estimated. The Mark I vs. Mark II framing, the three-explanation framework for the cross-firm null, and the OLS bias calibration are genuine analytical contributions that emerged from the revision process.

The paper falls short of acceptance because three specific computational analyses -- all flagged as "Must Fix" by the editor and agreed to by the authors -- remain unimplemented. These are not speculative "nice-to-haves"; they are standard inference procedures that the paper's own text identifies as necessary. The good news is that the intellectual framework for interpreting these analyses is already in the paper, and the textual caveats are strong enough that the computations are unlikely to require major rewriting. The most likely outcomes are: (a) HonestDiD widens the confidence interval but does not eliminate the effect, requiring modest revision of quantitative claims; (b) Sun & Abraham produces a similar coefficient, confirming robustness; (c) permutation inference yields a p-value consistent with the clustered SE, providing reassurance. If any of these produce surprises (e.g., HonestDiD CI includes zero), the paper's existing caveat language is already calibrated for that eventuality.

I recommend Minor Revision with the four "Must appear before acceptance" items above as the binding requirements. If these computations are performed and the results are consistent with the paper's current framing, I would support acceptance. If the HonestDiD correction substantially shrinks the coefficient or the permutation p-value exceeds 0.10, the paper would need to revise its quantitative claims but could still be published with the qualitative finding intact.
