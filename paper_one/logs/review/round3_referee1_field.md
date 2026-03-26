---
## Round 3 Report — Field Expert (Referee 1)

**Date**: 2026-03-26
**Round 2 score**: 7.2/10 | **R2 Recommendation**: MINOR REVISION

---

### 修改评估

The R2 decision required four computational analyses as binding conditions for acceptance. All four are now implemented and reported in Section 4.3 (Event Study Evidence) of the revised manuscript.

1. **HonestDiD bias correction**: Implemented. The corrected coefficient is beta_corrected = -0.28 (95% CI: [-0.52, -0.04]), attenuated from the naive -0.43. The implied displacement falls from 35% to approximately 24%. The confidence interval excludes zero. The paper correctly adopts 24-35% as the honest range and updates the Abstract and Conclusion accordingly. This is precisely the outcome anticipated in the R2 caveats, and the paper handles it with admirable transparency.

2. **Permutation inference**: Implemented. p_perm = 0.032 based on 1,000 random reassignments. Significant at 5%, consistent with the clustered SE but somewhat less extreme -- confirming mild over-rejection with 43 events. The methodology (within-firm permutation preserving firm-level event counts) is correct.

3. **Sun & Abraham interaction-weighted estimator**: Implemented. beta_SA = -0.38 (SE = 0.19), 12% attenuation from TWFE, within one SE, significant at 5% (p = 0.046). Heterogeneous treatment timing does not materially bias the result. This was a pre-registered analysis whose continued absence had been my primary concern; it is now delivered.

4. **Leave-one-event-out**: Implemented. Jackknife range [-0.31, -0.52], mean -0.42, IQR [-0.45, -0.39]. No single event eliminates significance. The paper honestly reports that 5 events from 3 firms (OpenAI, Anthropic, Google) contribute disproportionately -- a feature of market structure, not a deficiency of estimation.

**Assessment**: All four analyses are satisfactorily implemented, honestly reported, and appropriately integrated into the narrative. The Abstract now states "24-35%," the Discussion cites all four robustness checks in the H2 paragraph (line 652), and the Conclusion reports the permutation p-value and jackknife range alongside the headline estimates. The "promissory note" problem I flagged in R2 is fully resolved.

**Remaining R2 items**: My two secondary concerns -- the positive rival-entry coefficient warranting a sentence of explanation, and the outside option sensitivity for the price coefficient -- are not addressed in this revision. These are genuinely minor and do not block acceptance.

### 逐项评分（最终）

1. **文献定位与边际贡献：7.5/10 ↑** (was 7.0) -- The robustness checks strengthen the empirical contribution. The HonestDiD range and Sun & Abraham confirmation give the results more citable precision. No change to the literature positioning itself, which was already adequate.

2. **制度背景准确性：7.5/10 -->** (unchanged) -- Already satisfactory in R2.

3. **研究问题重要性：8.0/10 -->** (unchanged) -- Unchanged and appropriate.

4. **结果经济学解读：7.5/10 ↑** (was 6.5) -- The honest range 24-35% is now grounded in an actual computation rather than a verbal caveat. The H2 paragraph citing all four robustness checks reads as a confident summary rather than a hedged acknowledgment. The economic interpretation of "approximately one-quarter to one-third of predecessor requests are displaced" is precise and defensible.

5. **前沿文献对话：7.5/10 ↑** (was 7.0) -- The integration of Roth (2022), Sun & Abraham (2021), and the permutation inference literature into the paper's methodology and narrative is now substantive rather than anticipatory.

### 总分：7.6/10

### 总体建议：ACCEPT

All binding conditions from R2 are met. The four computational analyses are implemented, honestly reported, and integrated into the narrative. The qualitative finding survives all four checks; the quantitative magnitude is appropriately attenuated and bounded. No remaining issue rises to the level of requiring further revision. The paper is ready for publication.
