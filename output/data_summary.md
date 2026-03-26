# Data Exploration Summary

## Panel Dimensions
- **Observations**: 29,084 model×day observations
- **Unique models**: 389
- **Unique firms**: 66
- **Date range**: 2025-12-20 to 2026-03-23 (93 days)
- **Average days per model**: 74.8

## Market Structure
- **Mean model-level HHI**: 741 (×10,000 scale)
- **Mean firm-level HHI**: 1524 (×10,000 scale)
- **Mean CR10**: 55.2%
- **Median # models with >1K daily requests**: 194
- **Top model daily share (mean)**: 15.3%

## Key Distributional Facts
- Usage is extremely skewed: median model gets 323,913 total requests vs mean of 6,151,822
- Power law fit (top 200 models): α = 1.57
- 260/389 models (67%) have >1K daily average requests

## Technology Adoption Trends
- **Reasoning tokens**: 0.5% of total tokens (latest week)
- **Tool call rate**: 0.305 calls per request (latest week)
- **Cache share**: 76.7% of prompt tokens (latest week)

## Weekday Effects
- Weekdays show 103% of average usage
- Weekends show 92% of average usage
- Strongest day: Wed (1.06×)
- Weakest day: Sat (0.92×)

## New Model Entry
- 389 unique models observed
- First model entry date in panel: 2025-12-20
- Median weekly entry rate: 6 new models/week

## Data Quality Considerations
- OpenRouter retroactively updates historical data; high-volume models (>10K req/day) are stable (±4%), low-volume models are volatile
- Same-day data excluded (potentially incomplete)
- Recommended: use 7-day rolling averages, filter to >1K req/day for quantitative analysis

## Figures Produced
1. fig01_aggregate_trends.png — Daily requests and tokens over time
2. fig02_hhi_over_time.png — Model-level and firm-level HHI
3. fig03_top10_market_share.png — Top 10 models weekly market share
4. fig04_firm_market_share.png — Firm-level weekly market share
5. fig05_usage_distribution.png — Rank-size and histogram of usage
6. fig06_feature_adoption.png — Reasoning, tool calls, cache adoption
7. fig07_tokens_per_request.png — Token intensity by model
8. fig08_correlation_matrix.png — Correlation of model characteristics
9. fig09_model_entry.png — New model entry dynamics
10. fig10_weekday_effects.png — Day-of-week patterns

## Tables Produced
1. table01_descriptive_stats.csv — Full descriptive statistics
