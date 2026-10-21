"""
BIT 2118: Scientific Computing
Task 02 (Modified Real-World Case): Solar Photovoltaic (PV) Plant Power Generation Monitoring
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: Commercial Rooftop Solar PV Generation (500 kWp)
# 24 hourly AC power output readings in Kilowatts (kW)
# ---------------------------------------------------------
# New Assumptions:
# 1. Darkness occurs between 20:00 and 05:00 (zero generation).
# 2. Solar irradiance begins ramping up at 06:00, peaks around 12:00-13:00, and drops off by 19:00.
# 3. Peak grid feed-in tariff is $0.15/kWh (08:00 to 17:00), off-peak is $0.08/kWh.

hours = np.arange(24)
power_kw = np.array([
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0,     # 00:00 - 05:00
    12.4, 68.2, 175.5, 310.8, 420.0, 465.3, # 06:00 - 11:00
    485.0, 472.1, 430.5, 345.2, 210.0, 85.4, # 12:00 - 17:00
    18.2, 0.0, 0.0, 0.0, 0.0, 0.0      # 18:00 - 23:00
])

# Mathematical Operations: Summary statistics and energy conversion
daily_energy_kwh = np.sum(power_kw * 1.0) # Integral of power over 1-hour steps
peak_power_kw = np.max(power_kw)
mean_daytime_power = np.mean(power_kw[power_kw > 0])
nameplate_capacity = 500.0 # kW
capacity_utilization_factor = (daily_energy_kwh / (nameplate_capacity * 24)) * 100

# Revenue calculation with time-of-use tariff vectorization
tariff_rate = np.where((hours >= 8) & (hours <= 17), 0.15, 0.08) # $/kWh
hourly_revenue = power_kw * 1.0 * tariff_rate
total_daily_revenue = np.sum(hourly_revenue)

# Conversion from kW to MegaJoules (1 kWh = 3.6 MJ)
energy_mj = power_kw * 3.6

print("==================================================")
print("TASK 02 MODIFIED: SOLAR PV PLANT MONITORING")
print("==================================================")
print(f"Total Daily Energy Generated: {daily_energy_kwh:.2f} kWh")
print(f"Peak Power Output:            {peak_power_kw:.2f} kW")
print(f"Mean Daytime Power Output:    {mean_daytime_power:.2f} kW")
print(f"Capacity Utilization Factor:  {capacity_utilization_factor:.2f}%")
print(f"Estimated Daily Revenue:      ${total_daily_revenue:.2f}")
print("First 6 hours MegaJoules generation:", energy_mj[:6])

# Plotting the generation profile
os.makedirs("figures", exist_ok=True)
fig, ax1 = plt.subplots(figsize=(8, 4.5))

ax1.plot(hours, power_kw, color="#e67e22", marker="o", linewidth=2, label="AC Power (kW)")
ax1.fill_between(hours, power_kw, color="#f39c12", alpha=0.25)
ax1.set_xlabel("Hour of the Day (0-23)")
ax1.set_ylabel("Power Output (kW)", color="#d35400")
ax1.tick_params(axis='y', labelcolor="#d35400")
ax1.set_title("Task 02 Modified: Solar PV Generation Profile & Revenue")
ax1.grid(True, linestyle="--", alpha=0.6)

ax2 = ax1.twinx()
ax2.step(hours, hourly_revenue, color="#27ae60", where='mid', linewidth=1.5, linestyle=":", label="Hourly Revenue ($)")
ax2.set_ylabel("Revenue ($)", color="#27ae60")
ax2.tick_params(axis='y', labelcolor="#27ae60")

fig.tight_layout()
plt.savefig("figures/task_02_solar_pv.png", dpi=150)
plt.close()
print("Saved plot to figures/task_02_solar_pv.png")
