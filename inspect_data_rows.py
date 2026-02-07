import pandas as pd

print("VARIABLE ANNUITY - FORMATTED SHEET (Data rows)")
print("=" * 80)

df = pd.read_excel(
    "/Users/silvanfrank/Github/annuitynest/excel files/Variable Annuity Rates.xlsx",
    sheet_name="Formatted",
    header=None,
)

print("\nColumns 0-10 (first row is row 10 - header):")
print(df.iloc[9:13, 0:10])

print("\n\nColumns 10-20:")
print(df.iloc[9:13, 10:20])

print("\n\nColumns 15-20 (around column S which is index 18):")
print(df.iloc[9:13, 15:21])

print("\n\nRow 10 (index 9) all columns:")
for i, val in enumerate(df.iloc[9]):
    if pd.notna(val):
        print(f"  Column {i} ({chr(65 + i)}): {val}")

print("\n\n" + "=" * 80)
print("FIXED ANNUITY - FORMATTED 1 SHEET (Data rows)")
print("=" * 80)

df2 = pd.read_excel(
    "/Users/silvanfrank/Github/annuitynest/excel files/Fixed Annuity Rates.xlsx",
    sheet_name="FORMATTED 1",
    header=None,
)

print("\nData starting from row 9 (index 9):")
print(df2.iloc[9:15, :])
