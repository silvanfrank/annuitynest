import pandas as pd
import numpy as np
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
excel_dir = os.path.join(script_dir, "excel files")

# Detailed analysis of Fixed Annuity Rates
print("=== FIXED ANNUITY RATES - STRUCTURE ANALYSIS ===\n")

# Read without skipping to see raw structure
df_fixed_raw = pd.read_excel(
    os.path.join(excel_dir, "Fixed Annuity Rates.xlsx"),
    sheet_name="ORIGINAL DATA",
    header=None,
)
print(f"Total rows: {len(df_fixed_raw)}")
print(f"\nFirst 20 rows (raw):")
print(df_fixed_raw.iloc[:20].to_string())

print("\n\n=== VARIABLE ANNUITY RATES - STRUCTURE ANALYSIS ===\n")

# Read the Original sheet
df_var_raw = pd.read_excel(
    os.path.join(excel_dir, "Variable Annuity Rates.xlsx"),
    sheet_name="Original",
    header=None,
)
print(f"Total rows: {len(df_var_raw)}")
print(f"\nFirst 50 rows:")
print(df_var_raw.iloc[:50].to_string())

# Look for age bands
print("\n\n=== Looking for Age-based withdrawal rates ===")
for i, row in df_var_raw.iterrows():
    if pd.notna(row[0]) and "age" in str(row[0]).lower():
        print(f"Row {i}: {row[0]}")
        print(df_var_raw.iloc[i : i + 15].to_string())
        break
