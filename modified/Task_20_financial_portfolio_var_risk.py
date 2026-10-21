"""
BIT 2118: Scientific Computing
Task 20 (Modified Real-World Case): Monte Carlo Portfolio Value-at-Risk (VaR & CVaR)
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Quantitative Risk Management - Portfolio Value at Risk
# Simulated N = 100,000 Daily Portfolio P&L Realizations
# ---------------------------------------------------------
# New Assumptions:
# 1. Total Portfolio Capital = $2,500,000.
# 2. Daily returns follow a slightly skewed distribution with mean mu = 0.04% and sigma = 1.25%.
# 3. Rare market stress events occur with probability 1.5% producing larger shocks.
# 4. Compute 1-day 95% and 99% Value at Risk (VaR) and Expected Shortfall (CVaR).

rng = np.random.default_rng(2026)
N = 100_000
portfolio_value = 2_500_000.0

# Base market volatility
base_returns = rng.normal(0.0004, 0.0125, N)
# Market crash / tail risk shocks
shock_mask = rng.uniform(0.0, 1.0, N) < 0.015
base_returns[shock_mask] -= rng.exponential(0.035, shock_mask.sum())

# Simulated dollar Profit and Loss (P&L)
pnl = portfolio_value * base_returns

# Value at Risk (VaR): Quantile of losses
var_95 = -np.percentile(pnl, 5.0)
var_99 = -np.percentile(pnl, 1.0)

# Conditional Value at Risk (CVaR / Expected Shortfall)
cvar_95 = -np.mean(pnl[pnl <= -var_95])
cvar_99 = -np.mean(pnl[pnl <= -var_99])

# Running 95% VaR convergence
running_var_95 = np.zeros(200)
sample_sizes = np.unique(np.logspace(2, np.log10(N), 200).astype(int))

for idx, size in enumerate(sample_sizes):
    sub_sample = pnl[:size]
    running_var_95[idx] = -np.percentile(sub_sample, 5.0)

print("==================================================")
print("TASK 20 MODIFIED: PORTFOLIO MONTE CARLO VaR")
print("==================================================")
print(f"Total Portfolio Value:      ${portfolio_value:,.2f}")
print(f"Total Monte Carlo Paths:    {N:,}")
print(f"1-Day 95% Value-at-Risk:    ${var_95:,.2f} ({var_95/portfolio_value*100:.2f}% of capital)")
print(f"1-Day 99% Value-at-Risk:    ${var_99:,.2f} ({var_99/portfolio_value*100:.2f}% of capital)")
print(f"1-Day 95% Expected Shortfall:${cvar_95:,.2f}")
print(f"1-Day 99% Expected Shortfall:${cvar_99:,.2f}")

os.makedirs("figures", exist_ok=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# Plot 1: P&L Distribution
ax1.hist(pnl / 1000.0, bins=100, color="#34495e", edgecolor="#2c3e50", alpha=0.75, density=True)
ax1.axvline(-var_95 / 1000.0, color="#f39c12", linestyle="--", linewidth=2, label=f"95% VaR: -${var_95/1000:.1f}k")
ax1.axvline(-var_99 / 1000.0, color="#e74c3c", linestyle="--", linewidth=2, label=f"99% VaR: -${var_99/1000:.1f}k")
ax1.set_xlabel("Daily Portfolio P&L ($ in Thousands)")
ax1.set_ylabel("Probability Density")
ax1.set_title("Simulated P&L Distribution with Tail Risk")
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)

# Plot 2: Convergence
ax2.semilogx(sample_sizes, running_var_95 / 1000.0, color="#2980b9", linewidth=2)
ax2.axhline(var_95 / 1000.0, color="red", linestyle=":", label=f"Asymptotic 95% VaR")
ax2.set_xlabel("Number of Monte Carlo Simulations (Log Scale)")
ax2.set_ylabel("Estimated 95% VaR ($ in Thousands)")
ax2.set_title("Monte Carlo Convergence of 95% VaR")
ax2.legend()
ax2.grid(True, linestyle="--", alpha=0.5)

fig.tight_layout()
plt.savefig("figures/task_20_portfolio_var.png", dpi=150)
plt.close()
print("Saved plot to figures/task_20_portfolio_var.png")
