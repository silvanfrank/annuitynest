#!/usr/bin/env python3
"""Test script to verify the Excel data processing works correctly."""

import sys
import os

sys.path.insert(0, "/Users/silvanfrank/Github/annuitynest")

from data_processor import clean_fixed_annuity_data, load_variable_annuity_data
from logic import AnnuityCalculator

EXCEL_DIR = "/Users/silvanfrank/Github/annuitynest/excel files"


def test_fixed_annuity():
    print("=" * 80)
    print("TESTING FIXED ANNUITY")
    print("=" * 80)

    try:
        fixed_path = os.path.join(EXCEL_DIR, "Fixed Annuity Rates.xlsx")
        df = clean_fixed_annuity_data(fixed_path)

        print(f"\n✓ Loaded {len(df)} fixed annuity products")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 3 products:")
        print(df.head(3).to_string())

        # Test filtering
        filtered = df[df["Min Contribution"] <= 100000]
        print(f"\n✓ Filtered to {len(filtered)} products for $100,000 investment")

        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_variable_annuity():
    print("\n\n" + "=" * 80)
    print("TESTING VARIABLE ANNUITY")
    print("=" * 80)

    try:
        variable_path = os.path.join(EXCEL_DIR, "Variable Annuity Rates.xlsx")
        df = load_variable_annuity_data(variable_path)

        print(f"\n✓ Loaded {len(df)} variable annuity products")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 3 products:")
        print(df.head(3).to_string())

        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_calculator():
    print("\n\n" + "=" * 80)
    print("TESTING ANNUITY CALCULATOR")
    print("=" * 80)

    try:
        fixed_path = os.path.join(EXCEL_DIR, "Fixed Annuity Rates.xlsx")
        variable_path = os.path.join(EXCEL_DIR, "Variable Annuity Rates.xlsx")

        calc = AnnuityCalculator(fixed_path, variable_path)

        # Test fixed annuity
        print("\nTesting Fixed Annuity calculation...")
        fixed_results = calc.get_fixed_rates(100000)
        print(f"✓ Got {len(fixed_results)} fixed annuity results")
        if fixed_results:
            print(f"\nFirst fixed result:")
            for key, value in fixed_results[0].items():
                print(f"  {key}: {value}")

        # Test variable annuity
        print("\nTesting Variable Annuity calculation...")
        variable_result = calc.get_variable_income(55, 65, 100000)
        print(f"✓ Got {variable_result['count']} variable annuity products")
        if variable_result["products"]:
            print(f"\nFirst variable result:")
            for key, value in variable_result["products"][0].items():
                print(f"  {key}: {value}")

        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\nRunning Annuity Calculator Tests...\n")

    fixed_ok = test_fixed_annuity()
    variable_ok = test_variable_annuity()
    calc_ok = test_calculator()

    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Fixed Annuity: {'✓ PASS' if fixed_ok else '✗ FAIL'}")
    print(f"Variable Annuity: {'✓ PASS' if variable_ok else '✗ FAIL'}")
    print(f"Calculator: {'✓ PASS' if calc_ok else '✗ FAIL'}")
    print("=" * 80)

    if fixed_ok and variable_ok and calc_ok:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
