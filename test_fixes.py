#!/usr/bin/env python3
"""Quick test of the calculator fixes."""

import sys

sys.path.insert(0, "/Users/silvanfrank/Github/annuitynest")
from logic import AnnuityCalculator

calc = AnnuityCalculator(
    "20260210 feedback/Fixed Annuity Rates.xlsx",
    "20260210 feedback/Variable Annuity Rates.xlsx",
)

print("=== TESTING FIXED ANNUITY ===")
print()

# Test with $100,000
results_100k = calc.get_fixed_rates(100000)
if results_100k:
    first = results_100k[0]
    print(f"With $100,000:")
    print(f"  {first['company']} - {first['product']}")
    print(f"  Base Rate: {first['base_rate']}%, Years: {first['years']}")
    print(f"  Future Value: ${first['future_value']:,.2f}")
    print()

# Test with $525,000
results_525k = calc.get_fixed_rates(525000)
if results_525k:
    first = results_525k[0]
    print(f"With $525,000:")
    print(f"  {first['company']} - {first['product']}")
    print(f"  Base Rate: {first['base_rate']}%, Years: {first['years']}")
    print(f"  Future Value: ${first['future_value']:,.2f}")
    print()

    # Verify the math
    expected_525k = 525000 * ((1 + first["base_rate"] / 100) ** first["years"])
    print(f"Expected (manual calculation): ${expected_525k:,.2f}")
    print(
        f"Match: {'YES' if abs(first['future_value'] - expected_525k) < 0.01 else 'NO'}"
    )
print()

# Test with different amounts to prove calculation works
print("=== VERIFYING FIXED ANNUITY MATH CHANGES WITH AMOUNT ===")
for amount in [100000, 250000, 525000, 750000]:
    results = calc.get_fixed_rates(amount)
    if results:
        first = results[0]
        print(
            f"Amount: ${amount:>10,} -> Future Value: ${first['future_value']:>15,.2f}"
        )

print()
print("=== TESTING VARIABLE ANNUITY ===")
print()

# Test with the exact inputs from the feedback
result = calc.get_variable_income(60, 65, 525000)
print(f"Variable Annuity Results for Age 60, Withdrawal 65, $525,000:")
print(f"Total products: {result['count']}")
print()

# Find Brighthouse FlexChoice Access - Level (not Expedite)
for prod in result["products"]:
    if (
        "brighthouse" in prod["carrier"].lower()
        and "flexchoice access - level" in prod["rider_name"].lower()
    ):
        print(f"Brighthouse FlexChoice Access - Level:")
        print(f"  Benefit Base: ${prod['benefit_base']:,.2f}")
        print(f"  Annual Lifetime Income: ${prod['annual_lifetime_income']:,.2f}")
        print(f"  Monthly Income: ${prod['monthly_income']:,.2f}")
        print()
        print("Expected from Excel:")
        print("  Benefit Base: $670,047.82")
        print("  Annual Income: $42,883.06")
        print()

        # Check if values match
        benefit_match = abs(prod["benefit_base"] - 670047.82) < 0.01
        income_match = abs(prod["annual_lifetime_income"] - 42883.06) < 0.01
        print(f"Benefit Base Match: {'YES' if benefit_match else 'NO'}")
        print(f"Income Match: {'YES' if income_match else 'NO'}")
        break

print()
print("=== TEST COMPLETE ===")
