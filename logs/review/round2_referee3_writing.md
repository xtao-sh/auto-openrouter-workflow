---
## Referee Report -- Round 2 -- Presentation Specialist

**Date**: 2026-03-26
**Paper**: "Creative Destruction in the Market for Intelligence: Demand Reallocation When New LLMs Enter"

### 修改评估

**R1 Major Comment 1: Restructure the Introduction (8 paragraphs to 5--6; remove coefficient precision; move developer-risk to Discussion).**

Assessment: **Adequately addressed.** The Introduction has been reduced from 8 to 7 substantive paragraphs (lines 59--73). The developer-risk paragraph has been moved to the Discussion (line 636), as requested. The empirical preview (lines 67) no longer reports standard errors or the Oster bound -- it previews the magnitudes but defers the precision metrics to the Results section. The contribution paragraph (line 69) is tighter and better structured. The limitation paragraph (line 71) is direct and effective -- the opening sentence "Several limitations bound our conclusions" is a clean replacement for the former "We are explicit about what this paper does not do."

However, the Introduction is still slightly long. The limitation paragraph (line 71) could be shorter -- it runs to roughly 5 lines of material that all reappears in Section 7. More importantly, the phrase "a remarkable menu" (line 59) survives despite my Minor Comment 2 requesting its removal. This is a judgment call by the authors ("remarkable" does describe a 400-model menu), but I note that a factual adjective would be more precise.

Verdict: The revision accomplishes the substantive goal. The Introduction now builds toward the findings rather than front-loading them.  ↑

---

**R1 Major Comment 2: Reduce redundancy of key results (-0.43 and 0.46 reported too many times).**

Assessment: **Partially addressed.** The language "mutual validation" has been replaced with "qualitative consistency" (line 489), which is a genuine improvement. The structural comparison paragraph (line 489) now explicitly cautions against over-interpreting the numerical proximity, directly responsive to my concern and the editor's ruling on this point.

However, a count through the revised paper reveals that the family-upgrade coefficient of -0.43 still appears in: the Abstract (line 43, as "roughly 35%"), the Introduction (line 67, as "roughly 35%"), Results Panel A discussion (line 479), the economic significance paragraph (line 485), the structural comparison paragraph (line 489), the Discussion economic interpretation (line 618, as "roughly one-third"), the Discussion H2 assessment (line 652), and the Conclusion (line 688, implicitly). That is approximately 7--8 mentions. The response letter claimed "reduced repetition," but the count has increased by one relative to the original. To be fair, several of these now add interpretive value that was absent in R1 (the Discussion now contextualizes the number within the Mark I/II framework rather than merely restating it), so the quality of the repetitions has improved even if the quantity has not.

The nesting parameter 0.46 appears in: the Abstract (line 45), the Introduction (line 67), Table 2 (line 381), the discussion of Table 2 (line 397), the alternative nesting comparison (implicit), the Discussion (line 634), and the bias bounds paragraph (line 405, as "[0.25, 0.50]"). This is roughly 6 mentions, down from the original count, and the bias discussion adds genuine value.

Verdict: The interpretive quality of repetitions has improved, but the raw count remains higher than necessary. One more pass to consolidate would help.  →

---

**R1 Major Comment 3: Provide substantive discussion of Table 2 non-sigma coefficients.**

Assessment: **Well addressed.** The Table 2 discussion (line 407) has been substantially expanded with blue text. The revision now explains: (a) that the negative reasoning dummy likely reflects collinearity with price ("developers value reasoning but not at any price" -- a crisp formulation); (b) that the tool-call sign flip between logit and nested logit reflects firm-level confounding absorbed by sigma; (c) that the model-age coefficient implies a roughly 18% decline in the share ratio over 30 days, which is economically interpretable. The own-price elasticity range ($-0.5$ to $-1.5$) is now reported and benchmarked against Demirer et al.

This is a significant improvement. The paragraph still runs long (roughly 12 lines of dense text), and some sentences try to do too much work (the tool-call discussion packs three ideas into one sentence), but the substantive content is correct and informative.

Verdict: The revision delivers what was requested. The Table 2 discussion is now among the stronger paragraphs in the paper.  ↑

---

**R1 Major Comment 4: Address the Figure 2 and Figure 9 artifacts.**

Assessment: **Not adequately addressed.** The response letter states "Partially Accept: acknowledge problem, next round add annotation or truncation." The revised paper has not added annotations to Figure 2 (line 712) or Figure 9. The figure notes remain unchanged from R1: Figure 2 (line 715) merely states the averages without flagging the initial spike, and there is no Figure 9 in the revised paper's appendix at all (the entry dynamics figure appears to have been removed or was never included -- I note the appendix includes Figures 1, 2, 5, 10, 12, 13, 14 but not 9).

If Figure 9 has been removed, this partially resolves the concern for that figure, but Figure 2 still shows HHI starting near 10,000 and crashing, and the note says nothing about the left-censoring artifact. A reader encountering Figure 2 would still reasonably conclude that market concentration fell dramatically -- which is an artifact, not an economic phenomenon.

Verdict: This issue remains unresolved.  →

---

**R1 Major Comment 5: Reconsider the event study figure for family upgrades (Figure 16, wide CIs, only 8 events).**

Assessment: **Adequately addressed.** The revised paper repositions the event study figure as illustrative rather than confirmatory (line 530: "should be interpreted with these caveats in mind"), adds new paragraphs on pre-trends (line 518), HonestDiD (line 522), Sun & Abraham (line 524), permutation inference (line 526), and leave-one-event-out (line 528). The figure note (line 513) now explicitly states "only 8 predecessor models have at least 14 pre-event and 30 post-event days" and acknowledges "wide confidence intervals." The pre-trend test statistics are prominently reported ($t = -2.75$ for family upgrade).

This is a substantial improvement. The paper now handles the figure honestly: it presents it as directional evidence while explicitly flagging the pre-trend concern, the small N, and the wide CIs. The candid acknowledgment that HonestDiD, Sun & Abraham, permutation inference, and leave-one-event-out are all necessary but unimplemented is commendably transparent, though it also means the core quantitative finding remains on probation.

Verdict: The framing is now appropriate. The figure still does not visually support the narrative, but the text no longer asks it to.  ↑

---

**R1 Major Comment 6: Strengthen the Conclusion.**

Assessment: **Well addressed.** The Conclusion (lines 688--692) has been reduced from 5 paragraphs to 3, each with a distinct function: (1) summary of the descriptive finding with explicit caveats; (2) three priorities for future research that are specific and actionable (HonestDiD, longer panels, direct-API data); (3) a closing conjecture that advances beyond the Introduction. The final conjecture -- "the LLM market's apparent dynamism masks a stable oligopolistic structure -- one in which firms compete fiercely with their former selves while coexisting comfortably with their rivals" -- is genuinely provocative and memorable. This is the kind of ending I called for in R1.

The sentence "Whether this equilibrium is efficient, or whether it reflects insufficient cross-firm competitive pressure, is a question the current data cannot answer but that the rapid evolution of this market will soon make testable" closes the paper with forward-looking intellectual substance rather than the anodyne "much remains to be learned" of the original.

Verdict: This is one of the strongest improvements in the revision.  ↑

---

### Cross-Referee 反馈

**Referee 1 (Field Expert):** The revised paper adds Desai (2001), Draganska & Jain (2005), Aghion & Howitt (1992), Gentzkow (2007), Hagiu & Wright (2015), Santos Silva & Tenreyro (2006), and Zheng et al. (2024) -- all seven literatures that Referee 1 flagged as missing. The product line management paragraph (line 105) integrates Desai and Draganska substantively rather than as perfunctory citations. The multihoming paragraph (line 638) engages seriously with Gentzkow and connects it to the nesting parameter interpretation. The creative destruction framing has been softened to "quality-ladder cannibalization" in the Abstract and Discussion, responsive to Referee 1's Major Comment 2. From a presentation standpoint, this literature integration is well-executed: the new paragraphs are placed logically and do not bloat the Related Literature beyond its appropriate scope.

**Referee 2 (Econometrician):** The revision adds paragraphs on pre-trend reporting (line 518), Oster bound limitations (line 403), OLS bias direction and magnitude (line 405), Sun & Abraham (line 524), and permutation inference (line 526). These are among the most important new additions to the paper's credibility. From a writing perspective, these paragraphs are well-structured: each states the concern, describes the methodology, reports what has been done (or acknowledges what has not), and states the implication. The bias calibration paragraph (line 405) is particularly well-written -- it provides a "rough calibration" with a concrete range ([0.25, 0.50]) rather than hand-waving. The transparency about unimplemented analyses is handled with appropriate directness ("We have not yet implemented this correction, which represents an important limitation").

**Referee 4 (Policy):** The revision adds three explanations for the cross-firm null (horizontal differentiation, growth-phase masking, information frictions) at lines 624--632, directly responsive to Referee 4's Major Comment 1 about the "so what" of the null. The external validity discussion (line 664) now maps findings to specific market segments (API developers, enterprise, consumer-facing), which was Referee 4's core concern. From a presentation perspective, the three-explanation structure is clear and well-differentiated -- each gets its own italicized subheading, and the policy implications of each are sketched. The family-upgrade classification endogeneity concern (line 674) is new and responsive to Referee 4's Major Comment 5.

**Red Team:** The pre-trend reporting (line 518), the OLS bias discussion (lines 403--405), the Mark I vs. Mark II framing (line 168 in theory, line 620 in discussion), and the reframing to "quality-ladder cannibalization" all respond to core red team concerns. The paper now acknowledges, with unusual candor, that its causal claims are on probation until HonestDiD, Sun & Abraham, and permutation inference are implemented.

---

### AI 写作痕迹（更新评估）

**Ternary enumeration:** Reduced but not eliminated. The three-channel decomposition (cannibalization, displacement, expansion) remains, appropriately, as it is analytically motivated. The three hypotheses (H1, H2, H3) remain, also appropriate. The three cross-firm null explanations (lines 624--632) are a new ternary structure, but each is substantively distinct, so this is defensible. The three future research priorities in the Conclusion (line 690) are appropriately grouped. However, "Three contributions" (line 69) and the three limitation paragraphs given most weight could still be varied. The overall ternary density has decreased. Improved.

**Excessive hedging:** Substantially reduced. The Abstract (line 43) now states "the predecessor loses roughly 35% of daily requests" rather than "is associated with approximately 35% fewer daily requests." The Conclusion's closing conjecture is assertive. However, some hedging remains in places where it is now justified by the pre-trend caveats: "is associated with" (line 479), "may reflect" (line 632). Given the paper's honest acknowledgment that causal identification is lacking, the remaining hedging is appropriate rather than excessive. Improved.

**Meta-commentary:** Largely eliminated. "We are explicit about what this paper does not do" is gone. "H2 receives strong support" has been replaced with substantive language ("the data confirm the quality-ladder prediction" is gone too -- replaced with "the family-upgrade coefficient of -0.43 compared to the different-family coefficient of zero aligns with the vertical differentiation prediction," line 652, which is better but still somewhat formulaic). The "framed with appropriate caution" clause in the Policy section is gone. The Limitations subsection (lines 668--682) is now weighted by importance, with "No causal identification" receiving the longest treatment, as I suggested. Improved.

**Over-symmetric sentence structures:** Improved. The three cross-firm null explanations (lines 626--631) are still symmetric in structure (each gets an italicized heading and a 3-sentence paragraph), but the content varies in length and specificity. The hypothesis-mapping paragraph (lines 650--654) is less rigidly parallel than in R1. Still present but less jarring.

**Boilerplate connectors:** "Two patterns stand out" (line 561) survives. The roadmap paragraph (line 73) survives per the editor's ruling, though it has been shortened. "Several features of the data warrant attention" has been replaced. "Much remains to be learned" has been replaced with the conjecture. Net improvement.

**Perfectly parallel limitation lists:** The Limitations section (lines 668--682) is now appropriately weighted, with "No causal identification" receiving roughly 8 lines and shorter limitations like "Short panel" and "No supply-side model" receiving 2--3 lines each. This is a clear improvement over the uniformly-sized paragraphs of R1. Improved.

Overall: The AI writing artifacts are meaningfully reduced. The paper reads more like a human-authored academic paper than in R1. The remaining ternary structures are mostly analytically motivated, the hedging is now proportionate to the paper's honest uncertainty about its causal claims, and the meta-commentary is largely gone. The prose is not yet at the level of the best AER papers, but it is within the range of competent empirical IO working papers.

---

### 逐项评分（更新后）

1. **叙事结构与故事性：7.5/10 ↑** (was 7/10) -- The narrative has been substantively improved. The Mark I vs. Mark II framing provides a theoretical scaffold that was missing in R1. The three explanations for the cross-firm null add interpretive depth. The Conclusion's closing conjecture gives the paper a memorable landing. The story no longer peaks in the Introduction; the Discussion section now adds genuine intellectual value through the competing-explanations framework and the Mark II interpretation. The remaining issue is that the results section still largely confirms what the Introduction previews -- but this is now within acceptable norms for applied micro papers, and the caveats about pre-trends add genuine tension.

2. **逻辑连贯性：8/10 →** (was 8/10) -- Remains the paper's strongest dimension. The revision adds logical coherence in the form of the Mark I/II framework, the three cross-firm null explanations, and the honesty about pre-trends. The connection between the structural and reduced-form estimates is now appropriately caveated ("qualitative consistency" rather than "mutual validation"). One minor new tension: the paper prominently reports that its own pre-trend tests fail, then asks the reader to take the quantitative estimates seriously -- this is honest but logically uncomfortable. The paper handles it by explicitly downgrading the estimates to "informative descriptive statistics" (line 668), which is the right move.

3. **语言质量：7/10 ↑** (was 6/10) -- The most improved dimension. Hedging is now proportionate. Meta-commentary is largely gone. The Abstract is restructured into three clear paragraphs. The prose is more direct: "the predecessor loses roughly 35% of daily requests" rather than "is associated with approximately 35% fewer daily requests." The new paragraphs (OLS bias discussion, pre-trend reporting, three explanations for the null) are well-written. Ternary enumeration persists where analytically motivated but is no longer the default rhetorical structure. Some sentences remain overly long (the tool-call discussion in line 407 tries to do too much), and "remarkable menu" (line 59) still feels evaluative rather than factual. But the overall quality of the prose has visibly improved.

4. **Introduction 质量：7.5/10 ↑** (was 6.5/10) -- The restructuring is effective. Developer-risk is moved to the Discussion. The empirical preview now reports magnitudes without standard errors or Oster bounds. The contribution paragraph is more focused. The limitation paragraph is direct and honest. The roadmap is shorter. The Introduction is still slightly long (7 paragraphs rather than my suggested 5--6), but each paragraph now serves a clear purpose. The first three paragraphs remain strong (the question, the channels, the economic stakes). The remaining weakness is "a remarkable menu" in the opening sentence.

5. **表格图表：6/10 ↑** (was 5.5/10) -- Modest improvement. The event study figure is now appropriately framed as illustrative. The alternative nesting results are explicitly labeled as mechanical artifacts (line 563). The Table 2 discussion is substantially expanded. However, Figure 2 (HHI) still lacks annotation for the left-censoring artifact. The event study figure still has 8-log-point confidence intervals. Figure 13 (sigma robustness) still uses a bar chart rather than the dot-and-whisker format I suggested. The improvements are primarily in the textual treatment of figures rather than in the figures themselves.

6. **整体可读性：7.5/10 ↑** (was 7/10) -- The paper is more readable than in R1. The new Discussion paragraphs are well-organized and substantive. The Limitations section is weighted by importance. The Conclusion is tighter and more memorable. The new literature paragraphs are well-placed and do not disrupt flow. The main drag on readability is now the density of caveats in the Results section: the new paragraphs on pre-trends, HonestDiD, Sun & Abraham, permutation inference, and leave-one-event-out -- while individually necessary and well-written -- collectively run to over 40 lines of blue text that interrupt the flow of the empirical narrative. This is a temporary issue that will resolve when the analyses are actually implemented.

---

### 总分：7.2/10

The paper has improved meaningfully from the R1 score of 6.6. The narrative reframing around quality-ladder cannibalization and Mark I/II is a genuine intellectual contribution. The language quality has improved visibly. The Introduction and Conclusion are both stronger. The Discussion now adds interpretive value rather than merely recapitulating results. The main residual weaknesses are: (a) the Figure 2 artifact remains unaddressed; (b) the key results are still slightly over-repeated; and (c) the long sequence of "not yet implemented" paragraphs in the Results section, while honest, creates a temporarily awkward reading experience.

---

### 剩余问题

1. **Figure 2 (HHI) left-censoring artifact.** This was flagged in R1, acknowledged in the response letter as "Partially Accept," and remains unchanged in the manuscript. The figure note still does not explain the HHI crash from ~10,000 to ~600 in the first two weeks. A one-sentence note ("The initial spike in HHI reflects the small number of models observed in the first days of the panel and does not represent a genuine change in market concentration") would resolve this. This is a minor fix but it should not persist to a third round.

2. **"Remarkable menu" (line 59).** A minor but symptomatic issue: "remarkable" is the author's evaluation, not a factual description. Replace with a factual adjective or delete. This was flagged as Minor Comment 2 in R1 and remains unchanged.

3. **Redundancy count.** The -0.43 / 35% figure still appears approximately 7--8 times. One pass to consolidate (removing the re-statement in the Discussion H2 paragraph and the Conclusion, or at minimum varying the phrasing) would tighten the paper.

4. **"Two patterns stand out" (line 561).** This boilerplate connector survives from R1. Replace with a substantive transition.

5. **Unimplemented analyses.** The honest acknowledgment of HonestDiD, Sun & Abraham, permutation inference, and leave-one-event-out as unimplemented is appropriate and necessary. But from a presentation standpoint, these four separate paragraphs (lines 522--528) read as a list of IOUs rather than as analysis. When these analyses are implemented in the next revision, the "not yet implemented" framing should be replaced with actual results, and the presentation will improve substantially as a byproduct.

---

### 总体建议：ACCEPT (conditional on minor fixes)

The paper has addressed the substance of my six R1 Major Comments. The Introduction is restructured (MC1 -- addressed). The redundancy is reduced in interpretive quality if not in count (MC2 -- partially addressed, not a blocking issue). Table 2 discussion is expanded (MC3 -- well addressed). The event study figure is reframed (MC5 -- addressed). The Conclusion is rewritten with a memorable closing (MC6 -- well addressed). The one outstanding item is Figure 2's left-censoring artifact (MC4 -- not addressed), which requires only a one-sentence note.

The AI writing artifacts are substantially reduced. The prose reads as competent human-authored academic economics. The remaining ternary structures are analytically motivated. The hedging is proportionate to the paper's genuine uncertainty. The meta-commentary is largely eliminated.

From a pure presentation standpoint, all dimensions now score at or above 7/10, and the overall score of 7.2 is within the range I would consider acceptable for a working paper headed toward a good field journal. The methodological concerns raised by Referees 1 and 2 (pre-trends, identification, permutation inference) remain serious and are the binding constraint on publication -- but those are not within my remit as the Presentation Specialist. What I can say is that the paper now presents its evidence, caveats, and limitations with appropriate clarity and honesty, and the writing quality no longer stands in the way of publication.

My recommendation is **ACCEPT** conditional on: (1) adding the Figure 2 annotation, (2) one final pass to reduce the remaining result redundancy, and (3) replacement of the "not yet implemented" framing with actual results once the statistical analyses are complete. Items (1) and (2) are minor fixes that do not require re-review. Item (3) is contingent on the other referees' assessments of the methodological implementation.
