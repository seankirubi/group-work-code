"""
BIT 2118: Scientific Computing
Task 07 (Modified Real-World Case): Bridge Truss Multi-Load Displacement via LU Decomposition
Part E Implementation
"""

import os
import numpy as np
from scipy.linalg import lu_factor, lu_solve

# ---------------------------------------------------------
# Scenario: 4-DOF Bridge Truss Structure Stiffness Analysis
# K @ u = F  -->  Factor K once into P, L, U; solve multiple F
# ---------------------------------------------------------
# New Assumptions:
# 1. Structural stiffness matrix K (kN/mm) is fixed by truss geometry and steel modulus.
# 2. Three distinct engineering load cases F (kN) act on the 4 joint DOFs:
#    Case 1: Baseline Dead Load (truss self-weight)
#    Case 2: Rush-Hour Live Load (heavy vehicular convoy)
#    Case 3: Extreme Severe Wind Shear + Dynamic Load

K = np.array([
    [ 45.0, -18.0,   0.0,  -5.0],
    [-18.0,  52.0, -20.0,   0.0],
    [  0.0, -20.0,  48.0, -15.0],
    [ -5.0,   0.0, -15.0,  35.0]
])

load_scenarios = {
    "Dead Load Only (kN)": np.array([25.0, 30.0, 30.0, 20.0]),
    "Peak Live Load (kN)":  np.array([80.0, 110.0, 95.0, 60.0]),
    "Storm Wind Shear (kN)":np.array([120.0, 65.0, 40.0, 90.0])
}

# Factor stiffness matrix once
lu, piv = lu_factor(K)

print("==================================================")
print("TASK 07 MODIFIED: STRUCTURAL TRUSS LU SOLVER")
print("==================================================")
for name, F in load_scenarios.items():
    u = lu_solve((lu, piv), F) # Displacements in mm
    res = F - K @ u
    res_norm = np.linalg.norm(res)
    print(f"\n--- {name} ---")
    print(f"Applied Forces:      {F}")
    print(f"Joint Displacements (mm): u1={u[0]:.3f}, u2={u[1]:.3f}, u3={u[2]:.3f}, u4={u[3]:.3f}")
    print(f"Max Displacement:    {np.max(np.abs(u)):.3f} mm")
    print(f"Residual Norm:       {res_norm:.3e} kN")
