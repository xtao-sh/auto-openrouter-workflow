# Style Reference — 写作风格与质量锚定

## Primary Style Reference

**Demirer, Fradkin, Tadelis & Peng (2025)**
"The Emerging Market for Intelligence: Pricing, Supply, and Demand for LLMs"
NBER Working Paper 34608

这是与本研究**最直接相关**的高质量论文 — 同样研究 LLM API 市场的经济学。
Agent 在写作前必须搜索并阅读此论文的可用部分（至少摘要），模仿其：
- 论证节奏和结构
- 系数解读方式
- 制度背景的呈现方式

**Secondary Reference**：
- Fradkin (2025) "Demand for LLMs: Descriptive Evidence on Substitution, Market Expansion, and Multihoming" — 使用 OpenRouter 数据，是最直接的数据对标

## 写作原则

### 1. 开头 — 以事实引入，不以宏大叙事引入
❌ "The rise of artificial intelligence has fundamentally transformed the technology landscape..."
✅ "Between January and March 2026, over 2,000 large language models were available through API marketplaces, processing millions of requests daily. Yet the top 10 models captured over 60% of total usage."

### 2. 贡献陈述 — 具体、谦逊、对比
❌ "This paper makes three important contributions to the literature."
✅ "Relative to Fradkin (2025), who documents aggregate substitution patterns, we exploit within-author model releases to identify displacement effects at the model level."

### 3. 系数解读 — 经济含义优先
❌ "The coefficient on X is 0.15 and statistically significant at the 1% level."
✅ "A one-standard-deviation increase in new model capability (0.3 points on the benchmark score) is associated with a 15% decline in incumbent model usage (Table 3, Column 2), an effect roughly comparable to the impact of a 20% price reduction."

### 4. 显著性 — 坦诚且有层次
❌ "Unfortunately, this result is not statistically significant."
✅ "The point estimate is positive but imprecise (β = 0.12, SE = 0.12), and we cannot reject zero at conventional levels. The 95% confidence interval [-0.12, 0.36] includes economically meaningful effects in both directions, suggesting our sample may lack power to detect displacement over this time horizon."

### 5. 局限性 — 具体、不泛泛
❌ "This study has several limitations. Future research could address these."
✅ "Our panel spans 94 days. If displacement unfolds over quarters rather than weeks—as in traditional technology markets (Bresnahan and Greenstein, 1999)—our event window may be too short to capture it. We partially address this by examining cumulative effects in Figure 5, which shows no trend break through day 30."

### 6. 禁止的 AI 标志词汇和句式
- "delve into", "landscape", "paradigm shift", "game-changer"
- "It is worth noting that..." → 直接说
- "In conclusion, ..." → 直接总结
- "This paper aims to fill this gap" → 说具体填什么 gap
- 对称的三点结构（"First... Second... Third..."过度使用）
- 每段结尾都是总结句（over-signposting）

### 7. 数学符号
- 回归方程用 LaTeX 数学环境
- 变量名在公式中统一：用小写字母+下标
- 估计值用 hat：$\hat{\beta}$

## 经济学论文的"味道"（What Makes It Feel Like Economics）

好的经济学论文的特征不在于技术复杂度，而在于：

1. **始终在回答"so what"**：每个结果都连接回一个经济学问题
2. **对 identification 的执着**：不仅报告相关性，而是不断追问"这能说明因果吗？如果不能，我们知道什么？"
3. **与文献的持续对话**：不是在 lit review 里集中引用完就结束，而是在 Results 和 Discussion 中不断与已有发现对比
4. **对数据局限的坦诚**：好的论文让读者信任，是因为它明确告诉你自己做不到什么
5. **政策相关性但不急于给政策建议**：描述市场结构，但不急于说"therefore the government should..."
