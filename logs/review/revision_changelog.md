## Round 1 修改日志

### 写作层修改

- [x] **Abstract**: 拆分为 3 段，移除 SE/Oster/替代嵌套精度，加入 35% 经济显著性 — `paper/main_r1.tex`
- [x] **Introduction**: 从 8 段精简到 6 段；移除开发者风险段落(移至 Discussion)；合并实证预览段落，不报告系数/SE/Oster — `paper/main_r1.tex`
- [x] **Related Literature**: 新增 product line management 段落(Desai 2001, Draganska & Jain 2005)；加入 Aghion & Howitt 1992, Gentzkow 2007, Hagiu & Wright 2015, Santos Silva & Tenreyro 2006, Zheng et al. 2024 — `paper/main_r1.tex`
- [x] **Theoretical Framework**: 精简 H1-H3 各为一句话+论证；新增 Schumpeter Mark I vs Mark II 段落 — `paper/main_r1.tex`
- [x] **Results — Nested Logit**: 新增 Oster bound 不处理同时性偏误的显式说明；新增 OLS 偏误方向/幅度校准段落(sigma 诚实区间 [0.25, 0.50])；扩展 Table 2 非 sigma 系数讨论；重写替代嵌套结构(标记为机械伪影) — `paper/main_r1.tex`
- [x] **Results — Panel**: 显著报告前趋势 t 统计量(t=-2.46, -2.05, -2.75)；新增反向因果讨论；新增 Roth 2022 HonestDiD 段落；新增 Sun & Abraham 2021 段落；新增置换推断段落；新增 leave-one-event-out 段落；"mutual validation"改为"qualitative consistency" — `paper/main_r1.tex`
- [x] **Discussion**: 重新框架为"质量阶梯 cannibalization"和 Mark II；新增 cross-firm null 三种解释(水平差异化/增长掩盖/信息摩擦)；新增开发者风险段落(从 Intro 移入)；新增多归属讨论+Gentzkow 引用；新增外部有效性段落(API/企业/消费者)；新增 family-upgrade 分类内生性讨论 — `paper/main_r1.tex`
- [x] **Limitations**: 重写，按重要性加权(无因果识别获最多篇幅)；段落长度不再均匀 — `paper/main_r1.tex`
- [x] **Conclusion**: 从 5 段精简到 3 段；以大胆推测结尾；引用具体方法论优先事项 — `paper/main_r1.tex`
- [x] **Writing quality**: 减少三元列举、过度对冲、元评论、模板连接词 — `paper/main_r1.tex`

### 文献更新

- [x] 新增 10 篇引用 — `paper/references_r1.bib`:
  - Desai (2001), Draganska & Jain (2005), Aghion & Howitt (1992), Gentzkow (2007)
  - Hagiu & Wright (2015), Santos Silva & Tenreyro (2006), Zheng et al. (2024)
  - Roth (2022), Callaway & Sant'Anna (2021), Sun & Abraham (2021)

### 分析层修改（标记为需实施但尚未运行代码）

- [ ] Roth (2022) HonestDiD 前趋势偏误校正 — 需新代码 `code/review_r1/`
- [ ] Sun & Abraham (2021) 交互加权估计器 — 需新代码 `code/review_r1/`
- [ ] 置换推断(1000+ 日期随机化) — 需新代码 `code/review_r1/`
- [ ] Leave-one-event-out 分析 — 需新代码 `code/review_r1/`
- [ ] Hausman-type IV 替代估计 — 需新代码 `code/review_r1/`
- [ ] Wild cluster bootstrap — 需新代码 `code/review_r1/`

### 所有修改以 `\textcolor{blue}{...}` 标注

### Git Commit
- 待提交: "review: R1 revision complete"
