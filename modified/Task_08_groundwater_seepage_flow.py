"""
BIT 2118: Scientific Computing
Task 08 (Modified Real-World Case): Groundwater Piezometric Seepage Flow (Jacobi vs Gauss-Seidel)
Part E Implementation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Scenario: 1D Steady-State Confined Aquifer Piezometric Head
# Discretized Darcy-Laplace equation with 7 interior monitoring wells
# ---------------------------------------------------------
# New Assumptions:
# 1. Upstream boundary piezometric head (Reservoir): H_left = 85.0 meters.
# 2. Downstream boundary piezometric head (Canal): H_right = 18.0 meters.
# 3. Intermediate recharge from rainfall occurs at node 4 (+5.0 m head equivalent).
# 4. Tridiagonal finite-difference matrix equation A @ H = b.

n_interior = 7
A = np.diag(2.0 * np.ones(n_interior)) + \
    np.diag(-1.0 * np.ones(n_interior - 1), k=1) + \
    np.diag(-1.0 * np.ones(n_interior - 1), k=-1)

# RHS boundary vector with local recharge at center node
b = np.zeros(n_interior)
b[0] += 85.0    # Left boundary condition
b[-1] += 18.0   # Right boundary condition
b[3] += 5.0     # Artificial groundwater recharge well

def jacobi(A, b, tol=1e-8, max_iter=500):
    D = np.diag(A)
    R = A - np.diagflat(D)
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        x_new = (b - R @ x) / D
        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)
        if error < tol:
            return x_new, errors
        x = x_new
    return x, errors

def gauss_seidel(A, b, tol=1e-8, max_iter=500):
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (b[i] - A[i, :i] @ x[:i] - A[i, i+1:] @ old[i+1:]) / A[i, i]
        error = np.linalg.norm(x - old, ord=np.inf)
        errors.append(error)
        if error < tol:
            return x, errors
    return x, errors

x_j, err_j = jacobi(A, b)
x_gs, err_gs = gauss_seidel(A, b)
x_exact = np.linalg.solve(A, b)

print("==================================================")
print("TASK 08 MODIFIED: GROUNDWATER SEEPAGE FLOW")
print("==================================================")
print("Piezometric Heads (m):")
print("Jacobi:      ", np.round(x_j, 3))
print("Gauss-Seidel:", np.round(x_gs, 3))
print("Exact Direct:", np.round(x_exact, 3))
print(f"Jacobi Iterations:       {len(err_j)}")
print(f"Gauss-Seidel Iterations: {len(err_gs)}")
print(f"Gauss-Seidel Speedup:    {len(err_j)/len(err_gs):.1f}x fewer iterations")

os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(8, 4.5))
plt.semilogy(err_j, label=f"Jacobi ({len(err_j)} iters)", color="#e67e22", linewidth=2)
plt.semilogy(err_gs, label=f"Gauss-Seidel ({len(err_gs)} iters)", color="#2980b9", linewidth=2)
plt.xlabel("Iteration Count")
plt.ylabel("Maximum Absolute Error (inf-norm)")
plt.title("Task 08 Modified: Convergence Comparison (Aquifer Flow)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("figures/task_08_groundwater_convergence.png", dpi=150)
plt.close()
print("Saved plot to figures/task_08_groundwater_convergence.png")
