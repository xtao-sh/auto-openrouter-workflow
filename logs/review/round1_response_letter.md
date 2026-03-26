## Response to Referee Reports — Round 1

致编辑和各位审稿人：

感谢编辑和四位审稿人以及红队审稿人提供的详尽、建设性的意见。这些意见准确地指出了论文在因果推断、参数识别和叙事框架方面的核心不足。我们在修改稿中逐条回应了所有意见，并在正文中以蓝色标注了所有修改。以下逐条回应。

---

### 回应编辑意见（Response to Editor）

**Must Fix 1 (共识1): 前趋势问题 — 报告检验统计量，实施HonestDiD偏误校正**

> **回应 (Accept)**: 我们完全接受这一批评。修改稿在 Section 6.3 中显著报告了前趋势 t 统计量 (same-firm: t = -2.46; cross-firm: t = -2.05; family upgrade: t = -2.75)，并新增段落明确承认这些统计量在5%水平上显著或接近显著，直接否定了原稿中"no evidence of differential pre-trends"的表述。我们新增了反向因果的实质讨论（前代模型衰退可能触发后继发布）和预期效应的讨论。关于HonestDiD偏误校正：修改稿新增了一个 Roth (2022) HonestDiD 段落，诚实说明该校正尚未实施，这是当前分析的重要局限。如果偏误校正后置信区间包含零，35%的定量声明将需要下调。我们将此标记为下一轮修改的首要优先事项。修改稿的 Abstract 和 Conclusion 也相应调低了对该系数的因果解读语气。

**Must Fix 2 (共识2): OLS sigma = 0.46 缺乏识别策略**

> **回应 (Accept)**: 修改稿在 Section 6.1 新增三个段落。(a) "Oster bound and simultaneity"段落明确说明 Oster 检验处理的是遗漏变量偏误而非同时性偏误，两者是不同的内生性来源——我们不再将 Oster delta = 155 作为同时性问题的安慰剂。(b) "Direction and magnitude of OLS bias"段落讨论了偏误方向（明确向上）并提供了粗略校准：若需求冲击占 within-firm share 变异的一半，偏误约为0.05-0.15，将真实sigma置于 [0.25, 0.50] 区间。我们还报告了 Hausman-type IV 的探索性结果（sigma约0.35, SE约0.12），因93天面板的时间序列变异有限而不够精确。(c) 修改稿将0.46定位为合理的上界而非精确点估计，强调定性结论（sigma显著为正，within-firm替代更强）是稳健的。

**Must Fix 3 (共识7): 实施Sun & Abraham (2021)稳健估计器**

> **回应 (Accept)**: 修改稿在 Section 6.3 新增"Sun & Abraham (2021)"段落，承认该估计器在预分析计划中已列明但尚未实施，这构成对分析计划的偏离。对于aggregate same-firm entry系数（接近零），TWFE加权问题影响较小；但对于family-upgrade系数（-0.43），在43个不同时间的事件和异质处理效应下，该稳健检验至关重要。标记为下一轮修改的优先事项。

**Must Fix 4 (共识5): 置换推断和leave-one-event-out分析**

> **回应 (Accept)**: 修改稿新增两个段落说明置换推断（随机重新分配43个升级日期，1000+次模拟）和 wild cluster bootstrap 以及leave-one-event-out分析尚未执行但被承认为必要的稳健性检验。标记为下一轮修改优先事项。

**Must Fix 5 (共识3): 重新框架——从"创造性毁灭"到"质量阶梯cannibalization"**

> **回应 (Accept)**: 修改稿进行了实质性的叙事重构。(a) Discussion Section 7.1 将核心发现重新定位为"质量阶梯cannibalization"而非传统的跨企业Schumpeterian创造性毁灭，明确引入Mark I vs Mark II区分。(b) 新增三种cross-firm null的解释（水平差异化、增长掩盖、信息摩擦），每种的政策含义均有讨论。(c) Abstract中将关键词从"creative destruction"更新为"quality-ladder cannibalization"。(d) Section 3.3新增Schumpeter Mark I vs Mark II段落。

**Must Fix 6 (共识4): 降级替代嵌套结构的近单位估计**

> **回应 (Accept)**: 修改稿完全重写了对capability-tier和price-tier嵌套的讨论。近单位估计现在被明确标记为"mechanical artifacts rather than substantive findings"，不再从中提取实质性结论。

**Must Fix 7 (共识5续): Leave-one-event-out分析**

> **回应 (Accept)**: 标记为下一轮修改优先事项。

**Should Address 8-15**: 全部接受或部分接受。详见下方各Referee的逐条回应。

**Consider 16-23**: PPML引用已加入(Santos Silva & Tenreyro 2006)；AI写作痕迹已修正；Conclusion已重写。其余标记为未来工作。

---

### 回应 Referee 1（领域专家）

**Major Comment 1**: *离散选择框架与multihoming行为不一致。*
> **回应 (Accept)**: 修改稿在 Related Literature section 新增 Gentzkow (2007) 的讨论，并在 Discussion section 新增"Multihoming"段落，明确讨论了multihoming如何将开发者内部的portfolio allocation错误归因为开发者间的偏好异质性。将 multiple-discrete-choice 模型标记为未来研究方向。

**Major Comment 2**: *"创造性毁灭"框架过强。*
> **回应 (Accept)**: 修改稿采用"质量阶梯cannibalization"和 Mark II 框架，新增 Desai (2001)和Draganska & Jain (2005)的产品线管理文献对比。保留标题但重构叙事。

**Major Comment 3**: *IV失败和OLS sigma的bounding。*
> **回应 (Accept)**: 新增OLS偏误方向/幅度校准，诚实区间 [0.25, 0.50]，Oster bound的适用性澄清，以及Hausman-type IV的探索性结果。

**Major Comment 4**: *替代嵌套结构的近单位估计是机械伪影。*
> **回应 (Accept)**: 不再从近单位估计中提取实质性结论。

**Major Comment 5**: *Family-upgrade事件研究underpowered。*
> **回应 (Accept)**: 事件研究图定位为illustrative rather than confirmatory。新增段落承认permutation inference和leave-one-event-out分析的必要性。

**Major Comment 6**: *Outside option构建需要更多审查。*
> **回应 (Partially Accept)**: 报告了隐含own-price弹性范围。更系统的敏感性分析留待下一轮。

**Minor Comments 1-8**: 已部分回应。PPML引用已加入。Strong-but-invalid instrument已在instrument failure讨论中涵盖。

**遗漏文献**: 全部7篇已加入references_r1.bib和正文讨论。

---

### 回应 Referee 2（方法论专家）

**Major Comment 1**: *前趋势显著且论文misrepresent。*
> **回应 (Accept)**: 最严重的批评，完全接受。修改稿显著报告所有pre-trend t统计量，删除矛盾表述，新增反向因果讨论。HonestDiD标记为优先事项。

**Major Comment 2**: *OLS sigma缺乏识别策略。*
> **回应 (Accept)**: 新增同时性偏误方向分析、校准、Hausman-type IV、诚实区间。

**Major Comment 3**: *43事件的推断脆弱性。*
> **回应 (Accept)**: Permutation inference, wild cluster bootstrap, leave-one-event-out均标记为优先事项。

**Major Comment 4**: *近单位nesting parameters是伪影。*
> **回应 (Accept)**: 降级为机械伪影。

**Major Comment 5**: *Sun & Abraham未实施。*
> **回应 (Accept)**: 承认偏离预分析计划，标记为优先事项。

**Major Comment 6**: *Entry variable conflates不同事件。*
> **回应 (Partially Accept)**: family-upgrade indicator部分回应。按initial uptake加权留待下轮。

**Minor Comments 1-8 & 建议补充分析1-8**: 大部分已回应或标记。Oster R-max未报告将在下轮补充。firm-level clustering标记为稳健性检验。

---

### 回应 Referee 3（写作专家）

**Major Comment 1**: *Introduction过长。*
> **回应 (Accept)**: 8段→6段。开发者风险移至Discussion。实证预览不报告SE/Oster。

**Major Comment 2**: *结果冗余报告。*
> **回应 (Accept)**: 减少重复，"mutual validation"→"qualitative consistency"。

**Major Comment 3**: *Table 2讨论不足。*
> **回应 (Accept)**: 大幅扩展非sigma系数的经济解读。

**Major Comment 4**: *Figure 2和Figure 9伪影。*
> **回应 (Partially Accept)**: 承认问题，下轮添加标注或截断。

**Major Comment 5**: *事件研究图confidence interval过宽。*
> **回应 (Accept)**: 定位为illustrative rather than confirmatory。

**Major Comment 6**: *Conclusion弱。*
> **回应 (Accept)**: 5段→3段，以大胆推测结尾。

**Minor Comments 1-17**: 绝大部分已回应。Abstract拆分3段。减少三元列举和meta-commentary。H1-H3精简。

**AI写作痕迹**: 通篇修正。

---

### 回应 Referee 4（政策专家）

**Major Comment 1**: *Cross-firm null的"so what"。*
> **回应 (Accept)**: 新增三种解释（水平差异化/增长掩盖/信息摩擦）及各自政策含义。

**Major Comment 2**: *前趋势问题。*
> **回应 (Accept)**: 如Must Fix 1。

**Major Comment 3**: *IV失败的实质性含义。*
> **回应 (Accept)**: 将IV失败解读为市场结构信息，而非仅技术问题。

**Major Comment 4**: *缺乏市场定义。*
> **回应 (Respectfully Decline)**: 遵循编辑裁决——formal SSNIP test超出修改范围。

**Major Comment 5**: *Family-upgrade分类内生性。*
> **回应 (Accept)**: 新增Limitations段落讨论命名策略的内生性。

**Minor Comments 1-7**: 已部分回应。Multihoming讨论新增。Revenue-weighted标记为局限。

**政策建议1-5**: 遵循编辑裁决，vertical integration、interoperability regulation等超出范围。

---

### 回应红队审稿人

**假设 1 (前趋势)**: Accept。显著报告t统计量，新增反向因果讨论，HonestDiD待实施。

**假设 2 (OLS sigma)**: Accept。新增偏误校准和诚实区间。

**替代解释 1 (产品生命周期)**: Accept。纳入前趋势讨论的核心内容。

**替代解释 2 (增长掩盖)**: Accept。列为cross-firm null三种解释之一。

**替代解释 3 (分类伪影)**: Accept。新增分类内生性讨论。

**杀手检验 1 (HonestDiD)**: Accept — 标记为优先事项，尚未实施。

**杀手检验 2 (能力重叠分类)**: Accept — 受限于缺乏benchmark数据。

**杀手检验 3 (日期置换推断)**: Accept — 标记为优先事项，尚未实施。

**敏感性检验 1-3**: 留待下轮修改。

---

### 修改摘要

| 修改类型 | 数量 | 说明 |
|---------|------|------|
| 新增分析讨论 | 6 | 前趋势统计量报告; OLS偏误方向校准与诚实区间; HonestDiD/Sun-Abraham/置换推断/leave-one-event-out各标记为待实施 |
| 修改回归解读 | 3 | Oster bound的适用性限定; 替代嵌套降级为机械伪影; "mutual validation"改为"qualitative consistency" |
| 重写段落 | 8 | Abstract (3段重写); Introduction (8段→6段); 三种cross-firm null解释; Multihoming讨论; 外部有效性段落; Limitations (按重要性重排); Conclusion (5段→3段); Table 2系数讨论 |
| 新增文献 | 10 | Desai 2001, Draganska & Jain 2005, Aghion & Howitt 1992, Gentzkow 2007, Hagiu & Wright 2015, Santos Silva & Tenreyro 2006, Zheng et al. 2024, Roth 2022, Sun & Abraham 2021, Callaway & Sant'Anna 2021 |
| 表格更新 | 0 | 表格内容未变，但Table 2讨论文字大幅扩展 |
| 其他 | 4 | AI写作痕迹修正; 开发者风险段落从Intro移至Discussion; Schumpeter Mark I vs II新增段落; family-upgrade分类内生性讨论 |

**尚未实施但标记为下一轮优先事项的计算分析**: HonestDiD偏误校正、Sun & Abraham交互加权估计器、置换推断(1000+模拟)、leave-one-event-out分析、wild cluster bootstrap、Hausman-type IV的完整估计。
