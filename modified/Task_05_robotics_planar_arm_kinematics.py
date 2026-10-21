"""
BIT 2118: Scientific Computing
Task 05 (Modified Real-World Case): Robotic Manipulator Planar Kinematics
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: 2-Link Robotic Arm Tool-Tip Coordinate Mapping
# Homogeneous 3x3 Transformation (Rotation + Scaling + Translation)
# ---------------------------------------------------------
# New Assumptions:
# 1. An end-effector gripper has a square workpiece footprint defined in its local frame:
#    corners at [0,0], [15,0], [15,10], [0,10] (mm).
# 2. Joint rotation theta = 60 degrees.
# 3. Micro-scale calibration factor Sx = 1.05, Sy = 0.95.
# 4. Joint translation to world origin dx = 120 mm, dy = 80 mm.

tool_local = np.array([
    [0.0, 0.0, 1.0],
    [15.0, 0.0, 1.0],
    [15.0, 10.0, 1.0],
    [0.0, 10.0, 1.0],
    [0.0, 0.0, 1.0] # close polygon
])

theta = np.deg2rad(60)
dx, dy = 120.0, 80.0
sx, sy = 1.05, 0.95

# 3x3 Homogeneous transformation matrix: T = Translation @ Rotation @ Scale
T = np.array([
    [sx * np.cos(theta), -sy * np.sin(theta), dx],
    [sx * np.sin(theta),  sy * np.cos(theta), dy],
    [0.0,                 0.0,                1.0]
])

# Transform points (each row is [x, y, 1], so P_world = P_local @ T.T)
tool_world = tool_local @ T.T

det_linear_submatrix = np.linalg.det(T[:2, :2])

print("==================================================")
print("TASK 05 MODIFIED: ROBOTIC ARM TOOL TRANSFORMATION")
print("==================================================")
print("Homogeneous Transformation Matrix T (3x3):\n", T)
print("\nLocal Gripper Coordinates (mm):\n", tool_local[:, :2])
print("\nWorld Workspace Coordinates (mm):\n", tool_world[:, :2])
print(f"\nLinear Submatrix Determinant (Area scale): {det_linear_submatrix:.4f}")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(7, 6))
plt.plot(tool_local[:, 0], tool_local[:, 1], "b--o", label="Local Gripper Frame", linewidth=1.5)
plt.plot(tool_world[:, 0], tool_world[:, 1], "r-s", label="World Workpiece Frame", linewidth=2)
plt.title("Task 05 Modified: Robotic Kinematic Frame Transformation")
plt.xlabel("X Coordinate (mm)")
plt.ylabel("Y Coordinate (mm)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.axis("equal")
plt.tight_layout()
plt.savefig("figures/task_05_robotics_transform.png", dpi=150)
plt.close()
print("Saved plot to figures/task_05_robotics_transform.png")
