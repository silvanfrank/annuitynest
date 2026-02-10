#!/usr/bin/env python3
"""Test showing all fixed annuity products without filtering."""

import sys

sys.path.insert(0, "/Users/silvanfrank/Github/annuitynest")
from logic import AnnuityCalculator

calc = AnnuityCalculator(
    "20260210 feedback/Fixed Annuity Rates.xlsx",
    "20260210 feedback/Variable Annuity Rates.xlsx",
)

print("=== FIXED ANNUITY - ALL PRODUCTS ===")
print()

# Test with $100,000 (should now show all products from Excel)
results = calc.get_fixed_rates(100000)
print(f"Total products: {len(results)}")
print()

# Show first 15 products to compare with Excel
print("First 15 products (sorted by Base Rate):")
print("-" * 120)
print(
    f"{'Sort':<6} {'Company':<35} {'Product':<40} {'Years':<6} {'Base Rate':<10} {'Yield':<10} {'Future Value':<15}"
)
print("-" * 120)

for prod in results[:15]:
    print(
        f"{prod['sort'] or '':<6} {prod['company']:<35.34} {prod['product']:<40.39} {prod['years'] or 'N/A':<6} {prod['base_rate']:<10.2f} {prod['yield_to_surrender']:<10.3f} ${prod['future_value']:>14,.2f}"
    )

print()
print(f"Showing {len(results)} total products (all rows from Excel)")
