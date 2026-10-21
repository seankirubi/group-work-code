"""
BIT 2118: Scientific Computing
Task 12 (Modified Real-World Case): 2D Acoustic / Radio Beacon Trilateration
Part E Implementation
"""

import os
import numpy as np
from scipy.optimize import root
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: 2D Target Positioning from Two Ranging Beacons
# Beacon 1: (x1, y1) = (0, 0), Range r1 = 8.5 km
# Beacon 2: (x2, y2) = (10, 0), Range r2 = 6.5 km
# Circular Range Equations:
# Eq 1: (x - 0)^2 + (y - 0)^2 - 8.5^2 = 0
# Eq 2: (x - 10)^2 + (y - 0)^2 - 6.5^2 = 0
# ---------------------------------------------------------
# New Assumptions:
# 1. Beacons transmit synchronized radio chirps.
# 2. Circles intersect at two mirror points (above and below the baseline).
# 3. Solver is tested from positive-y and negative-y initial guesses.

r1 = 8.5
r2 = 6.5
b1 = np.array([0.0, 0.0])
b2 = np.array([10.0, 0.0])

def range_equations(coords):
    x, y = coords
    eq1 = (x - b1[0])**2 + (y - b1[1])**2 - r1**2
    eq2 = (x - b2[0])**2 + (y - b2[1])**2 - r2**2
    return [eq1, eq2]

guesses = [[5.0, 5.0], [5.0, -5.0]]
solutions = []

print("==================================================")
print("TASK 12 MODIFIED: 2D BEACON TRILATERATION")
print("==================================================")
for g in guesses:
    res = root(range_equations, g, method="hybr")
    solutions.append(res.x)
    print(f"Initial Guess: {g}")
    print(f"Located Target Coordinates: (x={res.x[0]:.4f}, y={res.x[1]:.4f}) km")
    print(f"Residual Vector: {range_equations(res.x)}")
    print(f"Convergence Success: {res.success}\n")

# Plotting the geometric intersection
os.makedirs("figures", exist_ok=True)
theta_grid = np.linspace(0, 2*np.pi, 200)
c1_x = b1[0] + r1 * np.cos(theta_grid)
c1_y = b1[1] + r1 * np.sin(theta_grid)
c2_x = b2[0] + r2 * np.cos(theta_grid)
c2_y = b2[1] + r2 * np.sin(theta_grid)

plt.figure(figsize=(7, 6))
plt.plot(c1_x, c1_y, "b--", label="Beacon 1 Range Circle (r=8.5km)")
plt.plot(c2_x, c2_y, "g--", label="Beacon 2 Range Circle (r=6.5km)")
plt.plot(b1[0], b1[1], "bs", markersize=8, label="Beacon 1 (0,0)")
plt.plot(b2[0], b2[1], "g^", markersize=8, label="Beacon 2 (10,0)")

for idx, sol in enumerate(solutions, 1):
    plt.plot(sol[0], sol[1], "ro", markersize=10, label=f"Target Fix {idx} ({sol[0]:.2f}, {sol[1]:.2f})")

plt.title("Task 12 Modified: Geometric Trilateration Intersection")
plt.xlabel("East Distance (km)")
plt.ylabel("North Distance (km)")
plt.legend(loc="upper right", fontsize=8)
plt.grid(True, linestyle="--", alpha=0.6)
plt.axis("equal")
plt.tight_layout()
plt.savefig("figures/task_12_trilateration.png", dpi=150)
plt.close()
print("Saved plot to figures/task_12_trilateration.png")
