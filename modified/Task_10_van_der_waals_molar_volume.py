"""
BIT 2118: Scientific Computing
Task 10 (Modified Real-World Case): Real Gas Molar Volume via Van der Waals Equation
Part E Implementation
"""

import os
import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Thermodynamics of High-Pressure Carbon Dioxide (CO2)
# Van der Waals: (P + a/V^2)(V - b) = R*T
# f(V) = P*V^3 - (P*b + R*T)*V^2 + a*V - a*b = 0
# ---------------------------------------------------------
# New Assumptions:
# Operating conditions: T = 325 K, P = 6.0e6 Pa (60 bar).
# Gas constants for CO2:
# a = 0.3640 Pa * m^6 / mol^2 (intermolecular attraction)
# b = 4.267e-5 m^3 / mol (molecular co-volume)
# R = 8.314 J / (mol * K)

P = 6.0e6
T = 325.0
a = 0.3640
b = 4.267e-5
R = 8.314

def f_vdw(V):
    return (P + a / (V**2)) * (V - b) - R * T

# Bisection search between physical lower bound (>b) and ideal gas volume V_ideal
V_ideal = (R * T) / P
bracket = [b * 1.05, V_ideal * 1.5]

sol_bisect = root_scalar(f_vdw, bracket=bracket, method="bisect", xtol=1e-12)

# Fixed-point iteration: V = b + R*T / (P + a/V^2)
def g_vdw(V):
    return b + (R * T) / (P + a / (V**2))

V_fp = V_ideal
history = [V_fp]
for _ in range(100):
    V_next = g_vdw(V_fp)
    history.append(V_next)
    if abs(V_next - V_fp) < 1e-12:
        break
    V_fp = V_next

# Compressibility factor Z = P*V / (R*T)
Z = (P * sol_bisect.root) / (R * T)

print("==================================================")
print("TASK 10 MODIFIED: VAN DER WAALS MOLAR VOLUME")
print("==================================================")
print(f"Ideal Gas Volume:             {V_ideal:12.6e} m^3/mol")
print(f"Bisection Molar Volume:       {sol_bisect.root:12.6e} m^3/mol")
print(f"Fixed-Point Molar Volume:     {history[-1]:12.6e} m^3/mol")
print(f"Fixed-Point Iteration Count:  {len(history) - 1}")
print(f"Compressibility Factor Z:     {Z:.4f} (real gas non-ideality)")

os.makedirs("figures", exist_ok=True)
v_vals = np.linspace(b * 1.2, V_ideal * 1.2, 300)
plt.figure(figsize=(8, 4.5))
plt.plot(v_vals * 1e3, [f_vdw(v) for v in v_vals], color="#2c3e50", linewidth=2, label="f(V) Van der Waals")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(sol_bisect.root * 1e3, color="#e74c3c", linestyle=":", linewidth=2, label=f"Root = {sol_bisect.root*1e3:.3f} L/mol")
plt.xlabel("Molar Volume (L/mol)")
plt.ylabel("Residual f(V) (J/mol)")
plt.title("Task 10 Modified: Van der Waals Equilibrium Molar Volume")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_10_vdw_molar_volume.png", dpi=150)
plt.close()
print("Saved plot to figures/task_10_vdw_molar_volume.png")
