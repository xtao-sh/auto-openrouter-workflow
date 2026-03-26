---
## Editorial Letter — Round 1

**Date**: 2026-03-26
**Paper**: "Creative Destruction in the Market for Intelligence: Demand Reallocation When New LLMs Enter"

### 编辑总评

This paper studies demand reallocation following new LLM model entry on OpenRouter, a multi-provider API aggregation platform. Using daily data on 385 models from 66 firms over 93 days (December 2025--March 2026), the authors estimate a Berry (1994) nested logit demand model and conduct descriptive panel regressions with event studies around entry events. The headline finding is that creative destruction operates almost exclusively through within-family upgrades -- when a firm releases a successor in the same product family, the predecessor loses roughly 35% of daily requests -- while cross-firm entries produce no detectable displacement. The OLS nesting parameter of 0.46 indicates moderate within-firm substitution.

The paper has genuine strengths. The research question is timely and important. The three-channel decomposition (cannibalization, displacement, expansion) is a clean and useful framework. The combination of structural and reduced-form approaches is sensible for a setting where clean causal identification is unavailable. And the authors display unusual honesty about what their evidence can and cannot establish -- the candid treatment of the IV failure, the descriptive framing of the panel regressions, and the forthright limitations section are commendable. All four referees and the red team acknowledged these virtues.

However, the paper has three first-order problems on which all reviewers converge. First, the pre-trend t-statistics for the family-upgrade event study (t = -2.75) are statistically significant, directly contradicting the paper's repeated claim of "no evidence of differential pre-trends." This is a credibility issue that must be resolved before any revision can be evaluated. Second, the OLS nesting parameter sigma = 0.46 lacks a credible identification strategy: the IV produces an out-of-range estimate (sigma = -0.15), and the Oster bound does not address the specific simultaneity concern at issue. Third, the "creative destruction" framing substantially overpromises relative to what the evidence -- within-family cannibalization on a single platform during a 93-day growth phase -- can deliver. The revision must address all three problems head-on.

### 审稿人共识（Consensus Issues）

**共识 1: 显著的前趋势未被报告，且与论文的文本陈述直接矛盾**

- **问题**: The results summary file reports pre-trend t-statistics of -2.46 (same-firm), -2.05 (cross-firm), and -2.75 (family upgrade), all significant or near-significant at the 5% level. Yet the paper claims "no evidence of differential pre-trends" and states that "pre-event coefficients are noisy but centered near zero." For the family-upgrade specification -- the paper's core finding -- t = -2.75 implies predecessor models were already declining before the upgrade event. This undermines the -0.43 coefficient and raises the possibility of reverse causality (declining usage triggering successor release).
- **来源**: Referee 2 (Major Comment 1), Referee 4 (Major Comment 2), Red Team (Assumption 1, Killer Test 1)
- **编辑判断**: Must Fix — non-negotiable
- **建议方向**: (a) Report the pre-trend test statistics prominently in the paper, not in auxiliary files. (b) Implement Roth (2022) HonestDiD bias correction to provide a corrected confidence interval for the family-upgrade coefficient under the assumption that pre-trends continue. (c) Explicitly discuss reverse causality: does declining predecessor usage trigger successor release? (d) If the bias-corrected coefficient includes zero or shrinks below -0.15, the paper must substantially revise its quantitative claims.

**共识 2: OLS sigma = 0.46 缺乏可信的识别策略**

- **问题**: The within-firm share ln(s_{m|g,t}) is mechanically correlated with the error term through simultaneous determination of market shares. The BLP instrument (product-line breadth) produces sigma = -0.15, outside the parameter space, confirming severe endogeneity. The paper defaults to OLS and leans on the Oster bound (delta = 155), but the Oster framework addresses omitted variable bias from unobservables correlated with observables -- not the mechanical simultaneity in share equations. This is a methodological mismatch.
- **来源**: Referee 1 (Major Comment 3), Referee 2 (Major Comment 2), Referee 4 (Major Comment 3), Red Team (Assumption 2)
- **编辑判断**: Must Fix
- **建议方向**: (a) Discuss the sign and expected magnitude of OLS bias formally -- the upward bias from positive demand shocks is well-understood and even a rough calibration would be informative. (b) Attempt alternative instruments: Hausman-type instruments (average within-firm share in other time periods), leave-out shares excluding model m from its firm's total, or characteristics of other firms' models. (c) If no valid instrument can be found, provide an honest range for sigma under plausible assumptions about bias direction and magnitude, rather than treating 0.46 as a precise point estimate. (d) Acknowledge explicitly that the Oster bound does not address simultaneity bias.

**共识 3: "创造性毁灭"框架与证据不匹配**

- **问题**: The paper's title and framing invoke Schumpeterian creative destruction, which implies cross-firm competitive displacement. What the paper actually documents is within-family cannibalization -- a firm's successor replacing its own predecessor -- with zero cross-firm effects. This is closer to product line management or planned obsolescence than to creative destruction. The 93-day window during a 20% growth phase further limits the scope of the claim.
- **来源**: Referee 1 (Major Comment 2), Referee 4 (Major Comment 1), Red Team (Final Judgment, point 3)
- **编辑判断**: Must Fix
- **建议方向**: The authors have two options. Option A (preferred): Reframe around "product line cannibalization" and "quality ladder dynamics," which accurately describe the evidence. This does not require a title change if the authors restructure the narrative to emphasize that creative destruction in this market, surprisingly, operates only along the vertical/intra-firm dimension. Option B: Retain the creative destruction framing but seriously engage with the Schumpeter Mark I vs. Mark II distinction and explain why the absence of cross-firm displacement is or is not consistent with the concept. Either way, the paper must explicitly distinguish between the three competing explanations for the cross-firm null: (i) genuine horizontal differentiation, (ii) growth-phase masking, (iii) information frictions. Currently the paper conflates (i) and (ii) and ignores (iii).

**共识 4: Alternative nesting results (sigma > 0.99) are mechanical artifacts**

- **问题**: With only 2 nests (reasoning vs. non-reasoning) or 4 nests (price quartiles), the within-group share varies enormously due to heterogeneity within groups. The near-unity sigma estimates are driven by mechanical correlation between model size and within-group share, not by genuine within-group substitution. Yet the paper draws substantive conclusions from these estimates.
- **来源**: Referee 1 (Major Comment 4), Referee 2 (Major Comment 4), Red Team (Final Judgment, point 4)
- **编辑判断**: Must Fix
- **建议方向**: Either (a) drop these results entirely and present only the firm-based nesting, or (b) demonstrate that the results survive with more granular nests (8-10 capability-price cells) and estimate a multi-level nested logit (capability tier > firm) to properly separate the margins. Under no circumstances should the paper draw policy conclusions from near-unity sigma estimates under coarse nesting.

**共识 5: Family-upgrade result relies on very few events, and no permutation inference is conducted**

- **问题**: Only 43 upgrade events drive the key finding, and the event study uses only 8 events with full pre/post windows. Standard asymptotic inference may be unreliable with so few effective clusters. The event study confidence intervals span roughly 8 log points, making the figure uninformative.
- **来源**: Referee 1 (Major Comment 5), Referee 2 (Major Comment 3), Red Team (Killer Test 3, Sensitivity Test 1)
- **编辑判断**: Must Fix
- **建议方向**: (a) Conduct permutation inference: randomly reassign the 43 upgrade dates within each firm and re-estimate the coefficient 1,000+ times. (b) Report wild cluster bootstrap p-values. (c) Conduct leave-one-event-out analysis to identify which specific upgrades drive the result. (d) Report individual event-level plots for the 3-5 largest upgrade events. (e) Redesign or downgrade the event study figure -- with 8 events and 8-log-point confidence intervals, it is illustrative at best.

**共识 6: Discrete-choice framework is inconsistent with multihoming behavior**

- **问题**: The nested logit assumes each request represents a discrete choice by a separate consumer. On OpenRouter, developers routinely send requests to multiple models simultaneously for A/B testing, fallback routing, and task-specific allocation. This misattributes within-developer portfolio allocation as between-developer preference heterogeneity and inflates the nesting parameter.
- **来源**: Referee 1 (Major Comment 1), Referee 4 (Minor Comment 2), Red Team (implicitly, through the external validity discussion)
- **编辑判断**: Should Address
- **建议方向**: (a) Provide evidence on multi-model usage patterns in the data (e.g., what fraction of requests come from models that are the sole model used in their firm on a given day?). (b) Discuss explicitly how multihoming affects the interpretation of sigma. (c) At minimum, acknowledge this as a limitation with a substantive discussion of the direction and likely magnitude of bias. A full multiple-discrete-choice model (e.g., Gentzkow 2007) is beyond the scope of a revision but should be flagged as the appropriate future extension.

**共识 7: Staggered TWFE estimator promised in the identification memo is not implemented**

- **问题**: The pre-analysis plan and identification memo list Sun & Abraham (2021) as a planned robustness check. It does not appear in the paper. With 43 upgrade events at different dates and potentially heterogeneous treatment effects, TWFE bias could be substantial for the family-upgrade specification.
- **来源**: Referee 2 (Major Comment 5), Referee 1 (Missing Literature: Sun & Abraham 2021)
- **编辑判断**: Must Fix
- **建议方向**: Implement the Sun & Abraham (2021) interaction-weighted estimator or Callaway & Sant'Anna (2021) for the family-upgrade specification. This was pre-registered and its omission is a deviation from the stated analysis plan.

### 分歧与编辑裁决（Disagreements & Editorial Judgment）

**分歧 1: Severity of the external validity concern**

- **分歧**: Referee 3 (Writing, 6.6/10) treats external validity as a secondary issue and considers the paper essentially publication-ready after presentation fixes. Referee 4 (Policy, 4.8/10) views external validity as a fundamental flaw that limits the paper's contribution to near zero for policy purposes, arguing that OpenRouter's self-selected developer population tells us almost nothing about enterprise customers.
- **编辑裁决**: I side partially with Referee 4 on the substance but not the severity. The external validity limitation is real and consequential -- the paper studies the lowest-switching-cost segment of the market, and the cross-firm null may not generalize to enterprise customers with fine-tuning investments, compliance requirements, and organizational inertia. However, I do not agree that this renders the paper unpublishable. The paper should: (a) substantially expand the discussion of external validity, explicitly mapping each finding to its generalizability across market segments (OpenRouter API developers, enterprise direct-API customers, consumer-facing applications); (b) frame the single-platform analysis as a lower bound on switching frictions rather than a characterization of the entire market; and (c) reduce the scope of policy claims to what the evidence supports. This is a revision requirement, not a basis for rejection.

**分歧 2: Whether the paper needs welfare analysis and market definition**

- **分歧**: Referee 4 argues the paper needs formal market definition (SSNIP test) and welfare analysis to fulfill its policy promise. Referee 1 and Referee 3 evaluate the paper as an empirical IO contribution that need not include welfare analysis.
- **编辑裁决**: I side with Referees 1 and 3. The paper is an empirical demand analysis, not an antitrust filing. Requiring formal market definition and welfare analysis would change the paper's scope fundamentally. However, the paper should either (a) scale back its policy framing to match its empirical scope, or (b) include a brief discussion of market definition implications of its findings (the near-unity sigma under capability nesting, if it survives scrutiny, has market definition implications). The authors should not be required to conduct welfare analysis.

**分歧 3: Whether the Introduction is too long or appropriately detailed**

- **分歧**: Referee 3 argues the Introduction is too front-loaded and should not report coefficients, following the Autor-Dorn-Hanson model of building tension. The current standard in empirical IO and applied micro, however, is to preview results in the Introduction -- see recent AER/QJE publications in demand estimation.
- **编辑裁决**: I partially side with Referee 3. The Introduction is too long at 8 paragraphs and reports results with excessive precision (standard errors, Oster bounds). But I disagree that coefficients should be entirely withheld. The compromise: reduce to 5-6 paragraphs, report key magnitudes without standard errors or robustness metrics, and move the developer-risk paragraph to the Discussion. Save the Oster bound and nesting comparisons for the Results section.

**分歧 4: How seriously to take the "concordance" between sigma = 0.46 and the panel coefficient of -0.43**

- **分歧**: The paper presents the numerical similarity as "mutual validation." Referee 1 argues this is coincidental because the two quantities measure fundamentally different things. Referee 2 is more neutral, noting it as a strength in the "statistical vs. economic significance" dimension.
- **编辑裁决**: I agree with Referee 1. The nesting parameter sigma measures preference correlation across all same-firm models continuously, while the panel coefficient measures the discrete displacement effect of a specific type of entry event. Their numerical proximity is suggestive but not a formal validation. The paper should tone down the "mutual validation" language and instead note that both approaches point in the same qualitative direction (within-firm substitution is the primary margin), without claiming that the numerical similarity is informative.

### 编辑附加意见

1. **Figures 2 and 9 contain left-censoring artifacts that are misleading.** Figure 2 (HHI) shows concentration crashing from ~10,000 to ~600 in the first two weeks -- an artifact of the panel starting with few observed models. Figure 9 shows 300+ "new models" in week 1 for the same reason. These figures, presented without explanation, will mislead readers. Start the time series after the initial loading period (January 2026) or add prominent notes. (Raised by Referee 3 and Referee 4 independently.)

2. **The paper should discuss model deprecation in the family-upgrade specification.** Some of the 43 upgrade events may involve provider-side deprecation of the predecessor, which is forced migration rather than voluntary switching. The paper should report how many upgrade events involve explicit deprecation and test whether the -0.43 coefficient differs between deprecation and non-deprecation events.

3. **Revenue-weighted analysis would strengthen the paper.** Request counts treat a cheap request identically to an expensive one. A revenue-weighted or token-volume-weighted analysis would be more informative for understanding economic significance. The token robustness check is a start but not sufficient.

4. **The paper should cite and engage with the product line management literature** (Desai 2001, Draganska & Jain 2005), the quality-ladder growth literature (Aghion & Howitt 1992 foundational paper), the multihoming demand literature (Gentzkow 2007), and the platform economics literature (Hagiu & Wright 2015). These are not obscure references -- they are directly relevant to the paper's core findings and current framing.

### 驳回的意见（Dismissed）

1. **Referee 4's request for formal SSNIP test / hypothetical monopolist test**: Dismissed. This is an empirical demand paper, not a merger review document. The paper should discuss market definition implications informally but is not required to implement antitrust market delineation tools. This would change the paper's scope beyond what is reasonable for a revision.

2. **Referee 4's request for engagement with the EU AI Act and FTC investigations**: Dismissed. While these are important policy developments, requiring the paper to address specific regulatory proceedings would date the paper rapidly and is not necessary for an economics journal. A brief mention in the policy discussion is sufficient.

3. **Referee 4's suggestion of moment inequality approach for sigma**: Dismissed as impractical. Moment inequality methods require strong institutional assumptions about the direction of bias and are computationally demanding. The simpler alternatives (honest bounds, alternative IVs) are more appropriate.

4. **Referee 3's suggestion to delete the roadmap paragraph entirely**: Partially dismissed. The roadmap is conventional in the field and costs only one sentence. Shortening it is fine; deleting it is not required.

5. **Referee 4's request for analysis of open-source vs. closed-source competitive dynamics as separate nesting structures**: Dismissed as beyond scope. This is a good idea for a separate paper but would substantially expand the current paper's already-complex empirical framework.

### 修改优先级清单

**Must Fix (required for the revision to be re-reviewed favorably)**

1. Report pre-trend test statistics in the paper; implement Roth (2022) HonestDiD bias correction for the family-upgrade event study. If the corrected coefficient includes zero, substantially revise quantitative claims. [Consensus 1]

2. Provide honest bounds on sigma under plausible assumptions about simultaneity bias. Attempt at least one alternative IV strategy. Stop citing the Oster bound as addressing the simultaneity concern. [Consensus 2]

3. Implement Sun & Abraham (2021) or Callaway & Sant'Anna (2021) robust estimator for the family-upgrade specification, as pre-registered. [Consensus 7]

4. Conduct permutation inference for the family-upgrade coefficient (1,000+ random reassignments of upgrade dates). Report wild cluster bootstrap p-values. [Consensus 5]

5. Reframe the paper's narrative: either adopt "product line cannibalization and quality ladder dynamics" or provide a serious engagement with Schumpeter Mark I vs. Mark II to justify the creative destruction framing. Explicitly distinguish between horizontal differentiation, growth-phase masking, and information frictions as explanations for the cross-firm null. [Consensus 3]

6. Drop or substantially downgrade the alternative nesting results (sigma > 0.99). Do not draw substantive conclusions from near-unity estimates under coarse nesting. If retained, demonstrate robustness with more granular nests. [Consensus 4]

7. Conduct leave-one-event-out analysis for the family-upgrade coefficient. Report which specific upgrade events drive the result. [Consensus 5]

**Should Address (expected in the revision)**

8. Discuss multihoming and its implications for the nested logit framework. Provide evidence on multi-model usage patterns if available. Cite Gentzkow (2007). [Consensus 6]

9. Restructure the Introduction: reduce to 5-6 paragraphs, remove coefficient-level precision (standard errors, Oster bounds), move developer-risk paragraph to Discussion. [Referee 3, Major Comment 1]

10. Provide substantive discussion of Table 2 non-sigma coefficients (reasoning dummy sign, tool-call flipping, model-age economic magnitude). [Referee 3, Major Comment 3]

11. Fix Figures 2 and 9 to address left-censoring artifacts. [Referee 3 Major Comment 4, Referee 4 Minor Comment 1]

12. Expand external validity discussion: map each finding to its generalizability across market segments (API developers, enterprise, consumer-facing). [Referee 4, Disagreement 1]

13. Reduce redundancy of key results (-0.43 reported 6 times, 0.46 reported 5+ times). Each section should add interpretive value, not restate numbers. [Referee 3, Major Comment 2]

14. Engage with missing literature: Desai (2001), Draganska & Jain (2005), Aghion & Howitt (1992), Gentzkow (2007), Hagiu & Wright (2015), Santos Silva & Tenreyro (2006), Zheng et al. (2024). [Referee 1, Missing Literature]

15. Discuss family-upgrade classification endogeneity: naming conventions are strategic and may correlate with expected displacement. Consider sensitivity to capability-overlap-based classification. [Referee 4 Major Comment 5, Red Team Killer Test 2]

**Consider (would improve the paper but not required)**

16. Replace ln(requests + 1) with Poisson pseudo-maximum-likelihood (PPML) as a robustness check. [Referee 1 Minor Comment 4, Red Team Sensitivity Test 2]

17. Report how the price coefficient and implied elasticities vary with the outside option assumption (not just sigma). [Referee 1, Major Comment 6]

18. Report firm-level clustered standard errors for the nested logit alongside model-level clustering. [Referee 2, Minor Comment — SE nearly doubles]

19. Strengthen the Conclusion: advance a bold interpretation rather than recapitulating the Introduction. [Referee 3, Major Comment 6]

20. Discuss model deprecation: how many of the 43 upgrade events involve forced migration? [Referee 2, Minor Comment 6]

21. Address AI writing artifacts: reduce ternary enumeration, excessive hedging, meta-commentary, and over-symmetric sentence structures. [Referee 3, AI Writing Check]

22. Consider sensitivity of the family-upgrade coefficient to alternative window lengths (3, 14, 30 days). [Red Team, Sensitivity Test 3]

23. Provide a sample reconciliation table showing which filters produce which sample sizes (29,084 vs. 30,903 vs. 26,444). [Referee 1, Minor Comment 1]

### 总体决策：MAJOR REVISION

The paper addresses a genuinely important question about competitive dynamics in the LLM market with a well-conceived dual empirical strategy. The core descriptive finding -- that within-family upgrades are the primary channel of demand reallocation -- is plausible and potentially valuable to the empirical IO literature. However, three of four referees recommend Major Revision, the average score is 5.85/10, and the red team identifies serious vulnerabilities in the paper's causal claims.

The pre-trend issue is the most urgent: the paper's text and its own test statistics are in direct contradiction, and this must be resolved before any other element of the revision can be evaluated. The identification of sigma, the framing of the contribution, and the scope of policy claims all require substantial work. That said, the paper's intellectual honesty, the quality of the institutional description, and the interest of the research question provide a solid foundation for revision. I invite the authors to resubmit a revised manuscript that addresses all "Must Fix" items and the majority of "Should Address" items. The revised paper will be sent back to the original referees.
