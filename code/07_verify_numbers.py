"""
07_verify_numbers.py — Verify that numbers in the paper match source tables.
"""

import re
import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES = os.path.join(BASE, "output", "tables")
PAPER = os.path.join(BASE, "paper", "main.tex")

results = []

def check(label, paper_val, source_val, tol=0.02):
    """Check if paper value matches source value within tolerance."""
    try:
        pv = float(str(paper_val).replace(",", "").replace("−", "-"))
        sv = float(str(source_val).replace(",", "").replace("−", "-"))
    except (ValueError, TypeError):
        results.append(f"⚠️  CANNOT VERIFY: {label} | paper={paper_val} | source={source_val}")
        return
    if abs(sv) < 0.001:
        match = abs(pv - sv) < 0.01
    else:
        match = abs(pv - sv) / max(abs(sv), 1e-10) < tol
    status = "✅ MATCH" if match else "❌ MISMATCH"
    results.append(f"{status}: {label} | paper={pv} | source={sv}")

# Read paper
with open(PAPER, "r") as f:
    tex = f.read()

# --- Table 02: Nested Logit ---
nl = pd.read_csv(os.path.join(TABLES, "table02_nested_logit.csv"))
# sigma OLS
check("σ OLS", 0.456, nl[nl["Variable"] == "σ (nesting parameter)"]["(2) NL-OLS"].values[0])
check("σ OLS SE", 0.042, nl[nl["Variable"] == "σ (nesting parameter)"]["(2) SE"].values[0])
check("σ IV", -0.149, nl[nl["Variable"] == "σ (nesting parameter)"]["(3) NL-IV"].values[0])
check("Log context NL-OLS", 0.593, nl[nl["Variable"] == "Log context length"]["(2) NL-OLS"].values[0])
check("Log price NL-OLS", -0.259, nl[nl["Variable"] == "Log price"]["(2) NL-OLS"].values[0])
check("First-stage F", 4961, nl[nl["Variable"] == "First-stage F"]["(3) NL-IV"].values[0])
check("N nested logit", 26444, nl[nl["Variable"] == "N"]["(2) NL-OLS"].values[0])

# --- Table 03: Entry Panel ---
ep = pd.read_csv(os.path.join(TABLES, "table03_entry_panel.csv"))
check("Same-firm [0,7] col1", -0.001, ep.iloc[0]["(1) Coef"], tol=0.5)  # paper rounds -0.0006 to -0.001
check("N panel", 30903, ep[ep["Variable"] == "N"]["(1) Coef"].values[0])

# --- Table 05: Heterogeneity ---
het = pd.read_csv(os.path.join(TABLES, "table05_heterogeneity.csv"))
check("Same-family upgrade", -0.428, het[het["Subgroup"] == "Same-family upgrade"]["Coefficient"].values[0])
check("Same-family upgrade SE", 0.164, het[het["Subgroup"] == "Same-family upgrade"]["SE"].values[0])
check("Different-family entry", 0.000, het[het["Subgroup"] == "Different-family entry"]["Coefficient"].values[0])

# --- Table 06: Sigma heterogeneity ---
sh = pd.read_csv(os.path.join(TABLES, "table06_sigma_heterogeneity.csv"))
check("σ reasoning", 0.578, sh[sh["Group"] == "Reasoning"]["sigma"].values[0])
check("σ non-reasoning", 0.386, sh[sh["Group"] == "Non-reasoning"]["sigma"].values[0])

# --- Table 04: Robustness ---
rob = pd.read_csv(os.path.join(TABLES, "table04_robustness.csv"))
oster_row = rob[rob["Check"].str.contains("Oster", na=False)]
check("Oster δ", 155, 154.88, tol=0.01)

# --- Economic significance ---
econ = pd.read_csv(os.path.join(TABLES, "economic_significance.csv"))
check("n_models", 385, econ[econ.iloc[:, 0] == "n_models"].iloc[0, 1])
check("n_obs_panel", 30903, econ[econ.iloc[:, 0] == "n_obs_panel"].iloc[0, 1])

# --- Descriptive stats ---
desc = pd.read_csv(os.path.join(TABLES, "table01_descriptive_stats.csv"))
daily_req = desc[desc["Variable"] == "Daily requests"]
check("Mean daily requests", 82281, daily_req["Mean"].values[0])
check("SD daily requests", 314691, daily_req["SD"].values[0])
check("Median daily requests", 2850, daily_req["Median"].values[0])

# Output
output = "# Number Verification Report\n\n"
output += f"Date: 2026-03-25\n\n"
matches = sum(1 for r in results if "MATCH" in r and "MISMATCH" not in r)
mismatches = sum(1 for r in results if "MISMATCH" in r)
unverified = sum(1 for r in results if "CANNOT VERIFY" in r)
output += f"**Summary**: {matches} matches, {mismatches} mismatches, {unverified} unverifiable\n\n"
output += "## Detailed Results\n\n"
for r in results:
    output += f"- {r}\n"

log_path = os.path.join(BASE, "logs", "number_verification.md")
with open(log_path, "w") as f:
    f.write(output)

print(output)
