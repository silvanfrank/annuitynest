import pandas as pd
import sys

# Inspect Variable Annuity Excel file
print("=" * 80)
print("VARIABLE ANNUITY RATES - SHEET INSPECTION")
print("=" * 80)

try:
    xls = pd.ExcelFile(
        "/Users/silvanfrank/Github/annuitynest/excel files/Variable Annuity Rates.xlsx"
    )
    print(f"\nSheet names: {xls.sheet_names}")

    for sheet_name in xls.sheet_names:
        print(f"\n{'=' * 80}")
        print(f"SHEET: {sheet_name}")
        print("=" * 80)

        df = pd.read_excel(
            "/Users/silvanfrank/Github/annuitynest/excel files/Variable Annuity Rates.xlsx",
            sheet_name=sheet_name,
        )

        print(f"\nShape: {df.shape}")
        print(f"\nColumns (first 20): {list(df.columns[:20])}")
        print(
            f"\nColumns (20-40): {list(df.columns[20:40]) if len(df.columns) > 20 else 'N/A'}"
        )
        print(
            f"\nColumns (40-60): {list(df.columns[40:60]) if len(df.columns) > 40 else 'N/A'}"
        )

        # Show first few rows
        print(f"\nFirst 5 rows:")
        print(df.head().to_string())

        # Show row 11 (the header row based on screenshot)
        if len(df) > 10:
            print(f"\nRow 11 (index 10):")
            print(df.iloc[10].to_string())

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("FIXED ANNUITY RATES - SHEET INSPECTION")
print("=" * 80)

try:
    xls = pd.ExcelFile(
        "/Users/silvanfrank/Github/annuitynest/excel files/Fixed Annuity Rates.xlsx"
    )
    print(f"\nSheet names: {xls.sheet_names}")

    for sheet_name in xls.sheet_names:
        print(f"\n{'=' * 80}")
        print(f"SHEET: {sheet_name}")
        print("=" * 80)

        df = pd.read_excel(
            "/Users/silvanfrank/Github/annuitynest/excel files/Fixed Annuity Rates.xlsx",
            sheet_name=sheet_name,
        )

        print(f"\nShape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")

        # Show first few rows
        print(f"\nFirst 5 rows:")
        print(df.head().to_string())

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
