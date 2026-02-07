import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def clean_fixed_annuity_data(file_path):
    try:
        df = pd.read_excel(file_path, header=None)

        data_rows = []
        current_company = None

        for idx in range(len(df)):
            row = df.iloc[idx]

            if pd.isna(row[0]) and pd.notna(row[1]):
                if pd.notna(row[1]) and isinstance(row[1], str):
                    current_company = row[1]

            elif pd.notna(row[1]) and isinstance(row[1], str):
                if "Product Name" in str(row[1]) or "Company Name" in str(row[1]):
                    continue

                product_name = row[1]
                product_type = row[2] if pd.notna(row[2]) else ""
                premium_type = row[3] if pd.notna(row[3]) else ""
                rate_term = parse_rate_term(row[4]) if pd.notna(row[4]) else None
                min_contrib = parse_currency(row[5]) if pd.notna(row[5]) else 0
                min_rate = parse_percentage(row[6]) if pd.notna(row[6]) else 0
                base_rate = parse_percentage(row[7]) if pd.notna(row[7]) else 0
                bonus_rate = parse_percentage(row[8]) if pd.notna(row[8]) else 0
                yield_to_surr = parse_percentage(row[9]) if pd.notna(row[9]) else 0
                surrender_period = row[10] if pd.notna(row[10]) else None

                if current_company and product_name:
                    data_rows.append(
                        {
                            "Company": current_company,
                            "Product": product_name,
                            "Product Type": product_type,
                            "Premium Type": premium_type,
                            "Rate Term": rate_term,
                            "Min Contribution": min_contrib,
                            "Min Rate": min_rate,
                            "Base Rate": base_rate,
                            "Bonus Rate": bonus_rate,
                            "Yield to Surrender": yield_to_surr,
                            "Surrender Period": surrender_period,
                        }
                    )

        cleaned_df = pd.DataFrame(data_rows)
        logger.info(f"Loaded {len(cleaned_df)} fixed annuity products")
        return cleaned_df

    except Exception as e:
        logger.error(f"Error cleaning fixed annuity data: {str(e)}")
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
    value_str = value_str.replace("$", "").replace(",", "").replace("%", "")

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


def load_variable_annuity_data(file_path):
    try:
        xls = pd.ExcelFile(file_path)

        dfs = {}
        for sheet_name in xls.sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                dfs[sheet_name] = df
            except Exception as e:
                logger.warning(f"Could not read sheet {sheet_name}: {str(e)}")

        logger.info(f"Loaded {len(dfs)} variable annuity sheets")
        return dfs

    except Exception as e:
        logger.error(f"Error loading variable annuity data: {str(e)}")
        raise
