"""
BIT 2118: Scientific Computing
Task 19 (Modified Real-World Case): Multi-Modal Freight Logistics Optimization with Carbon Caps
Part E Implementation
"""

import os
import numpy as np
from scipy.optimize import minimize

# ---------------------------------------------------------
# Scenario: Supply Chain Transport Cost Minimization
# x1: Metric tons shipped via Electric Rail
# x2: Metric tons shipped via Clean Diesel Fleet
# ---------------------------------------------------------
# New Assumptions:
# 1. Shipping Cost per ton: Rail = $18/ton, Road = $32/ton.
# 2. Minimum cargo shipping demand: at least 650 tons.
# 3. Maximum corporate carbon emissions cap: <= 35.0 kg CO2 equivalent.
#    Emission factors: Rail = 0.025 kg CO2/ton, Road = 0.090 kg CO2/ton.
# 4. Rail capacity ceiling: max 500 tons due to track slot availability.

def freight_cost(x):
    x1, x2 = x
    return 18.0 * x1 + 32.0 * x2

def demand_constraint(x):
    # x1 + x2 >= 650  -->  x1 + x2 - 650 >= 0
    return (x[0] + x[1]) - 650.0

def carbon_cap_constraint(x):
    # 0.025*x1 + 0.090*x2 <= 35.0  -->  35.0 - (0.025*x1 + 0.090*x2) >= 0
    return 35.0 - (0.025 * x[0] + 0.090 * x[1])

constraints = [
    {"type": "ineq", "fun": demand_constraint},
    {"type": "ineq", "fun": carbon_cap_constraint}
]

# Bounds: Rail in [0, 500], Road in [0, None]
bounds = [(0.0, 500.0), (0.0, None)]

init_guess = [300.0, 350.0]

solution = minimize(
    freight_cost,
    init_guess,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

x1_opt, x2_opt = solution.x
min_cost = solution.fun
total_emissions = 0.025 * x1_opt + 0.090 * x2_opt

print("==================================================")
print("TASK 19 MODIFIED: FREIGHT LOGISTICS OPTIMIZATION")
print("==================================================")
print(f"Solver Success:           {solution.success}")
print(f"Optimal Rail Allocation:  {x1_opt:.2f} tons")
print(f"Optimal Road Allocation:  {x2_opt:.2f} tons")
print(f"Total Tonnage Delivered:  {x1_opt + x2_opt:.2f} tons (Target: >= 650)")
print(f"Total Carbon Emissions:   {total_emissions:.2f} kg CO2 (Cap: <= 35.0 kg)")
print(f"Minimized Total Logistics Cost: ${min_cost:,.2f}")

# Discrete Integer Search near optimum
best_int = None
for r in range(int(x1_opt) - 5, min(501, int(x1_opt) + 6)):
    for t in range(int(x2_opt) - 5, int(x2_opt) + 6):
        if (r + t >= 650) and (0.025 * r + 0.090 * t <= 35.0) and (r >= 0) and (t >= 0):
            c = 18.0 * r + 32.0 * t
            if best_int is None or c < best_int[0]:
                best_int = (c, r, t)

if best_int:
    print(f"Nearest Discrete Integer Solution: ${best_int[0]:,.2f} (Rail: {best_int[1]}t, Road: {best_int[2]}t)")
