import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def clean_fixed_annuity_data(file_path):
    """
    Load fixed annuity data from the FORMATTED 1 sheet.
    Returns all columns and all rows as requested.
    """
    try:
        # Read from FORMATTED 1 sheet which has the calculation results
        df = pd.read_excel(file_path, sheet_name="FORMATTED 1", header=None)

        data_rows = []

        # Data starts from row 10 (index 9)
        for idx in range(9, len(df)):
            row = df.iloc[idx]

            # Check if this is a data row (has company name in column 1)
            if pd.notna(row[1]) and isinstance(row[1], str):
                # Skip header rows
                if "Company" in str(row[1]) or "Inputs from website" in str(row[1]):
                    continue

                company = row[1]
                product = row[2] if pd.notna(row[2]) else ""
                years = parse_rate_term(row[3]) if pd.notna(row[3]) else None
                min_contrib = parse_currency(row[4]) if pd.notna(row[4]) else 0
                min_rate = parse_percentage(row[5]) if pd.notna(row[5]) else 0
                base_rate = parse_percentage(row[6]) if pd.notna(row[6]) else 0
                bonus_rate = parse_percentage(row[7]) if pd.notna(row[7]) else 0
                yield_to_surr = parse_percentage(row[8]) if pd.notna(row[8]) else 0
                surrender_period = parse_rate_term(row[9]) if pd.notna(row[9]) else None
                future_value = parse_currency(row[10]) if pd.notna(row[10]) else 0

                data_rows.append(
                    {
                        "Sort": row[0] if pd.notna(row[0]) else None,
                        "Company": company,
                        "Product": product,
                        "Years": years,
                        "Min Contribution": min_contrib,
                        "Min Rate": min_rate,
                        "Base Rate": base_rate,
                        "Bonus Rate": bonus_rate,
                        "Yield to Surrender": yield_to_surr,
                        "Surrender Period": surrender_period,
                        "Future Value": future_value,
                    }
                )

        cleaned_df = pd.DataFrame(data_rows)
        logger.info(
            f"Loaded {len(cleaned_df)} fixed annuity products from FORMATTED 1 sheet"
        )
        return cleaned_df

    except Exception as e:
        logger.error(f"Error cleaning fixed annuity data: {str(e)}")
        raise


def load_variable_annuity_data(file_path):
    """
    Load variable annuity data from the Formatted sheet.
    Returns columns B, C, E, S as requested (Annuity Type, Carrier, Rider Name, Lifetime Income1)
    """
    try:
        # Read from Formatted sheet
        df = pd.read_excel(file_path, sheet_name="Formatted", header=None)

        data_rows = []

        # Data starts from row 11 (index 10) - row 10 is the header
        for idx in range(10, len(df)):
            row = df.iloc[idx]

            # Check if this is a data row (has sort number in column 0)
            sort_val = row[0]
            if pd.notna(sort_val):
                # Try to convert to int - if it fails, it's not a data row
                try:
                    sort_num = int(float(sort_val))
                except (ValueError, TypeError):
                    continue

                # Column B (index 1): Annuity Type - should be "Variable"
                annuity_type = str(row[1]).strip() if pd.notna(row[1]) else ""

                # Skip rows that don't have "Variable" as annuity type
                if annuity_type != "Variable":
                    continue

                # Column C (index 2): Carrier - should be a company name
                carrier = str(row[2]).strip() if pd.notna(row[2]) else ""

                # Skip rows with empty or invalid carrier
                if not carrier or carrier in ["", "NaN", "nan"]:
                    continue

                # Column E (index 4): Rider Name
                rider_name = str(row[4]).strip() if pd.notna(row[4]) else ""

                # Column S (index 18): Lifetime Income1
                lifetime_income = parse_currency(row[18]) if pd.notna(row[18]) else 0

                # Also get additional useful columns
                withdrawal_rate = parse_percentage(row[16]) if pd.notna(row[16]) else 0
                benefit_base = parse_currency(row[15]) if pd.notna(row[15]) else 0

                data_rows.append(
                    {
                        "Sort": sort_num,
                        "Annuity Type": annuity_type,
                        "Carrier": carrier,
                        "Rider Name": rider_name,
                        "Withdrawal Rate": withdrawal_rate,
                        "Benefit Base": benefit_base,
                        "Annual Lifetime Income": lifetime_income,
                    }
                )

        result_df = pd.DataFrame(data_rows)
        logger.info(
            f"Loaded {len(result_df)} variable annuity products from Formatted sheet"
        )
        return result_df

    except Exception as e:
        logger.error(f"Error loading variable annuity data: {str(e)}")
        raise


def parse_rate_term(value):
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return int(value)

    value_str = str(value).strip()

    import re

    match = re.search(r"(\d+)", value_str)
    if match:
        return int(match.group(1))

    return None


def parse_currency(value):
    if pd.isna(value):
        return 0

    if isinstance(value, (int, float)):
        return float(value)

    value_str = str(value).strip()
    value_str = (
        value_str.replace("$", "").replace("'", "").replace(",", "").replace("%", "")
    )

    try:
        return float(value_str)
    except:
        return 0


def parse_percentage(value):
    if pd.isna(value):
        return 0

    if isinstance(value, (int, float)):
        return float(value)

    value_str = str(value).strip()
    value_str = value_str.replace("%", "").replace("$", "").replace(",", "")

    try:
        return float(value_str)
    except:
        return 0
