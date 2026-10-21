"""
BIT 2118: Scientific Computing
Task 06 (Modified Real-World Case): Electrical DC Circuit Mesh Current Analysis
Part E Implementation
"""

import os
import numpy as np

# ---------------------------------------------------------
# Scenario: 3-Loop Electrical Network Analysis (KVL)
# R @ I = V  -->  Solve for Mesh Currents I = [I1, I2, I3]^T
# ---------------------------------------------------------
# New Assumptions:
# Loop 1: R1=10 ohms, R12=5 ohms (shared with loop 2), Source V1 = 24.0 V
# Loop 2: R2=8 ohms, R12=5 ohms, R23=4 ohms (shared with loop 3), Source V2 = 0.0 V
# Loop 3: R3=12 ohms, R23=4 ohms, Source V3 = -10.0 V (opposing battery)

# Self-resistance and mutual resistance matrix (Ohms):
# R11 = 10+5 = 15; R12 = -5; R13 = 0
# R21 = -5; R22 = 5+8+4 = 17; R23 = -4
# R31 = 0; R32 = -4; R33 = 4+12 = 16
R = np.array([
    [15.0,  -5.0,   0.0],
    [-5.0,  17.0,  -4.0],
    [ 0.0,  -4.0,  16.0]
])

V = np.array([24.0, 0.0, -10.0]) # Loop EMFs in Volts

currents = np.linalg.solve(R, V)
residual = V - R @ currents
residual_norm = np.linalg.norm(residual)

# Branch currents
i_loop1 = currents[0]
i_loop2 = currents[1]
i_loop3 = currents[2]
i_shared_12 = i_loop1 - i_loop2
i_shared_23 = i_loop2 - i_loop3

# Total power dissipation: sum(I_k^2 * R_k)
power_total = (i_loop1**2 * 10.0 + 
               i_shared_12**2 * 5.0 + 
               i_loop2**2 * 8.0 + 
               i_shared_23**2 * 4.0 + 
               i_loop3**2 * 12.0)

print("==================================================")
print("TASK 06 MODIFIED: ELECTRICAL MESH ANALYSIS")
print("==================================================")
print(f"Mesh Current I1: {currents[0]:.4f} Amperes")
print(f"Mesh Current I2: {currents[1]:.4f} Amperes")
print(f"Mesh Current I3: {currents[2]:.4f} Amperes")
print(f"Branch Current (R12 shared): {i_shared_12:.4f} A")
print(f"Branch Current (R23 shared): {i_shared_23:.4f} A")
print(f"Total Circuit Power Dissipation: {power_total:.2f} Watts")
print("Verification (R @ I):", R @ currents)
print(f"Residual Norm: {residual_norm:.3e} V")
