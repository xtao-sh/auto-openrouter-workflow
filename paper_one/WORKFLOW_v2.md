# WORKFLOW v2 — 多智能体自动经济学研究工作流

> **版本**：v2.2 (2026-03-25)
> **架构**：主研究 Agent + 3 个独立 Critic Agent + 自动化审计脚本
> **目标**：全自动产出一篇接近高质量经济学 Working Paper 标准的 LaTeX PDF 论文
>
> Agent 启动后按此流程自主推进，全程无需人类干预。
> 遇到任何不确定的背景知识、方法论问题或文献需求，**直接上网搜索查询**。

---

## 核心架构：五层质量保障

### 第一层：经济学规范锚定（Anchoring）

**问题**：AI 容易写出"看起来像论文但不像经济学论文"的东西。

**机制**：在关键节点要求 Agent 完成**结构化的经济学思考任务**：

1. **理论先行**：选题阶段必须写出简化理论框架：
   - 经济主体是谁？目标函数是什么？
   - 均衡预测是什么？什么条件下预测不同？
   - 实证检验的是哪个具体命题？
   - 至少 3 个可检验假说（hypotheses），每个有明确的经济学直觉

2. **识别策略审计**（Identification Memo）：基准回归之前完成 `output/identification_memo.md`：
   - 回归方程中的因果机制
   - 核心识别假设（如平行趋势、排他性约束）
   - 至少 3 个最大的识别威胁 + 每个的应对方案
   - 如果做不到可信的因果识别 → 论文必须定位为描述性/stylized facts

3. **文献深度锚定**：
   - 找到 **3 篇 closest papers**，逐篇说明本文的边际贡献
   - 找到**方法论经典参考**，说明为什么选这个方法
   - 上网搜索验证所有引用真实性

### 第二层：独立 Critic Agent（Gate Keeping）

**4 个 Gate，由独立 Claude Code 实例执行，不是主 Agent 自己审自己**。
- Gate 1-3：原有质量检查（选题、方法论、终审）
- Gate 4（新增）：论文修订审查 — 聚焦分析补充和写作质量提升
每个 Gate 最多 3 轮迭代；不通过则打回修改。
详见下方 [Critic Agent 执行规范](#critic-agent-执行规范)。

### 第三层：预注册式承诺（Pre-Registration Protocol）

**机制**：在阶段 2 通过 Gate 1 后、阶段 3 跑回归之前，Agent 写一份 `output/pre_analysis_plan.md`：
- 主回归方程（写出来，不是模糊描述）
- 因变量定义、核心自变量、控制变量、固定效应、聚类层级
- 预期系数方向 + 经济学理由
- 计划做的稳健性检验清单

Gate 2 审查时 Critic B 会对比：预分析计划 vs 实际执行。有偏离必须解释理由。

### 第四层：数字验真与复现（Anti-Hallucination + Reproducibility）

1. **数字验真脚本**：在论文写完后、Gate 3 之前运行 `code/07_verify_numbers.py`：
   - 遍历论文中所有数字（系数、SE、N、R²、描述性统计）
   - 与 `output/tables/` 中的 CSV 逐一比对
   - 输出 `logs/number_verification.md`：匹配 / 不匹配 / 无法验证
   - 任何不匹配必须修正

2. **代码复现检查**：最终打包前，从头重跑全部代码：
   ```bash
   cd code/
   for f in 0[1-6]_*.py; do python3 "$f"; done
   ```
   - 全部成功且输出与论文一致 → 通过
   - 任何脚本报错 → 修复后重跑

### 第五层：量化硬指标（Hard Metrics）

| 检查点 | 硬指标 | 不通过则 |
|--------|--------|---------|
| 数据探索 | ≥ 7 张图 + 1 个描述性统计表 | 补充 |
| 选题 | 3 个候选 + 理论框架 + identification memo | 补充 |
| 文献 | ≥ 20 篇引用，closest 3 篇有逐篇对比，全部上网验证 | 补搜 |
| 基准回归 | ≥ 3 个渐进式 specification | 补充 |
| 稳健性 | ≥ 5 种检验（含 event study / placebo） | 补充 |
| 异质性 | ≥ 3 个维度 | 补充 |
| 经济显著性 | 每个核心系数报告 1-SD 效应 + 对比文献 | 补充 |
| 论文长度 | ≥ 10,000 字（不含参考文献和附录） | 扩充 |
| LaTeX 编译 | 成功生成 PDF，无 undefined references | 修复 |
| 引用验证 | 0 个伪造引用 | 删除/替换 |
| 数字验真 | 论文中数字与表格 100% 一致 | 修正 |
| 代码复现 | 全部脚本从头跑通 | 修复 |
| 数据清洗文档 | 每步清洗有操作/影响/理由 | 补充 |
| 统计功效 | 核心效应的 power 讨论（至少 back-of-envelope） | 补充 |
| Sensitivity | 如果 ID 不完美，必须有 bounds/stability 分析 | 补充 |
| 图表格式 | 三线表 + 矢量图/300dpi + 专业配色 | 修改 |

---

## 执行流程

### 阶段 0：初始化

1. 读取本文件（WORKFLOW_v2.md）了解全流程
2. 读取 `config/research_rules.md` 了解研究纪律红线
3. 读取 `config/style_reference.md` 了解写作风格要求和参考论文
4. 读取 `data/README_data_pipeline.md` 和 `data/data_quality_report.md` 了解数据
5. 创建 `logs/research_log.md`，记录所有关键决策
6. 检查已有产出（`code/`, `output/`, `paper/`），评估是否可复用
7. 在日志中写入：启动时间、数据概况、工作流版本

---

### 阶段 1：数据探索（Data Exploration）

**任务**：
1. 编写 `code/01_data_exploration.py`
2. 加载两个数据源：
   - `data/master/usage_daily.csv` — 日频面板（模型×日期）
   - `data/rankings/` — 各期排行榜 JSON（5天间隔快照，11个维度）
3. 产出：
   - 描述性统计表（面板维度、变量分布、缺失值）
   - 至少 7 张探索性图表（总量趋势、市场份额变化、HHI、Top 10 分布、相关矩阵等）
   - `output/data_summary.md`

**硬指标门控**：≥ 7 张图 + 1 个完整描述性统计表 → 通过

---

### 阶段 2：选题与研究设计（Research Design）

**任务**：
1. 基于阶段 1 发现，提出 **3 个候选研究问题**
2. **每个候选必须包含**：
   - 简化理论框架（经济主体、目标函数、均衡预测、≥3 个可检验假说）
   - 因变量和自变量的具体定义
   - Identification strategy
   - Identification Memo（因果机制、核心假设、3 个最大威胁及应对）
   - 最接近的 3 篇已有论文 + 逐篇边际贡献说明
   - 数据可行性评估
3. **文献搜索（第一轮）**：
   - 搜索 NBER Working Papers（摘要公开，覆盖面广，质量有保障）
   - 搜索 Google Scholar / SSRN 补充
   - 重点搜索：AI/LLM 市场经济学、平台经济、网络效应、市场结构、创新竞争
   - **必读参考**：Demirer, Fradkin, Tadelis & Peng (NBER WP 34608, 2025) "The Emerging Market for Intelligence"；Fradkin (2025) "Demand for LLMs"
4. 选出最优方案，写入 `output/research_design.md`

**选题方向提示**（可参考但不限于）：
- 新模型进入对现有模型的替代/互补效应
- 开源 vs 闭源的市场份额竞争与定价策略
- 推理能力作为垂直差异化
- 工具调用/多模态能力与模型采用
- 市场集中度演变与竞争动态
- 定价策略与需求弹性

**⚠️ 选题要求**：必须有理论驱动。不接受纯描述性的"数据报告"。必须有因果性或至少结构化的研究问题。注意与 Fradkin (2025) 的差异化 — 他已经做了 OpenRouter 数据的描述性分析，本文必须在此基础上有增量贡献。

#### 🚧 GATE 1：Critic A 选题审查
- 独立 Agent 评分（5 项 × 1-10 分）
- **≥ 6.5 通过** → 进入阶段 3
- **< 6.5** → 返回修改 → 重新评审
- 最多 3 轮；3 轮不过 → 换候选方案

---

### 阶段 2.5：预分析计划（Pre-Analysis Plan）

在 Gate 1 通过后、阶段 3 之前，编写 `output/pre_analysis_plan.md`：

1. **主回归方程**（完整写出，包括下标）
2. **变量定义**：
   - 因变量：定义、构造方式、数据来源
   - 核心自变量：定义、变异来源
   - 控制变量：列表 + 每个的纳入理由
   - 固定效应：类型 + 理由
3. **聚类标准误**：聚类层级 + 理由
4. **预期结果**：
   - 核心系数的预期方向 + 经济学理由
   - 如果结果与预期不符，可能的解释
5. **稳健性检验计划**：至少 5 种，每种说明检验什么识别威胁
6. **异质性分析计划**：至少 3 个维度

---

### 阶段 3：实证分析（Empirical Analysis）

#### 3a. 数据构建
1. 编写 `code/03_data_construction.py`
2. 变量构造、样本筛选、面板结构处理
3. 输出 `output/analysis_panel.csv`

#### 3b. 基准回归
1. 编写 `code/04_baseline_regression.py`
2. 至少 3 个渐进式 specification（逐步加控制变量/固定效应）
3. 标准三线表保存到 `output/tables/`
4. 聚类标准误选择必须与预分析计划一致（偏离则解释）
5. **经济显著性强制报告**：
   - 每个核心系数：1-SD 变化 → Y 变化多少（绝对值 + 百分比）
   - 与已有文献中类似估计的效应大小对比
   - 明确判断 large / moderate / negligible

#### 3c. 稳健性检验
1. 编写 `code/05_robustness.py`
2. 按预分析计划执行至少 5 种检验：
   - 替换因变量定义
   - 改变样本范围
   - 替换控制变量/固定效应结构
   - 替换计量方法
   - Event study / Placebo test
3. 所有结果以标准格式保存

#### 3d. 异质性分析
1. 编写 `code/06_heterogeneity.py`
2. 至少 3 个维度的异质性
3. 交互项回归 + 分组回归

#### 3e. 文献搜索（第二轮）
- 回归结果出来后，搜索类似的实证发现
- 对比效应大小和方向：我们的结果与文献一致吗？不一致的话为什么？
- 补充到 `logs/literature_log.md`

**防线规则**：
- 每次 specification 变更记录在 `logs/research_log.md`
- 基准结果不显著 → 诚实报告，不 p-hack
- 与预分析计划的偏离必须解释理由
- 迭代 specification 最多 5 轮

#### 🚧 GATE 2：Critic B 方法论审查
- 独立 Agent 评分（5 项 × 1-10 分）
- **额外检查**：对比 pre_analysis_plan.md vs 实际执行
- **≥ 7.0 通过** → 进入阶段 4
- **< 7.0** → 返回修改 → 重新评审
- 最多 3 轮

---

### 阶段 4：论文写作（Paper Writing）

**输出格式**：LaTeX（可编译为 PDF）

#### ⚠️ 长文档分步生成规则（关键！）

**禁止一次性生成整篇论文**。LaTeX 论文必须**按章节分步写作**，每次只生成一个 section：

1. 先创建 `paper/main.tex` 框架（preamble + document structure + bibliography 设置）
2. 按顺序逐节填充内容：
   - Step 1: Abstract + Introduction → 写入 main.tex → 确认无误
   - Step 2: Background & Literature → 追加到 main.tex → 确认无误
   - Step 3: Theoretical Framework → 追加 → 确认
   - Step 4: Data section → 追加 → 确认
   - Step 5: Empirical Strategy → 追加 → 确认
   - Step 6: Results (baseline + robustness + heterogeneity) → 追加 → 确认
   - Step 7: Discussion + Conclusion → 追加 → 确认
   - Step 8: Appendix → 追加 → 确认
3. 每步完成后，检查 LaTeX 语法（`pdflatex -draftmode` 快速检查）
4. 全部写完后再做完整编译

**理由**：一次性生成 10,000+ 字的 LaTeX 会超出单次输出限制，导致截断和进程崩溃。分步生成既安全又便于质量控制。

同理，任何超过 3000 字的文档（代码、markdown、配置文件）都应分段写入。

#### 写作风格要求

**Style Reference**：Demirer, Fradkin, Tadelis & Peng (NBER WP 34608, 2025)。在写作前，Agent 必须搜索并阅读这篇论文的可用部分（至少摘要和目录结构），模仿其：
- 论证节奏
- 系数解读方式
- 制度背景的呈现方式

**写作纪律**：
- 语言：英文
- 风格：标准经济学期刊风格（简洁、精确、数据驱动）
- **禁止 AI 写作痕迹**：
  - ❌ "In recent years, AI has transformed..."（空洞开头）
  - ❌ "This paper makes several important contributions..."（自吹）
  - ❌ "The implications are profound..."（夸大）
  - ❌ "It is worth noting that..."（冗余）
  - ❌ "delve into", "landscape", "paradigm shift"（AI 标志词）
  - ✅ 直接切入数据和发现
  - ✅ 用具体数字说话
  - ✅ 对局限性直言不讳
- 每个表格/图表必须有具体的文字解读（不只是 "Table 2 shows the results"）
- 系数解读必须给出经济含义（"a one-standard-deviation increase in X is associated with a Y% change in Z"）
- 显著性讨论必须同时报告统计显著性和经济显著性

#### 论文结构（必须包含）

1. **Title**：简洁、信息量大
2. **Abstract**（250-300 字）：问题—数据—方法—发现—贡献
3. **1. Introduction**（1500-2000 字）：
   - 开头段：以具体的数据事实或经济现象引入
   - 研究问题的经济学重要性
   - 主要发现预览（1-2 句，清晰明确）
   - 边际贡献（与 closest 3 篇论文的明确对比，特别是 Fradkin 2025 和 Demirer et al. 2025）
   - 论文路线图
4. **2. Institutional Background**（500-800 字）：
   - LLM API 市场的运作方式
   - OpenRouter 作为聚合平台的角色和数据特点
   - 为什么这个市场适合研究所提出的问题
5. **3. Theoretical Framework**（800-1200 字）：
   - 简化模型（清晰的经济逻辑，不需要完整结构模型）
   - 可检验假说的推导
   - 与实证策略的联系
6. **4. Data**（800-1000 字）：
   - 数据来源和采集方式
   - 变量定义表（LaTeX tabular）
   - 描述性统计表
   - 样本选择、数据质量、时间覆盖讨论
7. **5. Empirical Strategy**（800-1200 字）：
   - 计量模型设定（完整回归方程，每个变量有解释）
   - 识别策略及其假设
   - 主要识别威胁的讨论和应对
8. **6. Results**（1500-2000 字）：
   - 基准结果（表格 + 经济学解读）
   - 经济显著性讨论
   - 稳健性检验（简洁汇报）
   - 异质性分析
9. **7. Discussion**（500-800 字）：
   - 经济学解释
   - 与已有文献的对话（特别是结果的一致性/差异性）
   - 政策含义（保持审慎）
10. **8. Conclusion**（300-500 字）：
    - 一句话总结
    - 具体的局限性（不是泛泛而谈）
    - 未来研究方向
11. **References**（BibTeX，全部上网验证真实性）
12. **Appendix**：附加稳健性表格、数据处理细节、变量构造详情

#### 文献搜索（第三轮）
- 写作过程中补充制度背景、市场数据、政策文献
- 搜索 NBER + 行业报告 + 新闻
- 记录在 `logs/literature_log.md`

#### 数字验真
- 编写并运行 `code/07_verify_numbers.py`
- 遍历论文中所有数字，与 output/tables/ 比对
- 输出 `logs/number_verification.md`
- 不一致的数字必须修正

#### 🚧 GATE 3：Critic C 终审
- 独立 Agent 评分（6 项 × 1-10 分）
- **≥ 7.0 通过** → 进入阶段 5
- **< 7.0** → 返回修改 → 重新评审
- 最多 3 轮

---

### 阶段 4.5：论文修订审查（Post-Writing Review）

**目标**：论文初稿完成后，进行深度审查，识别分析不足和写作缺陷，反复修订直至达标。

#### 🚧 GATE 4：Critic D 修订审查

**角色**：资深审稿人 + 写作编辑。不只看"能不能发"，而是看"哪里还能改得更好"。

**审查维度**（每项 1-10 分）：

1. **分析完整性**：是否有遗漏的分析角度？
   - 某个有趣的异质性维度没有探索？
   - 某个 robustness check 还缺？
   - 描述性统计是否充分支撑后续回归？
   - 是否需要补充子样本分析、时间趋势分解、或其他辅助分析？

2. **论证缺口**：论文的逻辑链是否有断裂？
   - Introduction 的 claim 是否在 Results 中都有支撑？
   - 理论预测与实证发现是否吻合？不吻合的地方有没有讨论？
   - 是否有"跳跃式推理"（从 A 直接到 C，缺少 B）？

3. **写作质量细节**：
   - 每个段落是否有明确的论点？
   - 过渡是否自然？
   - 是否有冗余段落或重复论述？
   - 引文是否在正确的位置（不是堆在 Literature Review 里不再出现）？
   - 表格/图表的文字解读是否充分（不只是"Table X shows..."）？

4. **读者体验**：
   - 非专家读者能否理解核心发现？
   - 专家读者是否会觉得无聊/肤浅？
   - 论文的"故事"是否清晰且引人入胜？

**输出格式**：
```
## 修订审查意见

### 逐项评分
1. 分析完整性：[X]/10 — [理由 + 具体补充建议]
2. 论证缺口：[X]/10 — [理由 + 具体修改建议]
3. 写作质量细节：[X]/10 — [理由 + 逐段修改建议]
4. 读者体验：[X]/10 — [理由]

### 总分：[X.X]/10
### 结果：PASS / FAIL（≥ 7.5 为 PASS）

### 必须修改的地方（Must Fix）
[按优先级排列，每条包含：问题描述 + 具体修改方案]

### 建议改进的地方（Nice to Have）
[按优先级排列]

### 可能需要补充的分析
[列出具体的分析建议，包括变量定义和预期结果]
```

**迭代流程**：
1. 主 Agent 完成论文初稿 → 调用 Critic D
2. Critic D 给出修订意见 → 主 Agent 逐条修改
3. 修改后重新提交 → Critic D 复审
4. **≥ 7.5 通过** → 进入阶段 5
5. 最多 3 轮；特别注意：如果 Critic D 建议补充分析，主 Agent 需要写代码跑分析、更新论文、更新表格

**与 Gate 3 的区别**：Gate 3 是"能不能发"的底线检查；Gate 4 是"怎么改得更好"的提升审查。Gate 3 确保无硬伤，Gate 4 提升论文质量。

---

### 阶段 5：LaTeX 编译与最终打包

#### 5a. LaTeX 编译
1. 论文使用标准经济学模板（类似 AER/NBER Working Paper 格式）
2. 所有表格用 LaTeX tabular（不是截图）
3. 所有图表嵌入
4. 引用使用 BibTeX（`paper/references.bib`）
5. 编译：`pdflatex` + `bibtex` → `paper/main.pdf`
6. 检查：无 undefined references，无溢出表格/图表

#### 5b. 代码复现检查
1. 从头重跑全部代码（01-06），确认输出一致
2. 记录在 `logs/reproducibility_check.md`

#### 5c. 最终自查清单

**文件完整性**：
- [ ] `paper/main.tex` — LaTeX 源文件
- [ ] `paper/main.pdf` — 编译后的 PDF
- [ ] `paper/references.bib` — 参考文献
- [ ] `code/01_*.py` 到 `code/07_*.py` — 全部代码
- [ ] `output/research_design.md` — 研究设计
- [ ] `output/identification_memo.md` — 识别策略备忘录
- [ ] `output/pre_analysis_plan.md` — 预分析计划
- [ ] `output/analysis_panel.csv` — 分析数据集
- [ ] `output/tables/` — 所有回归表
- [ ] `output/figures/` — 所有图表
- [ ] `logs/research_log.md` — 完整决策日志
- [ ] `logs/literature_log.md` — 文献搜索记录
- [ ] `logs/critic_scores.md` — 所有 Gate 评分记录
- [ ] `logs/number_verification.md` — 数字验真报告
- [ ] `logs/reproducibility_check.md` — 代码复现报告
- [ ] `output/data_cleaning_log.md` — 数据清洗文档
- [ ] `DONE.md` — 完成标志

**质量自查**：
- [ ] 所有引用均为真实论文（上网核查）
- [ ] 论文中的数字与表格 100% 一致
- [ ] 全部代码从头跑通
- [ ] 论文 ≥ 10,000 字
- [ ] 无 AI 写作痕迹
- [ ] 局限性讨论充分、具体
- [ ] 预分析计划 vs 实际执行的偏离已解释

---

## Critic Agent 执行规范

### 运行方式

Critic 是**独立的 Claude Code 实例**，不是主 Agent 自己扮演。
由主 Agent 在对应 Gate 处通过命令行调用。

```bash
claude --model claude-opus-4-6 \
  --dangerously-skip-permissions \
  -p "[Critic System Prompt + 待审查材料]"
```

### Critic A — 选题审稿人

**角色**：Top 5 经济学期刊 Associate Editor

**System Prompt**：
```
你是一位 Top 5 经济学期刊（如 AER、QJE、Econometrica）的 Associate Editor。
你正在评审一份关于 LLM API 市场的研究设计提案。

你的标准是严格的。一个好的选题必须：
1. 回应经济学理论中的某个争论或空白
2. 有可信的识别策略（或至少清晰地定位为描述性分析）
3. 相比已有文献有实质性贡献（不是增量改进）

评分维度（每项 1-10 分）：
1. 经济学意义：研究问题是否重要？是否回应了理论争论？
2. 数据匹配度：数据的结构和质量能否支撑这个问题？
3. 识别可行性：identification strategy 是否可信？最大威胁是什么？
4. 边际贡献：相比 Fradkin (2025) 和 Demirer et al. (2025) 等已有论文，新意何在？
5. 可行性：在现有数据和约束下能否完成？

输出格式（严格遵守）：
---
## 评审意见

### 逐项评分
1. 经济学意义：[X]/10 — [一句话理由]
2. 数据匹配度：[X]/10 — [一句话理由]
3. 识别可行性：[X]/10 — [一句话理由]
4. 边际贡献：[X]/10 — [一句话理由]
5. 可行性：[X]/10 — [一句话理由]

### 总分：[X.X]/10
### 结果：PASS / FAIL（≥ 6.5 为 PASS）

### 详细意见
[如果 FAIL：3 条具体修改建议]
[如果 PASS：1-2 个仍需注意的弱点]
---
```

### Critic B — 方法论审稿人

**角色**：计量经济学方法论专家

**System Prompt**：
```
你是一位计量经济学方法论专家，审查实证分析的技术质量。
你会同时收到预分析计划（pre-analysis plan）和实际执行的结果。

评分维度（每项 1-10 分）：
1. 模型设定：回归方程是否正确？变量选择有经济学理由吗？
2. 标准误处理：聚类层级合理吗？异方差、序列相关考虑了吗？
3. 识别策略执行：Identification Memo 的承诺是否兑现？
4. 稳健性充分度：检验是否涵盖主要识别威胁？有遗漏吗？
5. 结果解读：系数解读准确吗？统计显著性 vs 经济显著性区分了吗？

额外检查（重要）：
- 对比 pre_analysis_plan.md vs 实际执行：偏离了哪些？理由充分吗？
- 是否存在 p-hacking 迹象（如无理由地变换 specification 直到显著）？
- 经济显著性的计算和解读是否合理？

输出格式（严格遵守）：
---
## 方法论审查意见

### 预分析计划对比
- 一致项：[列出]
- 偏离项：[列出 + 评价理由是否充分]

### 逐项评分
1. 模型设定：[X]/10 — [详细理由]
2. 标准误处理：[X]/10 — [详细理由]
3. 识别策略执行：[X]/10 — [详细理由]
4. 稳健性充分度：[X]/10 — [详细理由]
5. 结果解读：[X]/10 — [详细理由]

### 总分：[X.X]/10
### 结果：PASS / FAIL（≥ 7.0 为 PASS）

### 修改建议
[按优先级排列，区分 Major / Minor]
---
```

### Critic C — 终审审稿人

**角色**：Reviewer 2（最挑剔的审稿人）

**System Prompt**：
```
你是一位资深经济学家，担任顶级期刊的 Reviewer 2。
你在审查一篇关于 LLM API 市场的实证论文。你以严格著称。

评分维度（每项 1-10 分）：
1. 论证逻辑：从引言到结论，逻辑链完整吗？有说服力吗？
2. 文献覆盖：遗漏重要文献了吗？与 closest papers 对比到位吗？
3. 写作质量：简洁精确吗？有 AI 写作痕迹吗？像经济学家写的吗？
4. 表格图表：专业、清晰、信息密度高吗？
5. 诚实度：局限性讨论充分吗？有过度解读吗？
6. 经济学洞察：论文推进了我们对这个市场的理解吗？

额外检查（必做）：
- 随机抽查 5 篇引用：上网搜索验证是否真实存在、作者和年份是否正确
- 论文中的关键数字是否与表格一致（抽查 10 个数字）
- 是否有内部矛盾（如引言说 X 但结论说 Y）
- 是否有 AI 写作的典型标志（空洞修饰语、过度平衡、不自然的对称结构）

输出格式（严格遵守）：
---
## 终审审查意见

### 逐项评分
1. 论证逻辑：[X]/10 — [详细理由]
2. 文献覆盖：[X]/10 — [详细理由]
3. 写作质量：[X]/10 — [详细理由]
4. 表格图表：[X]/10 — [详细理由]
5. 诚实度：[X]/10 — [详细理由]
6. 经济学洞察：[X]/10 — [详细理由]

### 引用抽查结果
[5 篇引用的验证结果]

### 数字抽查结果
[10 个数字的核对结果]

### 总分：[X.X]/10
### 结果：PASS / FAIL（≥ 7.0 为 PASS）

### Major Comments
[按重要性排列]

### Minor Comments
[按重要性排列]
---
```

### 评分记录

所有 Critic 评分记录在 `logs/critic_scores.md`：
```
## Gate [1/2/3] — Round [N]
- Date: [timestamp]
- Critic: [A/B/C]
- Scores: [逐项]
- Average: [X.X]
- Result: PASS / FAIL
- Key feedback: [摘要]
- Action taken: [主 Agent 的修改摘要]
```

---

## 文献搜索协议

### 搜索时机与任务

| 节点 | 搜索任务 | 搜索源 |
|------|---------|--------|
| 阶段 2（选题时） | closest papers + 方法论参考 | NBER WPs + Google Scholar + SSRN |
| 阶段 3（结果出来后） | 类似实证发现，对比效应大小和方向 | NBER + 领域期刊 |
| 阶段 4（写作时） | 制度背景、市场数据、政策文献 | 行业报告 + 新闻 + 监管文件 |
| Gate 3 前（引用验证） | 验证所有引用真实性 | 直接搜索论文标题 |

### 搜索策略
- **NBER 优先**：摘要公开、质量有保障、覆盖面广
- **关键词组合**：主题词 + "NBER working paper" / site:nber.org
- **必读论文**：
  - Demirer, Fradkin, Tadelis & Peng (2025) "The Emerging Market for Intelligence" (NBER WP 34608)
  - Fradkin (2025) "Demand for LLMs: Descriptive Evidence on Substitution, Market Expansion, and Multihoming"
  - 这两篇是最直接的对标，必须明确说明本文相对于它们的增量贡献

### 搜索记录
所有搜索记录在 `logs/literature_log.md`：
```
## 搜索 [N] — [日期时间]
- 搜索目的：[选题文献 / 效应对比 / 背景补充 / 引用验证]
- 关键词：[...]
- 找到的论文：
  1. [作者 (年份)] [标题] — [如何使用]
  2. ...
- 未找到 / 搜索失败：[记录]
```

---

## 补充机制

### A. 统计功效预检（Power Pre-Check）

在阶段 3 跑基准回归之前，先做一个 back-of-envelope 计算：
1. 数据中核心自变量的变异有多大？（within 方差 vs between 方差）
2. 以文献中类似研究的效应大小为参考，当前样本量和面板长度能检测到多大的效应？
3. 如果 power 明显不足 → 在论文中预先讨论，并在 identification memo 中标注

这能防止跑完回归才发现"样本太小检测不到效应"的尴尬。

### B. 失败模式处理

| 失败场景 | 处理方式 |
|---------|---------|
| Gate 1 三轮不过 | 放弃当前选题，换 3 个候选中的下一个。如果 3 个都不过 → 回到阶段 1 重新探索数据，提出新候选 |
| Gate 2 三轮不过 | 检查是否是选题本身的问题（识别策略不可行）。如果是 → 回到 Gate 1 重选。如果是技术问题 → 修复代码重跑 |
| Gate 3 三轮不过 | 区分问题类型：写作质量 → 重写；实证问题 → 回到阶段 3 补充分析；选题问题 → 回到阶段 2 |
| 代码复现失败 | 修复代码，重跑。如果结果变了 → 更新论文中的数字 → 重新过 Gate 3 |
| LaTeX 编译失败 | 修复语法错误，重新编译。最多尝试 5 次 |
| 某个 Python 包缺失 | 用 `pip install` 安装。如果安装失败 → 用替代方案 |

### C. 数据清洗文档

在 `output/data_cleaning_log.md` 中记录所有数据清洗决策：
```
## 清洗步骤 [N]
- 操作：[删除/修改/填补/转换]
- 影响：[多少观测受影响]
- 理由：[为什么这样做]
- 替代方案：[是否在稳健性检验中考虑]
```

### D. 表格和图表的学术标准

**表格**：
- 使用三线表（top rule、mid rule、bottom rule）
- 因变量在表头标注
- 每列是一个 specification，渐进式加控制变量
- 控制变量用 Yes/No 标注而非列出系数（除非控制变量本身有兴趣）
- 标准误在系数下方用括号
- 显著性星号：* p<0.10, ** p<0.05, *** p<0.01
- 表注说明：固定效应、聚类层级、观测值数、R²
- 参考格式：类似 `stargazer` 或 `estout` 的输出

**图表**：
- 清晰的标题（Figure X: [描述性标题]）
- 轴标签完整，字体大小可读
- 如果有置信区间，用阴影带而非误差线
- Event study 图：明确标注 t=0（处理时点）和参照期
- 保存为 PDF（矢量图，嵌入 LaTeX 更清晰）或 PNG 300dpi
- 配色专业（避免 matplotlib 默认彩色，用灰度+少量重点色）

### E. Sensitivity / Bounds Analysis

如果 identification strategy 依赖不可检验的假设（如 selection on observables），必须做一个 sensitivity analysis：
- Altonji, Elder & Taber (2005) 式的 selection on unobservables 检验
- 或 Oster (2019) δ-bounds
- 或简单的 coefficient stability test：加控制变量后系数变化多大？

这不是可选的"附加分析"，而是在识别不完美时的**必要**步骤。

---

## 执行约束

- **总时间预算**：4-8 小时（含所有 Gate 迭代）
- **迭代上限**：每个 Gate 最多 3 轮
- **网络查询**：随时可搜，不需要犹豫
- **日志**：所有重要决策记录在 `logs/research_log.md`
- **代码标准**：Python 3.13，pandas + statsmodels + scipy + matplotlib + seaborn + linearmodels
- **最终输出**：LaTeX PDF，标准经济学论文格式（NBER Working Paper 风格）
- **编排模式**：主 Agent 负责全流程执行；在每个 Gate 点调用独立 Critic 实例
- **LaTeX 模板**：使用以下 preamble（Palatino 字体、1.5 倍行距、A4）：

```latex
\documentclass[11pt, a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{mathpazo}
\usepackage{setspace}
\usepackage{hyperref}
\usepackage{natbib}
\usepackage{titlesec}
\usepackage{color}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage[dvipsnames]{xcolor}
\usepackage{enumitem}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, decorations.markings, patterns, calc, positioning}
\usepackage{multirow}
\onehalfspacing
```

根据需要可追加 `float`, `caption`, `subcaption`, `threeparttable`, `dcolumn`, `pdflscape`, `appendix` 等包。
