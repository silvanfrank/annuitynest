#!/usr/bin/env python3
"""Test the formula-based variable annuity calculation."""

import sys

sys.path.insert(0, "/Users/silvanfrank/Github/annuitynest")
from logic import AnnuityCalculator

calc = AnnuityCalculator(
    "20260210 feedback/Fixed Annuity Rates.xlsx",
    "20260210 feedback/Variable Annuity Rates.xlsx",
)

# Test with Age 60, Withdrawal 65, 525000 (5 year deferral)
result = calc.get_variable_income(60, 65, 525000)
print("Variable Annuity Results for Age 60, Withdrawal 65, Investment: 525000")
print(f"Total products: {result['count']}")
print()

# Find Brighthouse FlexChoice
for prod in result["products"]:
    if (
        "brighthouse" in prod["carrier"].lower()
        and "flexchoice access - level" in prod["rider_name"].lower()
    ):
        print("Brighthouse FlexChoice Access - Level:")
        print(f"  Withdrawal Rate: {prod['withdrawal_rate']:.2f}%")
        print(f"  Benefit Base: {prod['benefit_base']:,.2f}")
        print(f"  Annual Lifetime Income: {prod['annual_lifetime_income']:,.2f}")
        print()

        # Verify calculation
        investment = 525000
        deferral_period = 5
        deferral_credit = 0.05  # 5%
        withdrawal_rate = 0.064  # 6.4%

        expected_benefit = investment * ((1 + deferral_credit) ** deferral_period)
        expected_income = expected_benefit * withdrawal_rate

        print("Manual calculation:")
        print(f"  Benefit Base = 525000 × (1 + 0.05)^5 = {expected_benefit:,.2f}")
        print(
            f"  Annual Income = {expected_benefit:,.2f} × 0.064 = {expected_income:,.2f}"
        )
        print()
        print("Expected from Excel:")
        print("  Benefit Base: 670047.82")
        print("  Annual Income: 42883.06")
        print()

        # Check match
        benefit_match = abs(prod["benefit_base"] - 670047.82) < 0.01
        income_match = abs(prod["annual_lifetime_income"] - 42883.06) < 0.01
        print(f"Benefit Base Match: {'YES' if benefit_match else 'NO'}")
        print(f"Income Match: {'YES' if income_match else 'NO'}")
        break
