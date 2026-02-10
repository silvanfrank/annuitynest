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

    def calculate_fixed_future_value(self, amount, yield_to_surrender):
        """
        Calculate future value using compound interest formula.
        Formula from Excel: =+$C$3*(1+(I10/100))^10
        Note: Excel hardcodes 10 years for all products
        Where:
        - $C$3 = Investment amount (user input)
        - I10 = Yield to Surrender rate (column I)
        - Years = Fixed at 10 (as per Excel formula)
        """
        if yield_to_surrender is None or yield_to_surrender <= 0:
            return amount
        rate_decimal = yield_to_surrender / 100.0
        future_value = amount * ((1 + rate_decimal) ** 10)  # Excel uses 10 years
        return round(future_value, 2)

    def get_fixed_rates(self, amount, state=None):
        """
        Return all fixed annuity products with all columns.
        Show all rows from Excel (no filtering by minimum contribution).
        Calculate future value based on user's investment amount.
        """
        if self.fixed_data is None:
            logger.error("Fixed annuity data not loaded")
            return []

        # Show all products - no filtering (as per Excel "I would show all columns and all rows for output")
        filtered = self.fixed_data.copy()

        # Sort by Base Rate descending
        filtered = filtered.sort_values("Base Rate", ascending=False)

        # Convert to list of dicts with all columns
        results = []
        for _, row in filtered.iterrows():
            years = int(row["Years"]) if pd.notna(row["Years"]) else None
            base_rate = float(row["Base Rate"]) if pd.notna(row["Base Rate"]) else 0
            yield_to_surrender = (
                float(row["Yield to Surrender"])
                if pd.notna(row["Yield to Surrender"])
                else 0
            )

            # Calculate future value based on user's actual investment amount
            # Using Yield to Surrender rate and 10 years (as per Excel formula)
            future_value = self.calculate_fixed_future_value(amount, yield_to_surrender)

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
        Calculate Benefit Base and Annual Lifetime Income using Excel formulas:
        - Benefit Base = Investment × (1 + Deferral Credit Rate)^Deferral Period
        - Annual Lifetime Income = Benefit Base × Withdrawal Rate
        """
        if self.variable_data is None:
            logger.error("Variable annuity data not loaded")
            return []

        deferral_period = withdrawal_age - current_age

        if deferral_period <= 0:
            logger.error(f"Invalid deferral period: {deferral_period}")
            return []

        logger.info(
            f"Calculating variable annuity for ${amount:,.2f}, {deferral_period} year deferral period"
        )

        # Return all variable annuity products with calculated values
        results = []
        for _, row in self.variable_data.iterrows():
            # Get the deferral credit rate and withdrawal rate
            deferral_credit_rate = (
                float(row["Deferral Credit"]) if pd.notna(row["Deferral Credit"]) else 0
            )
            withdrawal_rate = (
                float(row["Withdrawal Rate"]) if pd.notna(row["Withdrawal Rate"]) else 0
            )

            # Calculate Benefit Base using formula: Investment × (1 + Deferral Credit Rate)^Deferral Period
            # Note: Deferral Credit Rate is stored as decimal (e.g., 0.05 for 5%)
            if deferral_credit_rate > 0:
                benefit_base = amount * ((1 + deferral_credit_rate) ** deferral_period)
            else:
                benefit_base = amount

            # Calculate Annual Lifetime Income: Benefit Base × Withdrawal Rate
            # Note: Withdrawal Rate is stored as decimal (e.g., 0.064 for 6.4%)
            annual_lifetime_income = benefit_base * withdrawal_rate

            result = {
                "sort": int(row["Sort"]) if pd.notna(row["Sort"]) else None,
                "annuity_type": str(row["Annuity Type"])
                if pd.notna(row["Annuity Type"])
                else "",
                "carrier": str(row["Carrier"]) if pd.notna(row["Carrier"]) else "",
                "rider_name": str(row["Rider Name"])
                if pd.notna(row["Rider Name"])
                else "",
                "withdrawal_rate": withdrawal_rate
                * 100,  # Convert to percentage for display
                "benefit_base": round(benefit_base, 2),
                "annual_lifetime_income": round(annual_lifetime_income, 2),
                "monthly_income": round(annual_lifetime_income / 12, 2),
            }
            results.append(result)

        # Sort by Sort column (ascending) to match Excel order
        results.sort(key=lambda x: x["sort"] if x["sort"] is not None else float("inf"))

        logger.info(f"Returning {len(results)} variable annuity products")
        return {
            "current_age": current_age,
            "withdrawal_age": withdrawal_age,
            "deferral_period": deferral_period,
            "investment_amount": amount,
            "products": results,
            "count": len(results),
        }
