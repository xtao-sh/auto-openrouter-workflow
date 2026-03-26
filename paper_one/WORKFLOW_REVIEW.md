# WORKFLOW_REVIEW — 多智能体学术同行评审工作流

> **版本**：v1.2 (2026-03-26)
> **定位**：WORKFLOW_v2 的下游流程。论文初稿完成（通过 Gate 4）后启动。
> **目标**：模拟 Top Tier 经济学期刊（AER / AEJ / QJE / REStud）的 R&R 流程，通过多轮多角度评审迭代提升论文质量。
> **领域**：时政经济学 / 政治经济学（Political Economy）

---

## 设计哲学

### 为什么不是"所有意见都改"？

真实的 R&R 流程中，作者需要：
1. **区分意见的权重**：Major concern vs. minor suggestion vs. 审稿人的个人偏好
2. **判断可行性**：有些建议在数据/方法约束下无法实现
3. **识别矛盾意见**：不同审稿人可能给出相反建议
4. **写 Response Letter**：逐条回应，接受的解释怎么改了，拒绝的解释为什么

本工作流模拟这个完整过程，不是简单的"审→改→审→改"。

### 对标标准

以下期刊的审稿标准作为参考锚点：
- **AER**：强调因果识别、理论贡献、政策相关性
- **AEJ: Economic Policy / Applied Economics**：实证扎实、政策导向、清晰的 identification
- **QJE**：高度创新、强叙事、big question
- **REStud**：方法论严谨、理论与实证结合

---

## 增强机制

### A. Adversarial Referee（红队审稿人）

在第二轮或第三轮引入一位**红队审稿人**，专门寻找论文的致命弱点：

- 如果换一个合理的 specification，核心结果还在吗？
- 如果放松某个识别假设，结论还成立吗？
- 数据中有没有被忽略的异常模式可以推翻主要发现？
- 有没有一个简单的替代解释能 rationalize 所有结果？

**触发条件**：当第一轮 Referee 2（方法论专家）的"识别策略可信度"评分 < 7.0 时，自动在第二轮引入红队审稿人。也可由 Editor 主动决定引入。

**Red Team Referee System Prompt**：
```
你是一位以挑战论文核心结论著称的审稿人。你的任务不是全面审查，而是集中攻击论文最薄弱的环节。

你的思路：
1. 找出论文最依赖的 1-2 个假设
2. 构造反例或替代解释来挑战这些假设
3. 提出具体的"杀手检验"——如果做了这个检验且结果不支持，论文的核心主张就不成立
4. 评估作者是否在 cherry-pick specification

输出格式：
---
## Red Team Report

### 论文最薄弱的假设
[识别 1-2 个，详细说明为什么薄弱]

### 替代解释
[提出至少 2 个能解释同样结果的替代故事]

### 杀手检验（Killer Tests）
[提出 2-3 个具体的检验，如果结果不支持则论文有问题]

### Specification Sensitivity
[建议 2-3 个合理的替代 specification，预测结果是否稳健]

### 综合评估：论文能否经受住挑战？[Yes/No/Partially]
---
```

### B. Cross-Referee Discussion（审稿人交叉讨论）

模拟 REStud 等期刊的机制：在第二轮评审时，让复审人看到**所有第一轮的 Referee Report**（不仅是自己的）。

**执行方式**：
- R2 的 Referee 收到的材料包中额外包含所有 R1 报告
- Referee 在 R2 报告中需要额外回应：
  - "我同意/不同意其他审稿人的哪些意见？"
  - "我认为编辑对分歧的裁决是否合理？"

这能提升审稿质量——看到其他人的意见后，审稿人可能发现自己忽略的问题，也可能修正自己过于苛刻或宽松的评判。

### C. Desk Reject 预筛机制

**在第一轮正式评审前**，由 Editor Agent 做一轮快速预筛（5 分钟）：

检查清单：
- [ ] 论文是否有明确的研究问题？
- [ ] 识别策略是否有根本性缺陷？
- [ ] 数据是否能支撑研究问题？
- [ ] 论文长度是否达标（≥ 10,000 字）？
- [ ] LaTeX 是否成功编译？
- [ ] 核心表格是否完整？

如果任何一项有根本性问题 → **Desk Reject**，打回 WORKFLOW_v2 补救，不浪费 Referee 的 token。

### D. Response Letter 质量审查

Editor 在将 Response Letter 转交复审人之前，先评估其质量：

- 是否逐条回应了所有 Major Comments？
- 拒绝的意见是否有充分论证？
- 修改是否落实到了论文中的具体位置？
- 是否有"打太极"嫌疑（表面回应但实质未改）？

如果 Response Letter 质量不达标 → 要求作者（主 Agent）重写后再提交复审。

### E. 量化改进追踪（Improvement Dashboard）

每轮修改后自动生成改进仪表盘，保存到 `logs/review/improvement_dashboard.md`：

```
## Improvement Dashboard — Round [N] vs Round [N-1]

### 评分变化
| Referee | R[N-1] 总分 | R[N] 总分 | 变化 |
|---------|-----------|---------|------|
| R1 | X.X | X.X | +X.X |
| ... | ... | ... | ... |

### 修改统计
- 文本变化量：[新增/删除/修改的字数]
- 新增分析：[列出]
- 新增文献：[列出]
- 表格更新：[列出]

### Major Comments 解决率
- 总计：[N] 条
- 已解决：[N] 条（[X]%）
- 部分解决：[N] 条（[X]%）
- 未解决：[N] 条（[X]%）

### 质量趋势
[简要评估论文质量是否在持续改善]
```

### F. 异步并行优化

**可并行的环节**：
- 4 个 Referee 的评审（完全独立）
- 分析层修改与写作层修改的部分工作（如：跑新回归的同时修改非数据相关的段落）

**必须串行的环节**：
- 编辑决策必须在所有 Referee Report 到齐后
- Response Letter 必须在编辑决策后
- 新回归结果必须先出来，才能更新论文中的数字

---

## Agent 行为规范（从 WORKFLOW_v2 继承）

### ⚠️ 长文档分步生成规则（关键！）

**禁止一次性生成整篇文档。** 所有长文本输出必须分步生成：

1. **LaTeX 论文修改**：按章节逐步修改，每次只处理一个 section：
   - Step 1: 修改 Abstract + Introduction → 确认无误
   - Step 2: 修改 Literature / Background → 确认无误
   - Step 3: 修改 Theoretical Framework → 确认
   - ...以此类推
2. **Response Letter**：按 Referee 分段撰写，不要一次性输出全部回应
3. **Referee Report 保存**：每份报告独立保存为单独文件，不要合并

**硬性上限**：任何超过 3000 字的文档（LaTeX、markdown、代码）都应分段写入。

**理由**：一次性生成 10,000+ 字的内容会超出单次输出限制，导致截断和进程崩溃。分步生成既安全又便于质量控制。

### 🔒 不可修改原始文件（Immutability Rule）

**Review 阶段禁止直接修改原始初稿和代码。** 所有修改必须在新版本副本中进行。

**论文版本管理**：
- `paper/main.tex` — 原始初稿（**只读，不可修改**）
- `paper/main_r1.tex` — 第一轮修改后的版本
- `paper/main_r2.tex` — 第二轮修改后的版本
- `paper/main_r3.tex` — 第三轮修改后的版本（如有）
- `paper/main_final.tex` — 最终版本

**代码版本管理**：
- `code/` 目录下的原始脚本（**只读，不可修改**）
- `code/review_r1/` — 第一轮新增或修改的分析脚本副本
- `code/review_r2/` — 第二轮新增或修改的分析脚本副本
- `code/review_r3/` — 第三轮（如有）

**表格和图表版本管理**：
- `output/tables/` — 原始表格（**只读**）
- `output/tables_r1/` — 第一轮更新的表格
- `output/tables_r2/` — 第二轮更新的表格
- `output/figures/` — 原始图表（**只读**）
- `output/figures_r1/` — 第一轮更新的图表
- `output/figures_r2/` — 第二轮更新的图表

**辅助文档同理**：
- `output/research_design.md` → `output/research_design_r1.md`
- `output/identification_memo.md` → `output/identification_memo_r1.md`

**好处**：
- 可以横向对比每个阶段的内容变化
- 如果某轮修改效果不好，可以回退到上一版本
- 便于评估改进幅度（配合 Improvement Dashboard）

### 📋 Git 版本控制

**项目根目录** (`Auto_OpenRouter/`) 必须初始化 Git 仓库，在关键节点自动 commit。

**Commit 节点（必须执行）**：

| 时间节点 | Commit Message 格式 |
|---------|-------------------|
| Review 流程启动前 | `review: init — snapshot before peer review` |
| 每位 Referee Report 保存后 | `review: R[N] referee[X] report saved` |
| Editorial Letter 保存后 | `review: R[N] editorial letter` |
| 每轮修改完成后 | `review: R[N] revision complete — [修改摘要]` |
| Response Letter 保存后 | `review: R[N] response letter` |
| 最终决策后 | `review: final decision — [ACCEPT/CONDITIONAL ACCEPT/END]` |

**Commit 执行方式**：
```bash
cd /path/to/Auto_OpenRouter
git add -A
git commit -m "review: R1 referee1 report saved"
```

**分支策略（简单模式）**：
- 所有工作在 `main` 分支上进行（不需要复杂分支）
- 通过 commit 历史和文件版本后缀（`_r1`, `_r2`）双重追踪
- 如需对比：`git diff <commit1> <commit2> -- paper/` 即可看到论文变化

### 📝 日志完整性要求

**所有 Referee Report 必须完整保存为独立文件**，格式为 Markdown（`.md`）。

保存规则：
1. **文件名规范**：`logs/review/round[N]_referee[X]_[role].md`
2. **内容完整性**：包含完整的评分、Major/Minor Comments、总体建议
3. **时间戳**：每份报告开头记录生成时间
4. **不可追溯修改**：一旦保存，Referee Report 不可修改（如需更正，另存新文件并注明）

**汇总文件**（方便快速查阅）：
- `logs/review/score_tracker.md` — 每轮评分汇总
- `logs/review/referee_status.md` — Referee 状态追踪
- `logs/review/improvement_dashboard.md` — 改进仪表盘
- `logs/review/revision_changelog.md` — 每轮修改的具体内容清单

`revision_changelog.md` 格式：
```
## Round 1 修改日志

### 分析层修改
- [x] 新增 placebo test — `code/review_r1/08_placebo_test.py`
- [x] 补充异质性分析（按模型大小分组） — `code/review_r1/09_hetero_size.py`

### 写作层修改
- [x] 重写 Introduction 第 1-3 段 — `paper/main_r1.tex` Section 1
- [x] 补充 Discussion 中的机制讨论 — `paper/main_r1.tex` Section 7

### 表格/图表更新
- [x] 新增 Table A3 — `output/tables_r1/table_a3_placebo.csv`
- [x] 更新 Figure 2 — `output/figures_r1/fig2_event_study.pdf`

### 文献更新
- [x] 新增 5 篇引用 — `paper/references_r1.bib`

### Git Commit
- Commit: `abc1234` — "review: R1 revision complete — added placebo test, rewrote intro"
```

---

## 审稿人团队（Referee Panel）

### Referee 1 — 领域专家（Field Expert）

**角色**：研究 AI/平台经济/产业组织的资深学者，熟悉 LLM 市场相关文献。

**关注重点**：
- **文献定位**：是否准确把握了文献脉络？遗漏了关键论文？
- **边际贡献**：相对于 Fradkin (2025)、Demirer et al. (2025) 等已有工作，贡献是否足够？
- **制度细节**：对 LLM API 市场、OpenRouter 平台的描述是否准确？是否遗漏了影响识别的制度特征？
- **经济学直觉**：结果是否有合理的经济学解释？是否与行业实际一致？
- **前沿对话**：是否与该领域最新进展（working papers、会议论文）有充分对话？

**System Prompt**：
```
你是一位专注于数字经济、平台经济和产业组织的资深经济学家，在 AER/AEJ 发表过多篇论文。你被邀请为一篇关于 LLM API 市场的实证论文撰写审稿报告。

你的审稿风格：
- 对文献定位极其敏感——你知道这个领域谁在做什么
- 重视经济学直觉——不接受"回归跑出来是显著的"就完事
- 关注制度细节——市场机制的描述必须准确
- 建设性但直率——指出问题同时给出可行的改进方向

审稿维度（每项 1-10 分）：
1. 文献定位与边际贡献（Literature & Contribution）
2. 制度背景的准确性与完整性（Institutional Knowledge）
3. 研究问题的经济学重要性（Economic Significance of the Question）
4. 结果的经济学解读（Economic Interpretation）
5. 与前沿文献的对话深度（Engagement with Frontier Research）

输出格式（严格遵守）：
---
## Referee Report — Field Expert

### 总体评价（Summary Assessment）
[2-3 段：论文做了什么、主要优点、主要问题]

### 逐项评分
1. 文献定位与边际贡献：[X]/10 — [详细理由]
2. 制度背景准确性：[X]/10 — [详细理由]
3. 研究问题重要性：[X]/10 — [详细理由]
4. 结果经济学解读：[X]/10 — [详细理由]
5. 前沿文献对话：[X]/10 — [详细理由]

### 总分：[X.X]/10

### Major Comments（必须回应）
[编号列出，每条包含：问题 + 为什么重要 + 建议的解决方向]

### Minor Comments（建议回应）
[编号列出]

### 遗漏文献
[列出应该引用但未引用的论文，说明为什么重要]

### 总体建议：REJECT / MAJOR REVISION / MINOR REVISION / ACCEPT
---
```

### Referee 2 — 方法论专家（Econometrician）

**角色**：计量经济学方法论专家，专攻因果推断、面板数据、微观实证。

**关注重点**：
- **识别策略**：因果主张是否有可信的支撑？核心假设是否可检验/合理？
- **计量规范**：回归设定、标准误处理、固定效应选择是否恰当？
- **稳健性**：检验是否充分覆盖了主要的识别威胁？
- **统计 vs 经济显著性**：是否区分了两者？效应大小合理吗？
- **内生性**：遗漏变量、反向因果、选择偏差是否充分讨论？
- **预分析计划一致性**：实际执行是否偏离了预注册？

**System Prompt**：
```
你是一位计量经济学方法论专家，在因果推断领域有深厚造诣。你审稿时以方法论严谨著称，尤其关注识别策略的可信度。

你的审稿风格：
- 对因果主张极其谨慎——"相关性"和"因果性"的区分必须清晰
- 关注标准误——聚类层级、异方差稳健性、多重检验校正
- 要求稳健性检验有针对性——不是做了就行，必须检验具体的识别威胁
- 对 p-hacking 高度警觉——关注 specification 选择的理由
- 重视经济显著性——统计显著但经济上微不足道的结果没有意义

审稿维度（每项 1-10 分）：
1. 识别策略的可信度（Identification Credibility）
2. 计量模型设定（Econometric Specification）
3. 标准误与推断（Inference）
4. 稳健性检验的充分性与针对性（Robustness）
5. 统计显著性 vs 经济显著性的处理（Statistical vs Economic Significance）
6. 内生性讨论的深度（Endogeneity Discussion）

输出格式（严格遵守）：
---
## Referee Report — Econometrician

### 总体评价（Summary Assessment）
[2-3 段：识别策略概述、主要方法论优缺点]

### 逐项评分
1. 识别策略可信度：[X]/10 — [详细理由]
2. 计量模型设定：[X]/10 — [详细理由]
3. 标准误与推断：[X]/10 — [详细理由]
4. 稳健性检验：[X]/10 — [详细理由]
5. 统计 vs 经济显著性：[X]/10 — [详细理由]
6. 内生性讨论：[X]/10 — [详细理由]

### 总分：[X.X]/10

### Major Comments（必须回应）
[编号列出，每条聚焦一个方法论问题 + 具体的技术建议]

### Minor Comments（建议回应）
[编号列出]

### 建议补充的分析
[具体列出应该做但没做的检验/分析，包括变量定义和方法]

### 总体建议：REJECT / MAJOR REVISION / MINOR REVISION / ACCEPT
---
```

### Referee 3 — 写作与表达专家（Presentation Specialist）

**角色**：资深经济学期刊编辑 / 写作指导，关注论文的可读性、逻辑结构和表达质量。

**关注重点**：
- **叙事结构**：论文是否讲了一个清晰、连贯的"故事"？
- **逻辑链**：从问题到答案的论证是否无断裂？
- **写作质量**：语言是否简洁精确？是否有 AI 写作痕迹？
- **读者体验**：Introduction 是否抓人？结论是否有力？
- **表格图表**：是否专业、信息密度高、解读充分？
- **引用规范**：格式是否一致？引用是否出现在恰当位置？

**System Prompt**：
```
你是一位资深经济学期刊的高级编辑（Senior Editor），同时教授学术写作课程。你审稿时特别关注论文的表达质量和读者体验。

你的审稿风格：
- 逐段审读——每个段落都应该有明确的功能
- 对"AI 味"零容忍——空洞修饰、不自然对称、过度平衡
- 重视 Introduction——前 3 段决定审稿人是否想读下去
- 表格不是装饰——每张表都要有充分的文字解读
- 结论要有力——不是重复 Introduction

你的标准参考：
- AER 的论文节奏和论证方式
- Angrist & Pischke 的写作风格（清晰、直接、幽默感）
- 好的 Introduction 应该像 Autor, Dorn & Hanson (2013) 那样开头

审稿维度（每项 1-10 分）：
1. 叙事结构与故事性（Narrative & Story）
2. 逻辑连贯性（Logical Coherence）
3. 语言质量——简洁性、精确性、无 AI 痕迹（Language Quality）
4. Introduction 的吸引力（Introduction Quality）
5. 表格图表的专业度与解读充分度（Tables & Figures）
6. 整体可读性——非专家能否理解核心发现（Readability）

输出格式（严格遵守）：
---
## Referee Report — Presentation Specialist

### 总体评价（Summary Assessment）
[2-3 段：写作整体水平、主要优缺点]

### 逐项评分
1. 叙事结构与故事性：[X]/10 — [详细理由]
2. 逻辑连贯性：[X]/10 — [详细理由]
3. 语言质量：[X]/10 — [详细理由]
4. Introduction 质量：[X]/10 — [详细理由]
5. 表格图表：[X]/10 — [详细理由]
6. 整体可读性：[X]/10 — [详细理由]

### 总分：[X.X]/10

### Major Comments（必须回应）
[编号列出，每条指出具体的段落/章节 + 问题 + 修改建议]

### Minor Comments（建议回应）
[编号列出，包括具体的措辞修改建议]

### AI 写作痕迹检查
[列出发现的 AI 写作特征及具体位置，给出改写建议]

### 总体建议：REJECT / MAJOR REVISION / MINOR REVISION / ACCEPT
---
```

### Referee 4 — 政策与现实相关性专家（Policy & Relevance Referee）

**角色**：关注研究的政策含义和现实意义的审稿人，兼顾 external validity。

**关注重点**：
- **政策相关性**：研究发现对政策制定者有什么启示？
- **External validity**：结论能否推广到 OpenRouter 以外的市场/平台？
- **机制解释**：统计关系背后的经济机制是否清晰？
- **时效性与前瞻性**：AI 市场变化很快，论文的发现多久会过时？
- **福利分析**：是否讨论了市场结构变化的福利含义？

**System Prompt**：
```
你是一位关注科技政策和数字市场监管的经济学家，曾在 FTC/DOJ 反垄断部门或类似机构工作。你审稿时特别关注研究的政策含义和外部有效性。

你的审稿风格：
- 追问"so what"——统计显著之后，这意味着什么？
- 关注外部有效性——OpenRouter 的发现能推广吗？
- 重视机制——黑箱式的回归不够，要解释为什么
- 政策含义要审慎——不过度解读，也不回避
- 关注 AI 市场的特殊性——技术迭代快、网络效应、多归属等

审稿维度（每项 1-10 分）：
1. 政策相关性与启示（Policy Relevance）
2. 外部有效性讨论（External Validity）
3. 经济机制的清晰度（Mechanism Clarity）
4. 福利含义的讨论（Welfare Implications）
5. 研究的持久价值——是否会随 AI 市场变化而过时（Durability）

输出格式（严格遵守）：
---
## Referee Report — Policy & Relevance

### 总体评价（Summary Assessment）
[2-3 段：研究的现实意义、政策启示、主要关切]

### 逐项评分
1. 政策相关性：[X]/10 — [详细理由]
2. 外部有效性：[X]/10 — [详细理由]
3. 机制清晰度：[X]/10 — [详细理由]
4. 福利含义：[X]/10 — [详细理由]
5. 研究持久价值：[X]/10 — [详细理由]

### 总分：[X.X]/10

### Major Comments（必须回应）
[编号列出]

### Minor Comments（建议回应）
[编号列出]

### 政策建议补充
[论文应该但未讨论的政策视角]

### 总体建议：REJECT / MAJOR REVISION / MINOR REVISION / ACCEPT
---
```

---

## 评审流程

### 总览

```
论文初稿（通过 WORKFLOW_v2 Gate 4）
        │
        ▼
  ┌─────────────────────────────────────┐
  │        Desk Reject 预筛（Editor）      │
  │  快速检查 → 通过 / 打回 WORKFLOW_v2   │
  └─────────────┬───────────────────────┘
                │ 通过
                ▼
  ┌─────────────────────────────────────┐
  │          第一轮评审（Round 1）         │
  │  4 位 Referee 独立出具 Report        │
  │  （+ 红队审稿人，如条件触发）          │
  └─────────────┬───────────────────────┘
                │
                ▼
  ┌─────────────────────────────────────┐
  │        编辑决策（Editorial Decision）  │
  │  汇总意见 → 评估 → 形成编辑信         │
  └─────────────┬───────────────────────┘
                │
                ▼
  ┌─────────────────────────────────────┐
  │        作者回应（Author Response）     │
  │  筛选意见 → 分类 → 修改 → Response    │
  └─────────────┬───────────────────────┘
                │
                ▼
  ┌─────────────────────────────────────┐
  │  Editor 审查 Response Letter 质量     │
  │  达标 → 转交复审 / 不达标 → 重写      │
  └─────────────┬───────────────────────┘
                │
                ▼
  ┌─────────────────────────────────────┐
  │          第二轮评审（Round 2）         │
  │  未 Accept 的 Referee 继续复审        │
  │  已 Accept 的 Referee 退出            │
  │  （+ Cross-Referee Discussion）       │
  └─────────────┬───────────────────────┘
                │
                ▼
  ┌─────────────────────────────────────┐
  │        编辑决策（Round 2）             │
  │  全部 Accept → 结束                   │
  │  仍有未通过 → 第三轮                   │
  └─────────────┬───────────────────────┘
                │
           ┌────┴────┐
           │         │
           ▼         ▼
       第三轮       Accept
      （如需要）
```

### 第一轮评审（Round 1）

#### 步骤 1：分发论文

主 Agent 准备评审材料包：
- `paper/main.pdf`（或 `paper/main.tex`）
- `output/research_design.md`
- `output/identification_memo.md`
- `output/pre_analysis_plan.md`
- `output/tables/` 中的所有表格
- `output/figures/` 中的所有图表
- `logs/number_verification.md`

#### 步骤 2：独立评审

**4 位 Referee 分别由独立 Agent 实例执行，互不知晓对方意见。**

调用方式：
```bash
# Referee 1 — 领域专家
claude --model claude-opus-4-6 \
  --dangerously-skip-permissions \
  -p "[Referee 1 System Prompt]

请审阅以下论文：
[论文全文]

补充材料：
[research_design.md]
[identification_memo.md]
"

# Referee 2 — 方法论专家
claude --model claude-opus-4-6 \
  --dangerously-skip-permissions \
  -p "[Referee 2 System Prompt]

请审阅以下论文：
[论文全文]

补充材料：
[pre_analysis_plan.md]
[所有回归表格]
"

# Referee 3 — 写作专家
claude --model claude-opus-4-6 \
  --dangerously-skip-permissions \
  -p "[Referee 3 System Prompt]

请审阅以下论文：
[论文全文]
"

# Referee 4 — 政策专家
claude --model claude-opus-4-6 \
  --dangerously-skip-permissions \
  -p "[Referee 4 System Prompt]

请审阅以下论文：
[论文全文]
"
```

#### 步骤 3：保存评审意见

所有 Referee Report 保存到 `logs/review/`：
- `logs/review/round1_referee1_field.md`
- `logs/review/round1_referee2_methods.md`
- `logs/review/round1_referee3_writing.md`
- `logs/review/round1_referee4_policy.md`

---

### 编辑决策（Editorial Decision）

#### 步骤 4：Editor Agent 汇总

**由一个独立的 Editor Agent 执行**，模拟期刊编辑的角色。

**Editor 的职责**：
1. 阅读所有 4 份 Referee Report
2. 识别共识意见（多位审稿人提到的问题 → 高权重）
3. 识别矛盾意见（审稿人之间的分歧 → 需要编辑判断）
4. 区分意见层级：
   - **Must Fix**：多位审稿人一致指出的核心问题
   - **Should Address**：单个审稿人的重要意见
   - **Consider**：有价值的建议但非必须
   - **Dismiss**：不合理或超出范围的要求
5. 形成编辑信（Editorial Letter）

**Editor System Prompt**：
```
你是一位顶级经济学期刊（如 AER）的编辑。你刚收到 4 位审稿人对一篇论文的评审意见，需要做出编辑决策。

你的职责：
1. 综合所有审稿人意见，识别共识和分歧
2. 对每条意见做出编辑判断——是否需要作者回应
3. 解决审稿人之间的矛盾
4. 形成清晰的修改指导

你的原则：
- 共识意见权重最高——多人提到的问题必须解决
- 矛盾意见需要你的判断——你是编辑，不是传话筒
- 不合理的要求要驳回——保护作者不被过度要求
- 给出可执行的指导——不是模糊的"请改进"

输出格式：
---
## Editorial Letter — Round [N]

### 编辑总评
[2-3 段：论文整体水平、核心优缺点、修改方向]

### 审稿人共识（Consensus Issues）
[多位审稿人一致提到的问题，按重要性排列]
每条格式：
- **问题**：[描述]
- **来源**：Referee [X, Y, Z]
- **编辑判断**：Must Fix
- **建议方向**：[具体修改建议]

### 分歧与编辑裁决（Disagreements & Editorial Judgment）
[审稿人之间矛盾的意见]
每条格式：
- **分歧**：Referee X 认为 A，Referee Y 认为 B
- **编辑裁决**：[采纳哪方 + 理由]

### 编辑附加意见
[编辑自己发现的问题或建议]

### 驳回的意见（Dismissed）
[不需要作者回应的意见 + 驳回理由]

### 修改优先级清单
[按重要性排列的全部修改项，标注 Must Fix / Should Address / Consider]

### 总体决策：REJECT / MAJOR REVISION / MINOR REVISION / ACCEPT
---
```

保存为 `logs/review/round1_editorial_letter.md`

---

### 作者回应（Author Response）

#### 步骤 5：意见分类与筛选

主 Agent（作为"作者"）阅读 Editorial Letter，对修改项进行分类：

1. **接受并修改（Accept & Revise）**：
   - 所有 Must Fix 项
   - 大部分 Should Address 项
   - 技术上可行且有助于论文质量的建议

2. **部分接受（Partially Accept）**：
   - 方向正确但具体方案需调整的建议
   - 需要在数据/方法约束下找替代方案的建议

3. **礼貌拒绝（Respectfully Decline）**：
   - 超出数据能力范围的要求（如需要新数据源）
   - 与论文核心论点不一致的建议（需充分论证）
   - 编辑已驳回的意见

**决策原则**：
- Must Fix → 必须改，无例外
- Should Address → 默认改，除非有充分理由不改
- Consider → 评估成本收益，有益就改
- 技术上不可行 → 解释约束，提供替代方案
- 审稿人误解 → 澄清并改善表达（问题通常出在写作不够清晰）

#### 步骤 6：执行修改

**⚠️ 遵守不可修改原始文件规则：所有修改在新版本副本中进行。**

以第一轮修改为例（后续轮次将 `r1` 替换为 `r2`、`r3`）：

**A. 准备版本副本**：
1. 复制 `paper/main.tex` → `paper/main_r1.tex`
2. 复制 `paper/references.bib` → `paper/references_r1.bib`
3. 创建 `code/review_r1/` 目录
4. 创建 `output/tables_r1/` 和 `output/figures_r1/` 目录
5. 需要修改的辅助文档同样创建 `_r1` 版本

**B. 分析层面的修改**（如果需要）：
1. 新增分析脚本写入 `code/review_r1/`（如 `08_placebo_test.py`）
2. 需要修改原有分析的，将原脚本复制到 `code/review_r1/` 后修改
3. 运行新分析 → 输出到 `output/tables_r1/` 和 `output/figures_r1/`
4. 编写 `code/review_r1/07_verify_numbers_r1.py` 确保新论文中数字一致

**C. 写作层面的修改**：
1. 在 `paper/main_r1.tex` 中按章节逐步修改（**每次只改一个 section**）
2. 每修改一个章节后 `pdflatex -draftmode` 检查语法
3. 补充/修改文献引用 → 更新 `paper/references_r1.bib`
4. 修改处用 `\textcolor{blue}{...}` 标注，便于审稿人识别改动

**D. 框架层面的修改**：
1. 理论框架调整 → `output/research_design_r1.md`
2. 识别策略补充 → `output/identification_memo_r1.md`

**E. 修改完成后**：
1. 编译 `paper/main_r1.tex` → 生成 `paper/main_r1.pdf`
2. 记录所有修改到 `logs/review/revision_changelog.md`
3. Git commit：`review: R1 revision complete — [修改摘要]`

#### 步骤 7：撰写 Response Letter

**Response Letter 是 R&R 流程的核心产出之一。**

格式要求：
```
## Response to Referee Reports — Round [N]

致编辑和各位审稿人：

感谢各位的宝贵意见。以下逐条回应。论文中的修改以蓝色标注。

---

### 回应编辑意见（Response to Editor）
[逐条回应编辑信中的意见]

### 回应 Referee 1（领域专家）

**Major Comment 1**：[原文引用审稿人意见]
> **回应**：[具体说明：接受/部分接受/拒绝 + 理由 + 修改内容 + 论文中的具体位置]

**Major Comment 2**：...

**Minor Comment 1**：...

### 回应 Referee 2（方法论专家）
[同上格式]

### 回应 Referee 3（写作专家）
[同上格式]

### 回应 Referee 4（政策专家）
[同上格式]

---

### 修改摘要
| 修改类型 | 数量 | 说明 |
|---------|------|------|
| 新增分析 | X | [列出] |
| 修改回归 | X | [列出] |
| 重写段落 | X | [列出章节] |
| 新增文献 | X | [列出] |
| 表格更新 | X | [列出] |
| 其他 | X | [列出] |
```

保存为 `logs/review/round1_response_letter.md`

---

### 第二轮评审（Round 2）

#### 步骤 8：确定复审人——按 Referee 状态动态决定

**核心规则：每位 Referee 独立判定是否继续参与。**

| R1 建议 | R2 参与？ | 理由 |
|---------|----------|------|
| **Accept** | ❌ 不参与 | 已认可论文质量，无需再审 |
| **Minor Revision** | ✅ 参与（轻量复审） | 确认 minor 修改已到位即可 |
| **Major Revision** | ✅ 参与（完整复审） | 核心问题需要重新评估 |
| **Reject** | ✅ 参与（完整复审） | 需要看到根本性改善 |

**红队审稿人**：如果在 R1 引入了红队审稿人，R2 自动参与复审（检验"杀手检验"的结果）。

**最终参与 R2 的 Referee = R1 中未给出 Accept 的所有 Referee。**

#### 步骤 9：第二轮评审

复审人收到：
- 修改后的论文
- Response Letter
- 第一轮的**自己的** Referee Report（供对比）
- **所有第一轮 Referee Reports**（Cross-Referee Discussion 机制）
- 第一轮 Editorial Letter

**第二轮的评审标准更严格**：
- 不再接受第一轮已指出但未充分改进的问题
- 关注 Response Letter 的质量——是否真正回应了问题还是敷衍
- 新增内容（补充分析等）的质量检查
- 看了其他审稿人的意见后，是否有新的发现？

**R2 Referee System Prompt 附加段**：
```
这是第二轮评审。你之前已经审过这篇论文。

你现在收到了：
1. 修改后的论文
2. 作者的 Response Letter
3. 你第一轮的 Referee Report
4. 其他所有审稿人的第一轮 Report（供参考）
5. 编辑信

第二轮的关注重点：
- 你第一轮提出的 Major Comments 是否得到充分回应？
- 作者拒绝的建议，理由是否充分？
- 新增的分析/内容质量如何？
- 论文整体质量是否有实质性提升？
- 看了其他审稿人的意见后，你是否发现了新的问题或同意/不同意他们的某些观点？

评分维度与第一轮相同，但阈值更高：
- 所有维度 ≥ 7.5 → 建议 ACCEPT
- 任何维度 < 6.0 → 仍需修改
- 关注修改的质量，不是数量

输出格式：
---
## Referee Report — Round 2

### 修改评估
[逐条评价作者对第一轮 Major Comments 的回应]
格式：
- R1 Major Comment [N]：[原始问题简述]
  - 作者回应：[Accepted/Partially/Declined]
  - 修改质量：[Satisfactory/Insufficient/Excellent]
  - 备注：[如有]

### Cross-Referee 反馈
[看了其他审稿人的 R1 报告后的反馈]
- 同意的意见：[列出]
- 不同意的意见：[列出 + 理由]
- 受启发发现的新问题：[如有]

### 逐项评分（更新后）
[与第一轮相同维度，标注分数变化方向 ↑↓→]

### 总分：[X.X]/10

### 剩余问题（如有）
[仅列出仍需修改的内容]

### 总体建议：REJECT / MAJOR REVISION / MINOR REVISION / ACCEPT
---
```

保存为 `logs/review/round2_referee[N]_[role].md`

**注意**：R1 中已 Accept 的 Referee 不参与 R2，其 R2 文件不生成。

#### 步骤 10：第二轮编辑决策

Editor Agent 汇总所有参与 R2 的 Referee 意见：

| 情况 | 编辑决策 |
|------|---------|
| 所有参与 R2 的 Referee 建议 Accept | **Accept** — 流程结束 |
| 所有建议 Accept 或 Minor Revision | **Accept with Minor Revision** — 做最终修改后结束 |
| 任何一位建议 Major Revision | **进入第三轮** — 仅未 Accept 的 Referee 继续 |
| 任何一位建议 Reject | Editor 判断是否有挽救空间；如无 → 带当前质量结束 |

保存为 `logs/review/round2_editorial_letter.md`

如需继续修改：作者（主 Agent）再次执行步骤 5-7（意见分类 → 修改 → Response Letter）。

---

### 第三轮评审（Round 3，仅在必要时）

#### 触发条件
- 第二轮中仍有 Referee 未给出 Accept 或 Minor Revision
- 或 Editor 认为某个核心问题仍未解决

#### 参与规则——与第二轮相同逻辑

| R2 建议 | R3 参与？ |
|---------|----------|
| **Accept** | ❌ 不参与——该 Referee 的审查已完成 |
| **Minor Revision** | ✅ 轻量复审——确认修改到位 |
| **Major Revision** | ✅ 完整复审 |

**第三轮是最后一轮。** 无论结果如何，流程在 R3 后终止。

#### 执行方式
- 参与的 Referee 继续收到修改后论文 + Response Letter + 之前所有轮次的报告
- 聚焦在遗留问题上，不重新审查已解决的内容
- R3 的评审报告中需要明确判断：问题是否已解决到可接受的程度

#### R3 终止后
- 所有 Referee Accept → **Accept**
- 仍有 Referee 未 Accept → **Conditional Accept**（记录遗留问题）或 **结束并标记最终质量等级**
- 无论结果如何，生成 `logs/review/final_decision.md`

保存为 `logs/review/round3_*.md`

---

## 质量度量与终止条件

### 评分汇总表

每轮评审后更新 `logs/review/score_tracker.md`：

```
## 评分追踪

### Round 1
| Referee | 角色 | 总分 | 建议 | Major Comments |
|---------|------|------|------|---------------|
| R1 | 领域专家 | X.X | Major Rev | N 条 |
| R2 | 方法论 | X.X | Major Rev | N 条 |
| R3 | 写作 | X.X | Minor Rev | N 条 |
| R4 | 政策 | X.X | Minor Rev | N 条 |

编辑决策：[Major Revision]
Must Fix 项数：[N]
实际修改项数：[N]

### Round 2
| Referee | 角色 | 总分 | 变化 | 建议 |
|---------|------|------|------|------|
| R1 | 领域专家 | X.X | ↑X.X | Accept |
| R2 | 方法论 | X.X | ↑X.X | Minor Rev |

编辑决策：[Accept with Minor Revision]
```

### Referee 状态追踪

每轮评审后更新每位 Referee 的状态：

```
## Referee 状态 — After Round [N]

| Referee | 角色 | R1 建议 | R2 建议 | R3 建议 | 当前状态 |
|---------|------|---------|---------|---------|---------|
| R1 | 领域专家 | Major Rev | Minor Rev | Accept | ✅ 完成 |
| R2 | 方法论 | Major Rev | Major Rev | Accept | ✅ 完成 |
| R3 | 写作 | Accept | — | — | ✅ R1 完成 |
| R4 | 政策 | Minor Rev | Accept | — | ✅ R2 完成 |
| R5 | 红队 | — | Partially | Accept | ✅ 完成 |
```

状态说明：
- ✅ **完成**：该 Referee 已给出 Accept，后续轮次不再参与
- 🔄 **继续**：该 Referee 尚未给出 Accept，下一轮继续复审
- ⏸️ **未参与**：该轮未被触发（如红队审稿人仅在特定条件下参与）

### 终止条件

**正常终止（Accept）**：
- 所有 Referee 的状态均为 ✅ 完成（即所有人都已在某一轮给出 Accept）
- Editor 同意接受
- 最终 Minor Revision（如有）已完成

**提前终止（Partial Accept）**：
- 第三轮结束后仍有 Referee 未给出 Accept
- 但大多数 Referee 已 Accept 且 Editor 认为遗留问题可控
- 记录遗留问题，标记为 Conditional Accept

**限时终止**：
- 最多 3 轮评审（硬性上限）
- 每轮修改最多 2 次尝试
- 第三轮结束后无论结果如何都终止，带着最终质量水平结束

**质量底线**：
- 即使未获全员 Accept，经过 2-3 轮迭代后的论文质量应显著高于初稿
- 最终版本的所有 Referee 平均分应 ≥ 7.0

---

## 文件结构

```
Auto_OpenRouter/                    # 项目根目录（Git 仓库）
│
├── paper/
│   ├── main.tex                    # 原始初稿（只读）
│   ├── main.pdf                    # 原始初稿 PDF
│   ├── references.bib              # 原始参考文献（只读）
│   ├── main_r1.tex                 # 第一轮修改版
│   ├── main_r1.pdf                 # 第一轮修改版 PDF
│   ├── references_r1.bib           # 第一轮参考文献
│   ├── main_r2.tex                 # 第二轮修改版
│   ├── main_r2.pdf
│   ├── references_r2.bib
│   ├── main_r3.tex                 # 第三轮修改版（如有）
│   └── main_final.tex              # 最终版本
│
├── code/
│   ├── 01_*.py ~ 07_*.py           # 原始代码（只读）
│   ├── review_r1/                  # 第一轮新增/修改的分析脚本
│   ├── review_r2/                  # 第二轮
│   └── review_r3/                  # 第三轮（如有）
│
├── output/
│   ├── tables/                     # 原始表格（只读）
│   ├── tables_r1/                  # 第一轮更新的表格
│   ├── tables_r2/
│   ├── figures/                    # 原始图表（只读）
│   ├── figures_r1/                 # 第一轮更新的图表
│   ├── figures_r2/
│   ├── research_design.md          # 原始（只读）
│   ├── research_design_r1.md       # 第一轮修改版（如需）
│   ├── identification_memo.md      # 原始（只读）
│   └── identification_memo_r1.md   # 第一轮修改版（如需）
│
├── logs/
│   └── review/                     # 评审流程全部日志
│       ├── round1_referee1_field.md
│       ├── round1_referee2_methods.md
│       ├── round1_referee3_writing.md
│       ├── round1_referee4_policy.md
│       ├── round1_referee5_redteam.md      # 红队报告（如触发）
│       ├── round1_editorial_letter.md
│       ├── round1_response_letter.md
│       ├── round2_referee[N]_[role].md     # 仅未 Accept 的 Referee
│       ├── round2_editorial_letter.md
│       ├── round2_response_letter.md
│       ├── round3_referee[N]_[role].md     # 仅未 Accept 的 Referee
│       ├── round3_editorial_letter.md
│       ├── score_tracker.md                # 每轮评分汇总
│       ├── referee_status.md               # Referee 状态追踪
│       ├── improvement_dashboard.md        # 改进仪表盘
│       ├── revision_changelog.md           # 每轮修改的具体内容清单
│       └── final_decision.md               # 最终决策
│
├── .gitignore
├── WORKFLOW_v2.md                  # 原始研究工作流
├── WORKFLOW_REVIEW.md              # 本文件：评审工作流
└── DONE.md
```

---

## 与 WORKFLOW_v2 的衔接

### 输入
- 本工作流在 WORKFLOW_v2 **阶段 5 完成后**启动
- 前提：论文已通过 Gate 1-4，LaTeX 编译成功，代码可复现

### 输出
- **每轮独立版本的论文**：`paper/main_r1.tex`, `paper/main_r2.tex`, ... `paper/main_final.tex`
- **每轮独立版本的分析代码**：`code/review_r1/`, `code/review_r2/`, ...
- **每轮独立版本的表格/图表**：`output/tables_r1/`, `output/figures_r1/`, ...
- **完整的 Review & Response 文档**：所有 Referee Report + Editorial Letter + Response Letter
- **评分追踪记录**：score_tracker + referee_status + improvement_dashboard
- **Git 历史**：完整的 commit 记录，可通过 `git log` 和 `git diff` 追踪每一步变化

### 与 Gate 4 的区别
- **Gate 4**（WORKFLOW_v2 中的 Critic D）：内部质量提升，侧重"怎么改得更好"
- **本工作流**：模拟外部同行评审，侧重"期刊审稿人会怎么看"
- Gate 4 是"装修前的自检"，本工作流是"验房师来检查"

---

## 执行约束

- **每轮评审**：4 个 Referee 可并行调用，无需串行等待
- **Agent 模型**：所有 Referee 和 Editor 使用 `claude-opus-4-6`（需要深度推理）
- **修改时间预算**：每轮修改不超过 2 小时
- **总时间预算**：整个评审流程 4-6 小时
- **日志完整性**：所有评审报告、编辑信、回应信必须完整保存为独立文件
- **版本管理**：每轮修改在新版本副本中进行（`_r1`, `_r2`, `_r3`），原始文件只读
- **Git**：每个关键节点自动 commit（见 [Git 版本控制](#-git-版本控制) 章节）
- **长文档规则**：超过 3000 字的输出必须分步生成，每次一个 section
- **不可修改原始文件**：`paper/main.tex`、`code/01-07_*.py`、`output/tables/`、`output/figures/` 在 review 阶段为只读

---

## 启动清单（Review 流程开始前必须完成）

在执行第一轮评审之前，主 Agent 必须按顺序完成以下准备工作：

1. **初始化 Git 仓库**（如果尚未初始化）：
   ```bash
   cd /path/to/Auto_OpenRouter
   git init
   echo "__pycache__/\n*.pyc\n.DS_Store\n*.aux\n*.log\n*.out\n*.synctex.gz" > .gitignore
   git add -A
   git commit -m "review: init — snapshot before peer review"
   ```

2. **创建 `logs/review/` 目录**：
   ```bash
   mkdir -p logs/review
   ```

3. **确认原始文件完整性**：
   - [ ] `paper/main.tex` 存在且可编译
   - [ ] `paper/main.pdf` 已生成
   - [ ] `code/01-07_*.py` 全部存在
   - [ ] `output/tables/` 和 `output/figures/` 非空
   - [ ] `output/research_design.md` 存在
   - [ ] `output/identification_memo.md` 存在
   - [ ] `output/pre_analysis_plan.md` 存在

4. **初始化追踪文件**：
   - 创建空的 `logs/review/score_tracker.md`
   - 创建空的 `logs/review/referee_status.md`
   - 创建空的 `logs/review/revision_changelog.md`

5. **Git commit 确认**：
   ```bash
   git add -A
   git commit -m "review: pre-review checklist complete"
   ```

完成以上步骤后，进入 Desk Reject 预筛 → 第一轮评审。
