import pandas as pd
import os

files = [
    "Fixed Annuity Rates.xlsx",
    "Variable Annuity Rates.xlsx"
]

for file in files:
    print(f"--- Inspecting {file} ---")
    try:
        xl = pd.ExcelFile(file)
        print(f"Sheet names: {xl.sheet_names}")
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, nrows=5)
            print(f"\nSheet: {sheet}")
            print(f"Columns: {list(df.columns)}")
            print(df.head(2).to_string())
    except Exception as e:
        print(f"Error reading {file}: {e}")
    print("\n")
