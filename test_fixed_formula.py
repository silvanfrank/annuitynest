#!/usr/bin/env python3
"""Test the fixed annuity calculation with Yield to Surrender formula."""

import sys

sys.path.insert(0, "/Users/silvanfrank/Github/annuitynest")
from logic import AnnuityCalculator

calc = AnnuityCalculator(
    "20260210 feedback/Fixed Annuity Rates.xlsx",
    "20260210 feedback/Variable Annuity Rates.xlsx",
)

print("=== TESTING FIXED ANNUITY ===")
print()

# Test with $525,000
results = calc.get_fixed_rates(525000)
if results:
    print(f"Total products: {len(results)}")
    print()

    # Show first product
    first = results[0]
    print(f"First product: {first['company']} - {first['product']}")
    print(f"  Years: {first['years']}")
    print(f"  Base Rate: {first['base_rate']}%")
    print(f"  Yield to Surrender: {first['yield_to_surrender']}%")
    print(f"  Future Value: ${first['future_value']:,.2f}")
    print()

    # Verify calculation
    investment = 525000
    years = first["years"]
    yield_rate = first["yield_to_surrender"]
    expected = investment * ((1 + yield_rate / 100) ** years)
    print(f"Manual calculation:")
    print(f"  ${investment:,.0f} × (1 + {yield_rate}%)^({years}) = ${expected:,.2f}")
    print()

    # Show all products sorted by future value
    print("All products (sorted by Yield to Surrender):")
    print("-" * 100)
    print(
        f"{'Company':<35} {'Product':<30} {'Years':<6} {'Base Rate':<10} {'Yield':<10} {'Future Value':<15}"
    )
    print("-" * 100)

    for prod in results[:10]:  # Show first 10
        print(
            f"{prod['company']:<35.34} {prod['product']:<30.29} {prod['years']:<6} {prod['base_rate']:<10.2f} {prod['yield_to_surrender']:<10.3f} ${prod['future_value']:>14,.2f}"
        )

print()
print("=== TEST COMPLETE ===")
