"""
BIT 2118: Scientific Computing
Task 09 (Modified Real-World Case): Google PageRank on Directed Web Hyperlink Graph
Part E Implementation
"""

import os
import numpy as np

# ---------------------------------------------------------
# Scenario: 5-Page Directed Website Navigation Network
# G @ p = 1.0 * p  --> Dominant Eigenvector equals PageRank
# ---------------------------------------------------------
# New Assumptions:
# Pages: 0:Home, 1:Product, 2:Pricing, 3:Blog, 4:Contact
# Outgoing links:
# Home (0) -> Product (1), Pricing (2), Blog (3)
# Product (1) -> Pricing (2), Contact (4)
# Pricing (2) -> Contact (4), Home (0)
# Blog (3) -> Home (0), Product (1)
# Contact (4) -> Home (0)

# Raw directed link matrix (A[i, j] = 1 if link from i to j)
A = np.array([
    [0., 1., 1., 1., 0.],
    [0., 0., 1., 0., 1.],
    [1., 0., 0., 0., 1.],
    [1., 1., 0., 0., 0.],
    [1., 0., 0., 0., 0.]
])

N = A.shape[0]
out_degree = A.sum(axis=1)

# Transition probability matrix (row stochastic)
P = A / out_degree[:, np.newaxis]

# Google PageRank Matrix with random teleportation damping factor d = 0.85
d = 0.85
# Transition operates on column probability vectors: G = d * P.T + (1-d)/N * ones
G = d * P.T + ((1.0 - d) / N) * np.ones((N, N))

eigenvalues, eigenvectors = np.linalg.eig(G)

# Find dominant eigenvalue (should theoretically be 1.0)
index = np.argmax(np.real(eigenvalues))
dominant_val = np.real(eigenvalues[index])
dominant_vec = np.abs(np.real(eigenvectors[:, index]))
pagerank = dominant_vec / dominant_vec.sum()

pages = ["0: Home", "1: Product", "2: Pricing", "3: Blog", "4: Contact"]

print("==================================================")
print("TASK 09 MODIFIED: GOOGLE PAGERANK EIGENVALUES")
print("==================================================")
print(f"Dominant Eigenvalue: {dominant_val:.6f}")
print("Verification Error ||G @ v - lambda * v||:",
      np.linalg.norm(G @ dominant_vec - dominant_val * dominant_vec))
print("\nPageRank Influence Scores:")
ranked_indices = np.argsort(pagerank)[::-1]
for rank, idx in enumerate(ranked_indices, start=1):
    print(f"Rank {rank}: {pages[idx]:<12} Score = {pagerank[idx]:.4f} ({pagerank[idx]*100:.2f}%)")
