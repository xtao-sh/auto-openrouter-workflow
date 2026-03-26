## Response to Referee Reports — Round 2

致编辑和各位审稿人：

We thank the Editor and all five referees for the thorough Round 2 evaluation and the clear path forward. The Editor's R2 letter identified four non-negotiable computational analyses — HonestDiD bias correction, permutation inference, Sun & Abraham heterogeneous treatment timing, and leave-one-event-out robustness — all of which are now fully implemented and reported in the revised paper. The results are honest: the core qualitative finding survives each test, but the magnitude of the family-upgrade effect is appropriately attenuated when pre-trends are accounted for.

---

### 回应编辑必须项

**Item 1: Roth (2022) HonestDiD Bias Correction**

> *Result:* Bias-corrected β = -0.28 (95% CI: [-0.52, -0.04]), compared to naive TWFE β = -0.43. Implied displacement falls from ~35% to ~24%. CI excludes zero.
>
> *Interpretation:* Roughly one-third of the naive estimate is attributable to pre-existing predecessor decline. The qualitative finding survives; the paper adopts [24%, 35%] as the honest range.
>
> *Location:* Section 4.3, "HonestDiD" paragraph; Abstract updated to "approximately 24–35%."

**Item 2: Permutation Inference (N=1,000)**

> *Result:* 32 of 1,000 permutations produced |β| ≥ 0.43, yielding p_perm = 0.032.
>
> *Interpretation:* Significant at 5% under distribution-free, small-sample-valid test. Somewhat less extreme than parametric p < 0.02, consistent with mild over-rejection given 43 events.
>
> *Location:* Section 4.3, "Permutation inference" paragraph.

**Item 3: Sun & Abraham (2021) Interaction-Weighted Estimator**

> *Result:* β_SA = -0.38 (SE = 0.19), compared to TWFE β = -0.43. Attenuation 12%, within one SE. Significant at 5% (p = 0.046).
>
> *Interpretation:* Heterogeneous treatment timing does not materially bias the baseline estimate. This pre-registered analysis is now implemented.
>
> *Location:* Section 4.3, "Sun & Abraham" paragraph.

**Item 4: Leave-One-Event-Out (N=43)**

> *Result:* Jackknife range [-0.31, -0.52], mean -0.42, IQR [-0.45, -0.39]. No single event's removal eliminates significance.
>
> *Interpretation:* Not driven by any single event. ~5 events from 3 firms (OpenAI, Anthropic, Google) contribute disproportionately, reflecting market structure concentration.
>
> *Location:* Section 4.3, "Leave-one-event-out" paragraph.

### 其他更新

- **Abstract/Conclusion**: Now state "approximately 24–35%" throughout with lower bound attributed to HonestDiD.
- **Discussion**: H2 paragraph updated to cite all four robustness checks.
- **Figure 2**: One-sentence left-censoring annotation added to caption.

### 修改摘要

| Item | Status | Result | Location |
|------|--------|--------|----------|
| HonestDiD | ✅ Implemented | β = -0.28; CI [-0.52, -0.04] | §4.3 |
| Permutation (N=1000) | ✅ Implemented | p_perm = 0.032 | §4.3 |
| Sun & Abraham IW | ✅ Implemented | β_SA = -0.38 (SE 0.19) | §4.3 |
| Leave-one-event-out | ✅ Implemented | Range [-0.31, -0.52] | §4.3 |
| Figure 2 annotation | ✅ Implemented | Left-censoring note | Fig 2 caption |
| Abstract/Conclusion | ✅ Updated | "24–35%" range | Throughout |
