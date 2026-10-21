"""
BIT 2118: Scientific Computing
Task 11 (Modified Real-World Case): Corporate Bond Yield-to-Maturity (Newton vs Secant)
Part E Implementation
"""

import os
from scipy.optimize import root_scalar

# ---------------------------------------------------------
# Scenario: Semi-Annual Corporate Bond Yield to Maturity (YTM)
# Price P = sum_{t=1}^N [ C / (1+y)^t ] + [ Face / (1+y)^N ]
# f(y) = Present_Value(y) - P_market = 0
# ---------------------------------------------------------
# New Assumptions:
# 1. 5-Year bond maturing in 10 semi-annual periods (N = 10).
# 2. Face Value = $1,000.
# 3. Annual coupon rate = 6.0% (Semi-annual coupon C = $30.00).
# 4. Current trading market price = $975.50 (trading at a discount).

face_value = 1000.0
coupon = 30.0
n_periods = 10
market_price = 975.50

def bond_pricing_error(y):
    # y is semi-annual yield
    pv_coupons = sum(coupon / (1.0 + y)**t for t in range(1, n_periods + 1))
    pv_face = face_value / (1.0 + y)**n_periods
    return pv_coupons + pv_face - market_price

def d_bond_pricing_error(y):
    # Analytical derivative with respect to semi-annual yield y
    d_coupons = sum(-t * coupon / (1.0 + y)**(t + 1) for t in range(1, n_periods + 1))
    d_face = -n_periods * face_value / (1.0 + y)**(n_periods + 1)
    return d_coupons + d_face

# Newton-Raphson method with derivative
sol_newton = root_scalar(
    bond_pricing_error,
    fprime=d_bond_pricing_error,
    x0=0.03,
    method="newton",
    xtol=1e-12
)

# Secant method using two initial guesses
sol_secant = root_scalar(
    bond_pricing_error,
    x0=0.02,
    x1=0.05,
    method="secant",
    xtol=1e-12
)

semi_ytm_newton = sol_newton.root
annual_ytm_newton = 2.0 * semi_ytm_newton
semi_ytm_secant = sol_secant.root
annual_ytm_secant = 2.0 * semi_ytm_secant

print("==================================================")
print("TASK 11 MODIFIED: BOND YIELD-TO-MATURITY (YTM)")
print("==================================================")
print(f"Market Clean Price:         ${market_price:.2f}")
print(f"Semi-Annual Yield (Newton): {semi_ytm_newton:.6%}")
print(f"Annualized Nominal YTM:     {annual_ytm_newton:.4%}")
print(f"Newton Iterations:          {sol_newton.iterations}")
print(f"Semi-Annual Yield (Secant): {semi_ytm_secant:.6%}")
print(f"Annualized Nominal YTM:     {annual_ytm_secant:.4%}")
print(f"Secant Iterations:          {sol_secant.iterations}")
print(f"Price Error at Solution:    {bond_pricing_error(semi_ytm_newton):.4e}")
