#!/usr/bin/env python3
"""Test fixed annuity calculation with 10-year formula."""

import sys

sys.path.insert(0, "/Users/silvanfrank/Github/annuitynest")
from logic import AnnuityCalculator

calc = AnnuityCalculator(
    "/Users/silvanfrank/Github/annuitynest/excel files/Fixed Annuity Rates.xlsx",
    "/Users/silvanfrank/Github/annuitynest/excel files/Variable Annuity Rates.xlsx",
)

print("=== FIXED ANNUITY - 10 YEAR FORMULA ===")
print()

# Test with $1,000,000 (matching Excel C3)
results = calc.get_fixed_rates(1000000)
print(f"Total products: {len(results)}")
print()

# Show first 15 products to compare with Excel
print("First 15 products (sorted by Yield to Surrender):")
print("-" * 130)
print(
    f"{'Sort':<6} {'Company':<40} {'Product':<35} {'Years':<6} {'Yield':<10} {'Future Value':<20} {'Excel Value':<20}"
)
print("-" * 130)

for prod in results[:15]:
    # Calculate what Excel shows (hardcoded 10 years)
    excel_value = 1000000 * ((1 + prod["yield_to_surrender"] / 100) ** 10)
    match = "✓" if abs(prod["future_value"] - excel_value) < 0.01 else "✗"
    print(
        f"{prod['sort'] or '':<6} {prod['company']:<40.39} {prod['product']:<35.34} {prod['years'] or 'N/A':<6} {prod['yield_to_surrender']:<10.3f} ${prod['future_value']:>18,.2f} ${excel_value:>18,.2f} {match}"
    )

print()
print("First product verification:")
first = results[0]
print(f"  Product: {first['company']} - {first['product']}")
print(f"  Yield to Surrender: {first['yield_to_surrender']}%")
print(f"  Investment: $1,000,000")
print(f"  Formula: $1,000,000 × (1 + {first['yield_to_surrender']}%)^10")
print(f"  Result: ${first['future_value']:,.2f}")
print(f"  Expected from Excel: $1,676,037.42")

print()
print(f"\\nTotal: {len(results)} products")
