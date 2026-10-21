"""
BIT 2118: Scientific Computing
Task 17 (Modified Real-World Case): Bioreactor Microbial Logistic Growth (Euler's Method)
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Microbial Biomass Growth in a Batch Bioreactor
# ODE: dN/dt = r * N * (1 - N / K)
# Exact: N(t) = (K * N0 * exp(r*t)) / (K + N0 * (exp(r*t) - 1))
# ---------------------------------------------------------
# New Assumptions:
# 1. Specific growth rate r = 0.35 h^-1.
# 2. Maximum bioreactor carrying capacity K = 45.0 g/L.
# 3. Initial inoculated biomass N0 = 1.5 g/L.
# 4. Total batch fermentation duration T_end = 24.0 hours.
# 5. Comparing coarse step (h = 1.0 h) vs fine step (h = 0.2 h).

r = 0.35
K = 45.0
N0 = 1.5
end_time = 24.0

def logistic_growth_rate(N):
    return r * N * (1.0 - N / K)

def solve_euler(h):
    t_arr = np.arange(0.0, end_time + h, h)
    N_arr = np.zeros_like(t_arr)
    N_arr[0] = N0
    for i in range(len(t_arr) - 1):
        N_arr[i + 1] = N_arr[i] + h * logistic_growth_rate(N_arr[i])
    return t_arr, N_arr

# Coarse and fine Euler simulations
t_coarse, N_coarse = solve_euler(1.0)
t_fine, N_fine = solve_euler(0.2)

# Exact analytical benchmark
t_dense = np.linspace(0.0, end_time, 250)
exact_dense = (K * N0 * np.exp(r * t_dense)) / (K + N0 * (np.exp(r * t_dense) - 1.0))
exact_end = (K * N0 * np.exp(r * end_time)) / (K + N0 * (np.exp(r * end_time) - 1.0))

err_coarse = abs(N_coarse[-1] - exact_end)
err_fine = abs(N_fine[-1] - exact_end)

print("==================================================")
print("TASK 17 MODIFIED: BIOREACTOR EULER ODE")
print("==================================================")
print(f"Exact Final Biomass (t=24h):  {exact_end:.4f} g/L")
print(f"Euler (h=1.0h) Final Biomass: {N_coarse[-1]:.4f} g/L | Error: {err_coarse:.4f} g/L")
print(f"Euler (h=0.2h) Final Biomass: {N_fine[-1]:.4f} g/L | Error: {err_fine:.4f} g/L")
print(f"Error Reduction Ratio:        {err_coarse / err_fine:.1f}x (Consistent with O(h) first-order method)")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(8, 4.5))
plt.plot(t_dense, exact_dense, "k-", linewidth=2, label="Analytical Exact")
plt.plot(t_coarse, N_coarse, "r--o", linewidth=1.5, label="Euler (h = 1.0 h)")
plt.plot(t_fine, N_fine, "b:^", linewidth=1.5, markevery=5, label="Euler (h = 0.2 h)")
plt.xlabel("Fermentation Time (hours)")
plt.ylabel("Biomass Concentration N(t) (g/L)")
plt.title("Task 17 Modified: Microbial Logistic Growth Simulation")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_17_bioreactor_euler.png", dpi=150)
plt.close()
print("Saved plot to figures/task_17_bioreactor_euler.png")
