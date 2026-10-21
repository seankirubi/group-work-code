"""
BIT 2118: Scientific Computing
Task 14 (Modified Real-World Case): Enzyme Reaction Kinetics (Michaelis-Menten Fitting)
Part E Implementation
"""

import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Biochemical Reaction Velocity vs Substrate Concentration
# Michaelis-Menten Model: V = (Vmax * S) / (Km + S)
# ---------------------------------------------------------
# New Assumptions:
# 1. Substrate concentration [S] in millimoles per liter (mM).
# 2. Reaction velocity V in micromoles per minute (umol/min).
# 3. Parameters to estimate: Vmax (maximum rate) and Km (Michaelis affinity constant).

substrate_mM = np.array([0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0], dtype=float)
velocity = np.array([18.2, 31.5, 52.0, 81.3, 103.4, 119.5, 131.0], dtype=float)

def michaelis_menten(s, vmax, km):
    return (vmax * s) / (km + s)

# Initial parameter guesses: Vmax ~ max(velocity), Km ~ median(substrate)
p0 = [140.0, 3.0]
params, cov = curve_fit(michaelis_menten, substrate_mM, velocity, p0=p0)
vmax_fit, km_fit = params
errors = np.sqrt(np.diag(cov))

predicted_v = michaelis_menten(substrate_mM, vmax_fit, km_fit)
rmse = np.sqrt(np.mean((velocity - predicted_v)**2))
# R-squared calculation
ss_tot = np.sum((velocity - np.mean(velocity))**2)
ss_res = np.sum((velocity - predicted_v)**2)
r_squared = 1.0 - (ss_res / ss_tot)

print("==================================================")
print("TASK 14 MODIFIED: MICHAELIS-MENTEN CURVE FITTING")
print("==================================================")
print(f"Fitted Vmax: {vmax_fit:.3f} +/- {errors[0]:.3f} umol/min")
print(f"Fitted Km:   {km_fit:.3f} +/- {errors[1]:.3f} mM")
print(f"Model RMSE:  {rmse:.3f} umol/min")
print(f"R-squared:   {r_squared:.4f}")
print(f"Predicted Velocity at [S] = 100 mM: {michaelis_menten(100.0, vmax_fit, km_fit):.2f} umol/min")

os.makedirs("figures", exist_ok=True)
s_smooth = np.linspace(0.1, 60.0, 200)
plt.figure(figsize=(8, 4.5))
plt.scatter(substrate_mM, velocity, color="#d35400", s=60, zorder=5, label="Bioassay Data")
plt.plot(s_smooth, michaelis_menten(s_smooth, vmax_fit, km_fit), color="#2980b9", linewidth=2, label="Fitted Michaelis-Menten")
plt.axhline(vmax_fit, color="gray", linestyle="--", label=f"Asymptotic Vmax ({vmax_fit:.1f})")
plt.xlabel("Substrate Concentration [S] (mM)")
plt.ylabel("Reaction Velocity V (umol/min)")
plt.title("Task 14 Modified: Enzyme Kinetics Hyperbolic Fit")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_14_enzyme_kinetics.png", dpi=150)
plt.close()
print("Saved plot to figures/task_14_enzyme_kinetics.png")
