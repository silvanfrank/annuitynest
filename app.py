from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
from logic import AnnuityCalculator

app = Flask(__name__)
CORS(app, origins="*")

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

calculator = None

EXCEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "excel files")


def init_calculator():
    global calculator
    logger.info("Starting init_calculator...")
    try:
        fixed_path = os.path.join(EXCEL_DIR, "Fixed Annuity Rates.xlsx")
        variable_path = os.path.join(EXCEL_DIR, "Variable Annuity Rates.xlsx")

        if not os.path.exists(fixed_path):
            logger.error(f"Fixed Annuity Rates file not found: {fixed_path}")
            return False
        if not os.path.exists(variable_path):
            logger.error(f"Variable Annuity Rates file not found: {variable_path}")
            return False

        logger.info(f"Loading Excel files from: {EXCEL_DIR}")
        calculator = AnnuityCalculator(fixed_path, variable_path)
        logger.info("AnnuityCalculator initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize calculator: {str(e)}", exc_info=True)
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    status = "healthy" if calculator is not None else "unhealthy"
    logger.info(f"Health check requested. Status: {status}")
    return jsonify({"status": status, "calculator_loaded": calculator is not None})


@app.route("/api/calculate", methods=["POST"])
def calculate():
    if calculator is None:
        return jsonify(
            {
                "error": "Calculator not initialized",
                "details": "Excel files could not be loaded",
            }
        ), 500

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        validation_errors = calculator.validate_input(data)
        if validation_errors:
            return jsonify(
                {"error": "Validation failed", "details": validation_errors}
            ), 400

        annuity_type = data.get("annuity_type", "").lower()
        amount = float(data.get("amount", 0))

        if annuity_type in ["fixed", "fixed indexed", "immediate"]:
            results = calculator.get_fixed_rates(amount)
            return jsonify({"type": "fixed", "results": results, "count": len(results)})

        elif annuity_type == "variable":
            current_age = int(data.get("current_age", 0))
            withdrawal_age = int(data.get("withdrawal_age", 0))

            result = calculator.get_variable_income(
                current_age=current_age, withdrawal_age=withdrawal_age, amount=amount
            )
            return jsonify({"type": "variable", "result": result})

        else:
            return jsonify(
                {
                    "error": "Invalid annuity type",
                    "details": f"Type '{annuity_type}' not recognized",
                }
            ), 400

    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return jsonify({"error": "Calculation failed", "details": str(e)}), 500



# Initialize calculator on module load for production servers (Gunicorn)
init_calculator()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
