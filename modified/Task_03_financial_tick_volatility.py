"""
BIT 2118: Scientific Computing
Task 03 (Modified Real-World Case): High-Frequency Financial Tick Volatility
Part E Implementation
"""

import os
import numpy as np
import timeit
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: 1,000,000 High-Frequency Stock Trade Ticks
# Continuous Log-Returns: r_t = ln(P_t / P_{t-1})
# Realized Variance Proxy: r_t^2
# ---------------------------------------------------------
# New Assumptions:
# 1. Stock price follows a geometric Brownian motion discretized across 1M ticks.
# 2. Starting price is $150.00 with annualized volatility ~ 25%.
# 3. Fast quantitative trading algorithms require near-instantaneous volatility updates.

rng = np.random.default_rng(101)
N = 1_000_000
log_innovations = rng.normal(0, 0.0002, N)
prices = 150.0 * np.exp(np.cumsum(log_innovations))

def loop_version():
    log_returns = []
    squared_returns = []
    for i in range(1, len(prices)):
        ret = np.log(prices[i] / prices[i - 1])
        log_returns.append(ret)
        squared_returns.append(ret ** 2)
    return log_returns, squared_returns

def vectorized_version():
    log_returns = np.diff(np.log(prices))
    squared_returns = log_returns ** 2
    return log_returns, squared_returns

loop_time = timeit.timeit(loop_version, number=1)
vector_time = timeit.timeit(vectorized_version, number=3) / 3

log_returns, squared_returns = vectorized_version()

print("==================================================")
print("TASK 03 MODIFIED: FINANCIAL TICK VOLATILITY")
print("==================================================")
print(f"Number of Ticks Analyzed: {N:,}")
print("First five log-returns:", log_returns[:5])
print("First five squared returns (variance proxy):", squared_returns[:5])
print(f"Python Loop Time:     {loop_time:.4f} s")
print(f"NumPy Vectorized Time:{vector_time:.4f} s")
print(f"Vectorized Speedup:   {loop_time / vector_time:.1f}x")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(8, 4))
plt.hist(log_returns, bins=100, color="#2980b9", edgecolor="#1b4f72", alpha=0.75, density=True)
plt.title("Task 03 Modified: Empirical Distribution of High-Frequency Log-Returns")
plt.xlabel("Log-Return per Tick")
plt.ylabel("Probability Density")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("figures/task_03_financial_ticks.png", dpi=150)
plt.close()
print("Saved plot to figures/task_03_financial_ticks.png")
