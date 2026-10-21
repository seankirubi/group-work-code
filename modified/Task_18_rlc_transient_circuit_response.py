"""
BIT 2118: Scientific Computing
Task 18 (Modified Real-World Case): Series RLC Circuit Transient Response via SciPy solve_ivp
Part E Implementation
"""

import os
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Underdamped Second-Order RLC Transient Response
# L * d^2q/dt^2 + R * dq/dt + (1/C)*q = Vs
# State Variables: y[0] = q (Charge, Coulombs), y[1] = i = dq/dt (Current, Amperes)
# ---------------------------------------------------------
# New Assumptions:
# R = 30.0 Ohms (damping resistance)
# L = 0.25 Henry (inductance)
# C = 150.0e-6 Farad (150 uF capacitance)
# Step Input: Vs = 12.0 Volts applied at t = 0
# Initial state: Uncharged capacitor q(0) = 0, zero initial current i(0) = 0

R = 30.0
L = 0.25
C = 150.0e-6
Vs = 12.0

def rlc_dynamics(t, y):
    q, i = y
    dq_dt = i
    di_dt = (Vs - R * i - q / C) / L
    return [dq_dt, di_dt]

t_span = (0.0, 0.12)
t_eval = np.linspace(0.0, 0.12, 500)

solution = solve_ivp(
    rlc_dynamics,
    t_span,
    [0.0, 0.0],
    t_eval=t_eval,
    method="RK45",
    rtol=1e-8,
    atol=1e-10
)

# Derived physical quantities
charge = solution.y[0]
current = solution.y[1]
vc = charge / C # Capacitor voltage in Volts

v_peak = np.max(vc)
overshoot_pct = ((v_peak - Vs) / Vs) * 100.0

print("==================================================")
print("TASK 18 MODIFIED: RLC TRANSIENT DYNAMICS")
print("==================================================")
print(f"Solver Success:             {solution.success}")
print(f"Supply Step Voltage:        {Vs:.1f} V")
print(f"Steady-State Final Voltage: {vc[-1]:.4f} V")
print(f"Peak Transient Voltage:     {v_peak:.4f} V")
print(f"Percentage Overshoot:       {overshoot_pct:.2f}%")
print(f"Max Peak Current:           {np.max(current):.4f} A")

os.makedirs("figures", exist_ok=True)
fig, ax1 = plt.subplots(figsize=(8, 4.5))

color = '#2980b9'
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Capacitor Voltage Vc (V)', color=color)
ax1.plot(solution.t, vc, color=color, linewidth=2, label="Capacitor Voltage (Vc)")
ax1.axhline(Vs, color="gray", linestyle="--", alpha=0.7, label="Steady-State (12V)")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#e74c3c'
ax2.set_ylabel('Circuit Current (A)', color=color)
ax2.plot(solution.t, current, color=color, linestyle=":", linewidth=1.8, label="Inductor Current (i)")
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Task 18 Modified: Underdamped RLC Second-Order Transient Dynamics')
fig.tight_layout()
plt.savefig("figures/task_18_rlc_circuit.png", dpi=150)
plt.close()
print("Saved plot to figures/task_18_rlc_circuit.png")
