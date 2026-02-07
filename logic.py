import pandas as pd
import logging
from data_processor import clean_fixed_annuity_data, load_variable_annuity_data

logger = logging.getLogger(__name__)

WITHDRAWAL_RATES = {
    59: 0.0475,
    60: 0.0475,
    61: 0.0475,
    62: 0.0475,
    63: 0.0475,
    64: 0.0475,
    65: 0.0635,
    66: 0.0635,
    67: 0.0635,
    68: 0.0635,
    69: 0.0635,
    70: 0.0655,
    71: 0.0655,
    72: 0.0655,
    73: 0.0655,
    74: 0.0655,
    75: 0.0675,
    76: 0.0675,
    77: 0.0675,
    78: 0.0675,
    79: 0.0675,
    80: 0.0690,
}


class AnnuityCalculator:
    def __init__(self, fixed_file_path, variable_file_path):
        self.fixed_data = None
        self.variable_data = None

        try:
            self.fixed_data = clean_fixed_annuity_data(fixed_file_path)
            logger.info("Fixed annuity data loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load fixed annuity data: {str(e)}")

        try:
            self.variable_data = load_variable_annuity_data(variable_file_path)
            logger.info("Variable annuity data loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load variable annuity data: {str(e)}")

    def validate_input(self, data):
        errors = []

        required_fields = ["amount", "annuity_type"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.replace('_', ' ').title()} is required")

        try:
            amount = float(data.get("amount", 0))
            if amount < 50000:
                errors.append("Amount must be at least $50,000")
        except:
            errors.append("Amount must be a valid number")

        annuity_type = data.get("annuity_type", "").lower()
        if annuity_type == "variable":
            try:
                current_age = int(data.get("current_age", 0))
                if current_age < 18 or current_age > 100:
                    errors.append("Current Age must be between 18 and 100")
            except:
                errors.append("Current Age is required for Variable annuities")

            try:
                withdrawal_age = int(data.get("withdrawal_age", 0))
                if withdrawal_age < 59:
                    errors.append("Age of First Withdrawal must be at least 59")
                if withdrawal_age > 100:
                    errors.append("Age of First Withdrawal must be 100 or less")
            except:
                errors.append(
                    "Age of First Withdrawal is required for Variable annuities"
                )

            try:
                current_age = int(data.get("current_age", 0))
                withdrawal_age = int(data.get("withdrawal_age", 0))
                if withdrawal_age <= current_age:
                    errors.append(
                        "Age of First Withdrawal must be greater than Current Age"
                    )
            except:
                pass

        return errors if errors else None

    def get_fixed_rates(self, amount, state=None):
        if self.fixed_data is None:
            return []

        filtered = self.fixed_data[self.fixed_data["Min Contribution"] <= amount].copy()

        if len(filtered) == 0:
            return []

        filtered = filtered.sort_values("Base Rate", ascending=False)

        results = []
        for _, row in filtered.head(10).iterrows():
            results.append(
                {
                    "company": str(row["Company"]),
                    "product": str(row["Product"]),
                    "product_type": str(row["Product Type"]),
                    "base_rate": float(row["Base Rate"])
                    if pd.notna(row["Base Rate"])
                    else 0,
                    "rate_term": int(row["Rate Term"])
                    if pd.notna(row["Rate Term"])
                    else None,
                    "min_contribution": float(row["Min Contribution"]),
                    "surrender_period": str(row["Surrender Period"])
                    if pd.notna(row["Surrender Period"])
                    else "",
                }
            )

        return results

    def get_variable_income(self, current_age, withdrawal_age, amount):
        deferral_period = withdrawal_age - current_age

        if withdrawal_age in WITHDRAWAL_RATES:
            withdrawal_rate = WITHDRAWAL_RATES[withdrawal_age]
        elif withdrawal_age > 80:
            withdrawal_rate = 0.0690
        else:
            withdrawal_rate = 0.0475

        annual_income = amount * withdrawal_rate
        monthly_income = annual_income / 12

        return {
            "current_age": current_age,
            "withdrawal_age": withdrawal_age,
            "deferral_period": deferral_period,
            "investment_amount": amount,
            "withdrawal_rate": round(withdrawal_rate * 100, 2),
            "annual_income": round(annual_income, 2),
            "monthly_income": round(monthly_income, 2),
            "disclaimer": "Rates are estimates based on average market rates. Actual rates may vary by carrier.",
        }
