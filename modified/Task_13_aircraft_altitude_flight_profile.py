"""
BIT 2118: Scientific Computing
Task 13 (Modified Real-World Case): Aircraft Climb & Descent Profile Interpolation
Part E Implementation
"""

import os
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Flight Telemetry Altitude Reconstruction
# Aircraft ADS-B radar transponder ping samples
# ---------------------------------------------------------
# New Assumptions:
# 1. Waypoint times in minutes: [0, 5, 12, 22, 35, 48, 60, 72].
# 2. Altitude in feet (FL0 to FL360 cruise down to approach).
# 3. Cubic splines capture continuous climb gradients without sharp corners.

minutes = np.array([0.0, 5.0, 12.0, 22.0, 35.0, 48.0, 60.0, 72.0])
altitude_ft = np.array([0.0, 4200.0, 14800.0, 26500.0, 36000.0, 36000.0, 18500.0, 2100.0])

linear_interp = interp1d(minutes, altitude_ft, kind="linear")
spline_interp = CubicSpline(minutes, altitude_ft)

dense_minutes = np.linspace(0.0, 72.0, 300)
alt_linear = linear_interp(dense_minutes)
alt_spline = spline_interp(dense_minutes)

# Target evaluation at t = 17.5 minutes (mid-climb)
eval_time = 17.5
lin_val = float(linear_interp(eval_time))
spline_val = float(spline_interp(eval_time))

# Instantaneous climb rate via derivative of cubic spline (feet per minute)
climb_rate_fpm = float(spline_interp.derivative()(eval_time))

print("==================================================")
print("TASK 13 MODIFIED: AIRCRAFT FLIGHT PROFILE")
print("==================================================")
print(f"Sample Radar Waypoints:       {len(minutes)} readings")
print(f"Evaluation at t = {eval_time} min:")
print(f"  Linear Altitude Estimate:   {lin_val:.1f} ft")
print(f"  Cubic Spline Estimate:      {spline_val:.1f} ft")
print(f"  Estimated Vertical Speed:   {climb_rate_fpm:.1f} ft/min")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(8, 4.5))
plt.scatter(minutes, altitude_ft, color="black", zorder=5, label="Radar Pings")
plt.plot(dense_minutes, alt_linear, "r--", label="Linear Piecewise", linewidth=1.5)
plt.plot(dense_minutes, alt_spline, "b-", label="Cubic Spline Trajectory", linewidth=2)
plt.scatter([eval_time], [spline_val], color="green", s=80, zorder=6, label=f"t=17.5m ({spline_val:.0f}ft)")
plt.xlabel("Flight Elapsed Time (minutes)")
plt.ylabel("Pressure Altitude (feet)")
plt.title("Task 13 Modified: Flight Trajectory Interpolation")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_13_flight_interpolation.png", dpi=150)
plt.close()
print("Saved plot to figures/task_13_flight_interpolation.png")
