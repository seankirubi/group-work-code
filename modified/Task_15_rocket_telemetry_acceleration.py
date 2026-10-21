"""
BIT 2118: Scientific Computing
Task 15 (Modified Real-World Case): Rocket Telemetry Velocity & Acceleration
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Sounding Rocket Launch Telemetry Differentiation
# Altitude y(t) -> First Derivative v(t) -> Second Derivative a(t)
# ---------------------------------------------------------
# New Assumptions:
# 1. Uniform telemetry sampling interval h = 2.0 seconds.
# 2. Stage-1 powered burn occurs between t = 0s and t = 12s.
# 3. Standard gravity g0 = 9.81 m/s^2 to calculate payload g-force.

time = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
altitude = np.array([0.0, 44.0, 185.0, 428.0, 775.0, 1230.0, 1795.0])
h = time[1] - time[0]
n = len(time)

# 1. First Derivative: Velocity v(t) = dy/dt
velocity = np.zeros(n)
# Forward difference at start (O(h))
velocity[0] = (altitude[1] - altitude[0]) / h
# Central differences for interior (O(h^2))
for i in range(1, n - 1):
    velocity[i] = (altitude[i + 1] - altitude[i - 1]) / (2.0 * h)
# Backward difference at end (O(h))
velocity[-1] = (altitude[-1] - altitude[-2]) / h

# 2. Second Derivative: Acceleration a(t) = d^2y/dt^2 (Central differences O(h^2))
acceleration = np.zeros(n)
acceleration[0] = (altitude[2] - 2*altitude[1] + altitude[0]) / (h**2)
for i in range(1, n - 1):
    acceleration[i] = (altitude[i + 1] - 2.0*altitude[i] + altitude[i - 1]) / (h**2)
acceleration[-1] = (altitude[-1] - 2*altitude[-2] + altitude[-3]) / (h**2)

g_force = acceleration / 9.81

print("==================================================")
print("TASK 15 MODIFIED: ROCKET TELEMETRY DERIVATIVES")
print("==================================================")
for t, y, v, a, g in zip(time, altitude, velocity, acceleration, g_force):
    print(f"t={t:4.1f}s | Alt={y:6.1f}m | Vel={v:6.2f}m/s | Accel={a:5.2f}m/s^2 | Load={g:4.2f} g")

os.makedirs("figures", exist_ok=True)
fig, ax1 = plt.subplots(figsize=(8, 4.5))

color = '#1f77b4'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Velocity (m/s)', color=color)
ax1.plot(time, velocity, color=color, marker='o', linewidth=2, label='Velocity')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#d62728'
ax2.set_ylabel('Acceleration (m/s²)', color=color)
ax2.plot(time, acceleration, color=color, marker='s', linestyle='--', linewidth=2, label='Acceleration')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Task 15 Modified: Rocket Velocity & Acceleration Profiles')
fig.tight_layout()
plt.savefig("figures/task_15_rocket_derivatives.png", dpi=150)
plt.close()
print("Saved plot to figures/task_15_rocket_derivatives.png")
