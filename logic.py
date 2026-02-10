import pandas as pd
import logging
from data_processor import clean_fixed_annuity_data, load_variable_annuity_data

logger = logging.getLogger(__name__)


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

    def calculate_fixed_future_value(self, amount, base_rate, years):
        """
        Calculate future value using compound interest formula.
        Formula: FV = P × (1 + r)^n
        Where P = principal (amount), r = rate (as decimal), n = years
        """
        if years is None or years <= 0:
            return amount
        rate_decimal = base_rate / 100.0
        future_value = amount * ((1 + rate_decimal) ** years)
        return round(future_value, 2)

    def get_fixed_rates(self, amount, state=None):
        """
        Return all fixed annuity products with all columns.
        Filter by minimum contribution amount.
        Calculate future value based on user's investment amount.
        """
        if self.fixed_data is None:
            logger.error("Fixed annuity data not loaded")
            return []

        # Filter products where Min Contribution <= user amount
        filtered = self.fixed_data[self.fixed_data["Min Contribution"] <= amount].copy()

        if len(filtered) == 0:
            logger.info(f"No fixed annuity products found for amount ${amount}")
            return []

        # Sort by Base Rate descending
        filtered = filtered.sort_values("Base Rate", ascending=False)

        # Convert to list of dicts with all columns
        results = []
        for _, row in filtered.iterrows():
            years = int(row["Years"]) if pd.notna(row["Years"]) else None
            base_rate = float(row["Base Rate"]) if pd.notna(row["Base Rate"]) else 0

            # Calculate future value based on user's actual investment amount
            future_value = self.calculate_fixed_future_value(amount, base_rate, years)

            result = {
                "sort": int(row["Sort"]) if pd.notna(row["Sort"]) else None,
                "company": str(row["Company"]) if pd.notna(row["Company"]) else "",
                "product": str(row["Product"]) if pd.notna(row["Product"]) else "",
                "years": years,
                "min_contribution": float(row["Min Contribution"])
                if pd.notna(row["Min Contribution"])
                else 0,
                "min_rate": float(row["Min Rate"]) if pd.notna(row["Min Rate"]) else 0,
                "base_rate": base_rate,
                "bonus_rate": float(row["Bonus Rate"])
                if pd.notna(row["Bonus Rate"])
                else 0,
                "yield_to_surrender": float(row["Yield to Surrender"])
                if pd.notna(row["Yield to Surrender"])
                else 0,
                "surrender_period": int(row["Surrender Period"])
                if pd.notna(row["Surrender Period"])
                else None,
                "future_value": future_value,
            }
            results.append(result)

        logger.info(f"Returning {len(results)} fixed annuity products")
        return results

    def get_variable_income(self, current_age, withdrawal_age, amount):
        """
        Return all variable annuity products with columns B, C, E, S.
        Filter by matching withdrawal age with the data.
        """
        if self.variable_data is None:
            logger.error("Variable annuity data not loaded")
            return []

        deferral_period = withdrawal_age - current_age

        # Get the base investment amount from the Excel file
        # This is the amount the Excel calculations are based on
        base_investment = self.variable_data.attrs.get("base_investment", 1000000)
        logger.info(
            f"Scaling variable annuity from base ${base_investment:,.2f} to user amount ${amount:,.2f}"
        )

        # Return all variable annuity products
        results = []
        for _, row in self.variable_data.iterrows():
            # Calculate the income based on user's investment amount
            # The Excel has pre-calculated values based on base_investment
            # We need to scale it proportionally
            base_income = (
                float(row["Annual Lifetime Income"])
                if pd.notna(row["Annual Lifetime Income"])
                else 0
            )
            base_benefit = (
                float(row["Benefit Base"]) if pd.notna(row["Benefit Base"]) else 0
            )

            # Scale based on user's amount vs the base investment amount from Excel
            scale_factor = amount / base_investment if base_investment > 0 else 1
            scaled_income = base_income * scale_factor
            scaled_benefit = base_benefit * scale_factor

            result = {
                "sort": int(row["Sort"]) if pd.notna(row["Sort"]) else None,
                "annuity_type": str(row["Annuity Type"])
                if pd.notna(row["Annuity Type"])
                else "",
                "carrier": str(row["Carrier"]) if pd.notna(row["Carrier"]) else "",
                "rider_name": str(row["Rider Name"])
                if pd.notna(row["Rider Name"])
                else "",
                "withdrawal_rate": float(row["Withdrawal Rate"]) * 100
                if pd.notna(row["Withdrawal Rate"])
                else 0,
                "benefit_base": round(scaled_benefit, 2),
                "annual_lifetime_income": round(scaled_income, 2),
                "monthly_income": round(scaled_income / 12, 2),
            }
            results.append(result)

        # Sort by annual lifetime income descending
        results.sort(key=lambda x: x["annual_lifetime_income"], reverse=True)

        logger.info(f"Returning {len(results)} variable annuity products")
        return {
            "current_age": current_age,
            "withdrawal_age": withdrawal_age,
            "deferral_period": deferral_period,
            "investment_amount": amount,
            "products": results,
            "count": len(results),
        }
