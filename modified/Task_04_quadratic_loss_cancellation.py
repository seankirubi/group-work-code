"""
BIT 2118: Scientific Computing
Task 04 (Modified Real-World Case): Quadratic Roots & Loss of Significance in Orbital Mechanics
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Orbital Trajectory Flight-Path Angle Calculation
# Solving ax^2 + bx + c = 0 when b^2 >> 4ac
# ---------------------------------------------------------
# New Assumptions:
# 1. In near-parabolic orbital rendezvous, curvature parameter 'a' is tiny (a = 1e-8),
#    velocity term 'b' is large (b = 10^4), and offset 'c' is small (c = 1.0).
# 2. In floating-point arithmetic, computing sqrt(b^2 - 4ac) yields a value extremely
#    close to b. Subtracting it from b causes severe catastrophic cancellation.

a = 1e-8
c = 1.0
b_values = np.logspace(2, 8, 7) # b from 10^2 to 10^8

direct_roots = []
stable_roots = []
relative_discrepancies = []

print("==================================================")
print("TASK 04 MODIFIED: CATASTROPHIC CANCELLATION IN ORBITS")
print("==================================================")
for b in b_values:
    # Standard formula (subtractive cancellation when b > 0)
    disc = b**2 - 4*a*c
    x_direct = (-b + np.sqrt(disc)) / (2*a)
    
    # Algebraically equivalent rationalized / stable formula
    x_stable = (-2*c) / (b + np.sqrt(disc))
    
    direct_roots.append(x_direct)
    stable_roots.append(x_stable)
    rel_err = abs(x_direct - x_stable) / abs(x_stable)
    relative_discrepancies.append(rel_err)
    
    print(f"b = {b:1.0e} | Direct: {x_direct:20.15e} | Stable: {x_stable:20.15e} | Rel Diff: {rel_err:.2%}")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(8, 4.5))
plt.loglog(b_values, [max(e, 1e-16) for e in relative_discrepancies], marker="s", color="#c0392b", linewidth=2)
plt.title("Task 04 Modified: Catastrophic Loss of Precision as b Grows")
plt.xlabel("Magnitude of Linear Coefficient b (Log Scale)")
plt.ylabel("Relative Error of Standard Quadratic Formula")
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_04_cancellation.png", dpi=150)
plt.close()
print("Saved plot to figures/task_04_cancellation.png")
