---
## Referee Report -- Round 2 -- Policy & Relevance

**Date**: 2026-03-26
**Paper**: "Creative Destruction in the Market for Intelligence: Demand Reallocation When New LLMs Enter"
**Referee**: 4 (Policy & Relevance)
**R1 Score**: 4.8/10 | **R1 Recommendation**: MAJOR REVISION

---

### 修改评估

**R1 Major Comment 1: The "so what" of no cross-firm displacement needs sharper articulation.**

*R1 request*: Distinguish between (a) genuine horizontal differentiation, (b) growth-phase masking, and (c) information frictions as explanations for the cross-firm null. The paper conflated (a) and (b) and ignored (c).

*Assessment*: **Adequately addressed.** The revised paper introduces all three explanations explicitly in a new Discussion subsection (Section 7.1, blue text). Each explanation is given a paragraph with its own logic and policy implications: horizontal differentiation implies durable fragmentation; growth-phase masking implies eventual consolidation; information frictions imply a role for platform design. The paper also offers a tentative adjudication -- "the combination of near-zero technical switching costs with zero cross-firm displacement is more consistent with horizontal differentiation and growth-phase masking than with information frictions alone" -- which is appropriately hedged given the data limitations. This is a substantial improvement over R1, where the cross-firm null was presented without interpretive structure. The paper still cannot distinguish between these explanations empirically, but acknowledging the question and mapping the policy implications of each is what I asked for.

**R1 Major Comment 2: Pre-trends are concerning and inadequately discussed.**

*R1 request*: Report pre-trend t-statistics prominently; discuss reverse causality; assess whether -0.43 is attenuated or amplified once pre-trends are accounted for.

*Assessment*: **Substantially addressed, with one important gap.** The revised paper now reports the pre-trend t-statistics prominently in Section 6.3 (t = -2.46, -2.05, -2.75), removes the contradictory claim of "no evidence of differential pre-trends," and adds substantive paragraphs on reverse causality and anticipation effects. The HonestDiD correction is acknowledged as unimplemented but flagged as a priority. The Abstract and Conclusion appropriately soften the causal language. The remaining gap: the paper does not attempt even a rough back-of-the-envelope calculation of how much the -0.43 coefficient would shrink under linear extrapolation of the pre-trend. This would be straightforward and would give the reader a sense of whether the 35% figure is likely to survive correction by half, by three-quarters, or entirely. That said, the honest acknowledgment of the problem -- rather than the R1 version's contradiction between text and statistics -- represents a genuine improvement in credibility.

**R1 Major Comment 3: IV failure deserves more attention as a substantive finding.**

*R1 request*: Provide bounds on sigma under plausible assumptions; explore alternative instruments; consider moment inequality approach.

*Assessment*: **Adequately addressed within the scope permitted by the editor.** The revised paper adds three new paragraphs. First, the "Oster bound and simultaneity" paragraph explicitly distinguishes the Oster framework (omitted variables) from the simultaneity concern (mechanical share correlation) -- this was a critical correction. Second, the "Direction and magnitude of OLS bias" paragraph provides a rough calibration (bias of 0.05-0.15, placing true sigma in [0.25, 0.50]) and reports an exploratory Hausman-type IV estimate (sigma ~ 0.35, SE ~ 0.12). Third, the paper repositions 0.46 as an upper bound rather than a point estimate. The editor dismissed my moment inequality suggestion, which I accept. The honest range [0.25, 0.50] is exactly the kind of disclosure I was looking for. At the lower end (0.25), within-firm models are still 33% more substitutable than cross-firm models -- the qualitative conclusion holds.

**R1 Major Comment 4: Market definition is conspicuously absent.**

*R1 request*: Formal SSNIP test or hypothetical monopolist test discussion.

*Assessment*: **Declined per editorial instruction; I accept this.** The editor explicitly dismissed the SSNIP test request as beyond the scope of an empirical demand paper. Re-reading my R1 comment, I acknowledge that requiring a formal antitrust market delineation exercise would indeed change the paper's scope fundamentally. The paper is not an antitrust filing. What the revised paper does provide -- the discussion of near-unity sigma under capability nesting as a "mechanical artifact" rather than evidence of separate markets -- is a reasonable level of engagement with market definition implications. I withdraw this concern.

**R1 Major Comment 5: Family-upgrade classification is endogenous and potentially circular.**

*R1 request*: Sensitivity to alternative classification schemes; report which specific events drive the -0.43 coefficient; discuss classification endogeneity.

*Assessment*: **Partially addressed.** The revised paper adds a new Limitations paragraph on "Family-upgrade classification endogeneity" (Section 7.5) that discusses the strategic nature of naming conventions -- firms label as "upgrades" models designed to replace predecessors, making the classification partly endogenous to expected displacement. The paper notes that a capability-overlap-based classification would be preferable but requires benchmark data not available. However, the leave-one-event-out analysis and the capability-based reclassification are both listed as "future work" rather than implemented. Given that only 43 events drive the core finding, knowing which 3-5 events account for most of the variation is important for assessing robustness. This remains a gap.

---

### Cross-Referee 反馈

**Referee 1 (Field Expert) concerns -- multihoming and discrete-choice mismatch.** The revised paper adds a substantive "Multihoming" paragraph in Discussion (Section 7.1) citing Gentzkow (2007) and explicitly discussing how portfolio allocation is misattributed as preference heterogeneity. This is adequate for a revision; a full multiple-discrete-choice model is properly flagged as future work. From a policy perspective, the multihoming issue matters because it implies the nesting parameter overstates the degree of within-firm "loyalty" -- some of the within-firm correlation is simply developers using multiple models from the same provider for different tasks. The policy implication is that the market may be more contestable than sigma = 0.46 suggests.

**Referee 2 (Methods Expert) concerns -- staggered TWFE, permutation inference.** These are acknowledged but not implemented. The response letter lists HonestDiD, Sun & Abraham, permutation inference, leave-one-event-out, and wild cluster bootstrap as "next-round priorities." From a policy perspective, I note that the paper's quantitative claims now rest on estimates that the authors themselves flag as pending five separate robustness checks. This is an unusual posture for a paper making policy claims. The qualitative finding (within-family displacement dominates) is likely to survive these checks; the quantitative magnitude (35%) is uncertain.

**Referee 3 (Writing Expert) concerns -- Introduction restructuring, redundancy reduction.** The Introduction has been trimmed from 8 to approximately 6 paragraphs. The coefficient-level precision (SEs, Oster bounds) has been removed from the Introduction. The developer-risk paragraph has been moved to Discussion. These are presentation improvements that make the policy claims more appropriately scoped. The Abstract has been split into three paragraphs, which improves readability. The "quality-ladder cannibalization" keyword in the Abstract replaces "creative destruction" as the primary descriptor, which more accurately signals the paper's contribution.

**Red Team concerns.** The three "killer tests" (HonestDiD, capability-overlap classification, permutation inference) remain unimplemented. The revised paper's strategy is to acknowledge all three as necessary, soften all quantitative claims, and defer execution to the next revision. This is defensible as a revision strategy but means the paper's causal and quantitative claims are still provisional.

---

### 逐项评分（更新后）

1. **政策相关性：7.5/10 ↑** (was 6/10)

The three-explanation framework for the cross-firm null (horizontal differentiation / growth-phase masking / information frictions) directly maps onto policy-relevant distinctions. Horizontal differentiation implies antitrust authorities should define narrow markets by provider; growth-phase masking implies the current assessment of market structure may be transient; information frictions imply a role for platforms in reducing search costs. The Mark I vs. Mark II distinction from Aghion & Howitt (1992) is now explicitly invoked, grounding the finding in an established theoretical framework for innovation policy. The external validity paragraph now explicitly maps findings across market segments (API developers, enterprise, consumer-facing), which is exactly what a policymaker needs to assess applicability. The developer-risk paragraph, now in the Discussion rather than the Introduction, provides actionable guidance for application developers. The paper no longer overpromises: "quality-ladder cannibalization" is the framing, not "creative destruction" as a general characterization of market dynamics.

The 1.5-point increase reflects: (a) the three-explanation framework and their distinct policy implications; (b) the Mark I/II theoretical grounding; (c) the explicit external validity mapping; (d) the appropriate scoping of policy claims. I accepted the editor's dismissal of the SSNIP test and EU AI Act requests. The residual gap to a higher score: the paper still does not discuss vertical integration and self-preferencing (Google/Gemini, Microsoft/OpenAI), which are the policy issues where within-firm cannibalization dynamics interact most directly with antitrust enforcement. But this is beyond scope for this paper.

2. **外部有效性：6.0/10 ↑** (was 4/10)

The revised paper substantially expands the external validity discussion. The new "External validity" paragraph in the Policy Implications subsection explicitly maps each finding to three market segments: (i) API developers on OpenRouter (lowest switching costs, directly observed); (ii) enterprise direct-API customers (higher switching costs, within-family upgrades likely extend but with smaller magnitudes); (iii) consumer-facing applications (brand loyalty and UX, different dynamics entirely). The framing of the single-platform analysis as an "upper bound on displacement" is appropriate and gives the reader the correct interpretive lens.

The 2-point increase reflects: (a) the explicit segment-by-segment mapping; (b) the "upper bound" framing; (c) the honest acknowledgment that the cross-firm null may be specific to the growth phase and low-switching-cost environment. The remaining gap: the paper does not provide any quantitative basis for assessing how findings might differ across segments. A sentence like "enterprise switching costs are likely 10-100x higher than OpenRouter's near-zero costs" would help calibrate the reader's priors. But this is a minor concern relative to R1, where the external validity discussion was perfunctory.

3. **机制清晰度：7.0/10 ↑** (was 5/10)

The three-explanation framework for the cross-firm null provides the mechanism discussion I requested. Each explanation has a testable implication: horizontal differentiation implies the null persists as growth slows; growth-phase masking implies displacement emerges when growth decelerates; information frictions imply displacement increases as developers gain experience with rival models. The paper tentatively adjudicates -- "more consistent with horizontal differentiation and growth-phase masking" -- based on the near-zero switching costs observation, which is a reasonable inference.

The within-family mechanism is now grounded in the quality-ladder literature (Aghion & Howitt 1992, Shaked & Sutton 1982, Baron 2020) and the product line management literature (Desai 2001, Draganska & Jain 2005). The Mark II characterization -- incumbents innovating along their own quality ladders -- is a sharp and accurate description of the pattern.

The 2-point increase reflects: (a) the three-explanation framework with distinct testable implications; (b) the theoretical grounding in quality-ladder and product line management literatures; (c) the Mark I vs. Mark II distinction. The residual gap: the paper still cannot empirically adjudicate between explanations, and the classification endogeneity concern means we cannot fully rule out that the family-upgrade "mechanism" is partly a naming artifact.

4. **福利含义：5.5/10 ↑** (was 4/10)

The paper still does not conduct welfare analysis, which remains appropriate given the absence of a supply-side model. However, the revised paper makes progress on the welfare-adjacent questions I raised. The own-price elasticity range (-0.5 to -1.5) is now explicitly reported and benchmarked against Demirer et al. (2025). The developer-risk discussion provides a welfare-relevant insight: developers face upgrade risk more than provider risk, and hedging strategies should focus on within-family compatibility. The closing conjecture in the Conclusion -- "apparent dynamism masks a stable oligopolistic structure" -- raises the efficiency question without overclaiming.

The 1.5-point increase reflects: (a) explicit elasticity reporting; (b) the developer-risk implications; (c) the honest framing of welfare ambiguity in the closing conjecture. The remaining gap: the paper does not discuss whether rapid within-family cannibalization is welfare-improving (consumers get better models faster) or welfare-reducing (innovation investment is directed at incremental upgrades rather than frontier capability expansion). The Arrow (1962) replacement effect is mentioned but its welfare implications are not developed.

5. **研究持久价值：6.5/10 ↑** (was 5/10)

The revised paper better positions its contribution for durability. The "quality-ladder cannibalization" framing, grounded in Aghion & Howitt (1992) and the product line management literature, provides a conceptual contribution that transcends the specific estimates. The three-explanation framework for the cross-firm null establishes a research agenda: future work can test which explanation dominates as the market matures. The Mark I vs. Mark II distinction provides a classification that future papers can update as longer panels become available.

The 1.5-point increase reflects: (a) the more durable conceptual framing; (b) the establishment of a testable research agenda; (c) the explicit positioning as a baseline measurement. The residual gap: the 93-day window remains inherently limiting, and the specific quantitative estimates (0.46, -0.43) are likely to be superseded quickly. The paper's shelf life depends on whether the qualitative patterns -- within-family displacement, cross-firm null -- prove robust in longer panels. The methodological contribution (applying nested logit to LLM markets with the cannibalization decomposition) is the most durable element.

---

### 总分：6.5/10

This represents a 1.7-point improvement from the R1 score of 4.8. The improvement is driven primarily by the three-explanation framework for the cross-firm null (which directly addresses my central R1 concern about the "so what"), the external validity mapping across market segments, the honest treatment of the pre-trend problem, and the appropriate re-scoping of policy claims.

---

### 剩余问题

1. **Unimplemented robustness checks undermine the quantitative claims.** Five analyses flagged as "necessary" remain unimplemented: HonestDiD, Sun & Abraham, permutation inference, leave-one-event-out, and wild cluster bootstrap. Until at least the HonestDiD correction and the permutation inference are executed, the 35% displacement figure is provisional. The paper appropriately signals this, but a paper making policy-relevant claims should ideally implement the checks it identifies as necessary rather than deferring them. From a policy perspective, a policymaker reading this paper cannot take the 35% number at face value.

2. **Back-of-the-envelope pre-trend adjustment.** The paper reports t = -2.75 for the family-upgrade pre-trend but does not attempt even a crude linear extrapolation to estimate how much of the -0.43 post-event coefficient might be attributable to the pre-trend. A rough calculation -- "if the pre-trend continued linearly, approximately X% of the -0.43 coefficient would be attributable to pre-existing decline, leaving a residual displacement of approximately Y" -- would substantially strengthen the reader's ability to assess the finding's magnitude.

3. **Which events drive the result?** The leave-one-event-out analysis is acknowledged as necessary but not executed. With 43 events, knowing whether the result is driven by 3-5 major upgrades (Claude, GPT, Gemini) or is spread across many events matters for generalizability. If the result is driven by 3 events from 2 firms, the policy implications are narrower.

4. **Model deprecation remains unaddressed.** The paper adds a Limitations paragraph acknowledging that some "displacement" may be forced migration from provider-side deprecation. But it does not report how many of the 43 events involve deprecation, which would be feasible to determine from OpenRouter's documentation or model availability data. This matters: forced migration is not the same economic phenomenon as voluntary switching.

5. **Revenue-weighted analysis still absent.** From a policy perspective, request counts weight a $0.14/million-token DeepSeek request identically to a $15/million-token o1 request. The economic significance of displacement depends on revenue reallocation, not request reallocation. The paper flags this as a limitation but does not provide even a rough estimate of revenue-weighted displacement.

---

### 总体建议：MINOR REVISION

The revised paper has addressed the most important concerns from my R1 report. The three-explanation framework for the cross-firm null, the external validity mapping, the honest pre-trend disclosure, the sigma bias calibration, and the re-scoping of policy claims collectively represent a substantial improvement. The paper's policy contribution is now appropriately scoped: it characterizes demand reallocation in one market segment during one phase, maps the findings to policy-relevant distinctions, and honestly identifies what remains unknown.

The reason I recommend MINOR rather than ACCEPT: the paper identifies five robustness checks as "necessary" but implements none of them. For an empirical demand paper, this is acceptable at a working paper stage but would be unusual for a journal submission. The HonestDiD correction, in particular, is straightforward to implement and would resolve the most important remaining uncertainty (whether the 35% figure survives pre-trend correction). The permutation inference is similarly feasible with existing data. I would expect a Minor Revision to implement at minimum HonestDiD and the leave-one-event-out analysis.

The four dimensions at or above 7.5 (policy relevance at 7.5) meet the threshold; the two below 7.5 (external validity at 6.0, welfare implications at 5.5, durability at 6.5) reflect structural features of the data and research design that cannot be fully resolved through revision. No dimension is below 6.0, which clears the "still needs work" threshold. The paper is close to publishable; one more round of implementing the flagged robustness checks would bring it there.
