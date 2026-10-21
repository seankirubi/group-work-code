"""
BIT 2118: Scientific Computing
Task 16 (Modified Real-World Case): Hydroelectric Dam Floodgate Water Discharge Volume
Part E Implementation
"""

import os
import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Hydroelectric Dam Spillway Total Water Discharge
# Cumulative Volume V = \int_{0}^{T} Q(t) dt
# ---------------------------------------------------------
# New Assumptions:
# 1. Flow rate Q(t) is logged every 3 hours over a 24-hour floodgate release operation.
# 2. Time in hours: t = [0, 3, 6, 9, 12, 15, 18, 21, 24].
# 3. Discharge rate in m^3/s. Conversion: 1 hour = 3600 seconds.
# 4. Total volume converted to Mega-liters (1 ML = 1000 m^3).

time_hours = np.array([0.0, 3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0])
flow_m3_s = np.array([120.0, 180.0, 340.0, 560.0, 620.0, 510.0, 380.0, 230.0, 140.0])

# Time in seconds for integration
time_seconds = time_hours * 3600.0

# Integration: Trapezoidal Rule vs Simpson's 1/3 Rule
vol_trapezoid_m3 = np.trapezoid(flow_m3_s, time_seconds)
vol_simpson_m3 = simpson(flow_m3_s, x=time_seconds)

vol_trapezoid_ML = vol_trapezoid_m3 / 1000.0
vol_simpson_ML = vol_simpson_m3 / 1000.0
discrepancy_ML = abs(vol_simpson_ML - vol_trapezoid_ML)
rel_diff_pct = (discrepancy_ML / vol_simpson_ML) * 100

print("==================================================")
print("TASK 16 MODIFIED: DAM DISCHARGE INTEGRATION")
print("==================================================")
print(f"Monitoring Period:          24.0 Hours (9 samples, h = 3 hr)")
print(f"Volume (Trapezoidal Rule):  {vol_trapezoid_m3:12.1f} m^3  ({vol_trapezoid_ML:.2f} Mega-Liters)")
print(f"Volume (Simpson's 1/3 Rule):{vol_simpson_m3:12.1f} m^3  ({vol_simpson_ML:.2f} Mega-Liters)")
print(f"Absolute Difference:        {discrepancy_ML:.2f} ML")
print(f"Relative Difference:        {rel_diff_pct:.4f}%")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(8, 4.5))
plt.plot(time_hours, flow_m3_s, "b-o", linewidth=2, label="Hydrograph Q(t)")
plt.fill_between(time_hours, flow_m3_s, color="skyblue", alpha=0.4, label="Integrated Volume Area")
plt.xlabel("Time Elapsed (Hours)")
plt.ylabel("Discharge Rate (m³/s)")
plt.title("Task 16 Modified: Hydroelectric Reservoir Discharge Hydrograph")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_16_dam_integration.png", dpi=150)
plt.close()
print("Saved plot to figures/task_16_dam_integration.png")
