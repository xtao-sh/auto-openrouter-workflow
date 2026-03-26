# Data Cleaning Log

## Raw Data
- Source: data/master/usage_daily.csv
- Initial observations: 29084
- Initial models: 389

## Cleaning Steps
- Step 1: Remove models with <1000 total requests: 30978 → 30907 obs (71 removed, 4 models dropped)
- Step 2: Remove first 3 days of panel: 30907 → 30903 obs
- Step 3: Remove zero-count observations: 30903 → 30903 obs

## Final Sample
- Observations: 30903
- Unique models: 385
- Unique firms: 64
- Date range: 2025-12-23 to 2026-03-23
- Models with pricing: 28815 obs (339 models)
- Free models: 32
- Reasoning models: 166

## Entry Events
- Total entry events in sample: 385
- Entry events after sample start: 78

## Outside Option
- Assumed inside share: 80% (outside option = 20% of market)
- Rationale: OpenRouter captures a substantial share of multi-model API traffic,
  but enterprise direct-contract usage is not observed. 20% outside option is conservative.
  Robustness: will vary between 10% and 40%.
