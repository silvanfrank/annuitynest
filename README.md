# Annuity Nest MVP

A Flask-based web application for generating annuity quotes. This MVP captures user data through a form, processes it against Excel spreadsheets containing annuity rates, and displays personalized results.

## Features

- **Fixed Annuities**: Point-to-point investments paying interest over a duration - displays ALL columns and ALL rows from Excel
- **Variable Annuities**: Mutual fund-like investments - displays columns B, C, E, S (Annuity Type, Carrier, Rider Name, Lifetime Income) from the Excel Formatted sheet
- **Conditional Fields**: "Age of First Withdrawal" field appears only for Variable annuity type
- **Responsive Design**: Mobile-friendly form matching Elementor/Astra theme styling
- **iframe Ready**: Auto-resize messaging for WordPress embedding

## Excel Data Structure

### Fixed Annuity Rates.xlsx
- **Sheet**: FORMATTED 1 (calculated results sheet)
- **Output**: ALL columns (Sort, Company, Product, Years, Min Contribution, Min Rate, Base Rate, Bonus Rate, Yield to Surrender, Surrender Period, Future Value)
- **Rows**: ALL matching rows (not limited to top 10)
- **Filter**: Products where Min Contribution ≤ user's investment amount

### Variable Annuity Rates.xlsx
- **Sheet**: Formatted (web calculation sheet)
- **Output**: Columns B, C, E, S per instructions:
  - Column B (index 1): Annuity Type (e.g., "Variable")
  - Column C (index 2): Carrier (e.g., "Brighthouse", "Corebridge")
  - Column E (index 4): Rider Name (e.g., "FlexChoice Access - Level")
  - Column S (index 18): Annual Lifetime Income
- **Additional columns**: Withdrawal Rate, Benefit Base (for calculations)
- **Calculation**: Income values are scaled proportionally based on user's investment amount vs Excel's default $1,000,000

## Excel Data Flow & Updates

### 1. File Updates
The application loads Excel data **into memory at startup**.
- **If you update the Excel files**: You must **RESTART** the application for changes to take effect.
- **On a server**: Redeploy the application or restart the service.

### 2. Formulas vs. Values
The application reads **Values**, not formulas.
- **Formulas in Excel**: Are NOT executed by the Python application.
- **Calculations**: Are re-implemented in Python (`logic.py`) using the static rates read from Excel.

### 3. Consumed Data Points
The application strictly depends on the following columns. If these columns are moved or renamed, the application may break.

**Fixed Annuities (Sheet: "FORMATTED 1")**
- **Company Name** (Column B)
- **Product Name** (Column C)
- **Rate Term / Years** (Column D)
- **Minimum Contribution** (Column E)
- **Minimum Rate** (Column F)
- **Base Rate** (Column G)
- **Bonus Rate** (Column H)
- **Yield to Surrender** (Column I) - *Used for unexpected calculations*
- **Surrender Period** (Column J)

**Variable Annuities (Sheet: "Formatted")**
- **Annuity Type** (Column B) - *Must be "Variable"*
- **Carrier Name** (Column C)
- **Rider Name** (Column E)
- **Deferral Credit Rate** (Column F) - *Used for Benefit Base calculation*
- **Withdrawal Rate** (Column Q) - *Used for Income calculation*

### 4. Replicated Logic (Formulas)
The following Excel logic is hardcoded in Python (`logic.py`):

**Fixed Annuity Future Value**:
- Excel: `= Investment * (1 + Yield_To_Surrender)^10`
- Python: `User_Amount * ((1 + Yield_To_Surrender_Rate) ** 10)`
- *Note: This hardcodes the term to 10 years, matching the Excel formula*

**Variable Annuity Benefit Base**:
- Excel: `= Investment + (Investment * Deferral_Credit_Rate * Deferral_Period)`
- Python: `User_Amount + (User_Amount * Deferral_Credit_Rate * Deferral_Period)`
- *Note: This is Simple Interest, matching the Excel formula*

**Variable Annuity Annual Lifetime Income**:
- Excel: `= Benefit_Base * Withdrawal_Rate`
- Python: `Benefit_Base * Withdrawal_Rate`

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
cd annuitynest
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser to `http://localhost:5000`

## File Structure

```
annuitynest/
├── app.py                 # Flask application with routes
├── logic.py              # AnnuityCalculator class with business logic
├── data_processor.py     # Excel data cleaning and parsing
├── requirements.txt      # Python dependencies
├── test_implementation.py # Test script to verify implementation
├── templates/
│   └── index.html       # Main form (matches Elementor design)
├── static/
│   ├── style.css        # Astra theme matching styles (navy blue theme)
│   └── script.js        # Form handling and API calls
└── excel files/         # Excel data files
    ├── Fixed Annuity Rates.xlsx
    ├── Variable Annuity Rates.xlsx
    └── Guaranteed Income Calculator 1 26 26.xlsx
```

## API Endpoints

### GET `/`
Returns the main calculator form (HTML).

### GET `/health`
Health check endpoint.
```json
{
  "status": "healthy",
  "calculator_loaded": true
}
```

### POST `/api/calculate`
Calculate annuity quote.

**Request Body:**
```json
{
  "amount": 100000,
  "annuity_type": "variable",
  "current_age": 50,
  "withdrawal_age": 65
}
```

**Response (Variable):**
```json
{
  "type": "variable",
  "result": {
    "current_age": 50,
    "withdrawal_age": 65,
    "deferral_period": 15,
    "investment_amount": 100000,
    "count": 37,
    "products": [
      {
        "sort": 1,
        "annuity_type": "Variable",
        "carrier": "Brighthouse",
        "rider_name": "FlexChoice Access - Level",
        "withdrawal_rate": 6.4,
        "benefit_base": 162889.46,
        "annual_lifetime_income": 10424.93,
        "monthly_income": 868.74
      }
    ]
  }
}
```

**Response (Fixed):**
```json
{
  "type": "fixed",
  "results": [
    {
      "sort": 43,
      "company": "Delaware Life",
      "product": "Apex Control MYGA",
      "years": 7,
      "min_contribution": 100000,
      "min_rate": 0.25,
      "base_rate": 4.9,
      "bonus_rate": 0.0,
      "yield_to_surrender": 4.9,
      "surrender_period": 7,
      "future_value": 161344.77
    }
  ],
  "count": 6
}
```

## Form Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Name | text | No | Optional |
| Email | email | **Yes** | Required |
| Current Age | number | No | 18-100 |
| Type of Annuity | radio | No | Fixed, Fixed Indexed, Immediate, Variable |
| Phone Number | tel | No | Optional |
| Retirement Account | radio | No | IRA, Non-IRA |
| State of Residence | select | **Yes** | All 50 states + DC |
| Amount of Annuity | number | **Yes** | Minimum $50,000 |
| Age of First Withdrawal | number | Variable only | Min age 59, shown only when Variable selected |

## Implementation Details

### Fixed Annuity Calculation

Data is read from the "FORMATTED 1" sheet. All products are displayed (no filtering), and future values are calculated dynamically using the Excel formula.

**Displayed columns:**
- Sort: Product sort order
- Company: Insurance carrier name
- Product: Product name
- Years: Rate term in years
- Min Contribution: Minimum investment required
- Min Rate: Minimum interest rate
- Base Rate: Base interest rate
- Bonus Rate: Bonus interest rate (if any)
- Yield to Surrender: Yield to surrender percentage
- Surrender Period: Surrender charge period in years
- Future Value: Calculated future value after term

**Product Display:**
- All 170 products are shown (as per Excel instruction: "I would show all columns and all rows for output")
- No filtering by minimum contribution amount
- Sorted by Yield to Surrender (descending)

**Future Value Formula (from Excel):**
```
FV = Investment × (1 + Yield to Surrender/100)^10
```
Where:
- Investment = User's investment amount (replaces $C$3 in Excel)
- Yield to Surrender = Yield to surrender percentage from column I
- Years = Fixed at 10 years (as per Excel formula `=+$C$3*(1+(I10/100))^10`)

### Variable Annuity Calculation

Data is read from the "Formatted" sheet with specific columns. Values are calculated using the same formulas as the Excel file.

**Displayed columns (B, C, E, S):**
- Annuity Type (Column B): "Variable"
- Carrier (Column C): Insurance company name
- Rider Name (Column E): Product rider name
- Annual Lifetime Income (Column S): Calculated annual income

**Product Display:**
- All products displayed (no filtering)
- Sorted by Sort column (ascending) to match Excel order
- Shows columns B, C, E, and S as specified in Excel

**Calculated fields using Excel formulas:**
- **Benefit Base**: Calculated using deferral credit rate and deferral period
- **Withdrawal Rate**: Percentage from column Q
- **Annual Lifetime Income**: Benefit Base × Withdrawal Rate
- **Monthly Income**: Annual income ÷ 12

**Calculation Formulas (from Excel):**
```
Benefit Base = Investment + (Investment × Deferral Credit Rate × Deferral Period)
Annual Lifetime Income = Benefit Base × Withdrawal Rate
```

Where:
- Benefit Base uses **simple interest** (not compound): `=+$C$4+($C$4*F12*$C$5)`
- Deferral Credit Rate = Product-specific roll-up rate (e.g., 5%, 6%, 7%)
- Deferral Period = Withdrawal Age - Current Age
- Withdrawal Rate = Product-specific percentage (e.g., 6.15%)

## Testing

### Run Automated Tests

**Basic test suite:**
```bash
python3 test_implementation.py
```

This will verify:
- Fixed annuity data loading (all columns, all rows)
- Variable annuity data loading (columns B, C, E, S)
- Calculator functionality with sample data

**Calculation verification tests:**
```bash
python3 test_fixes.py
```

This will verify:
- Fixed annuity future value changes correctly with different investment amounts
- Variable annuity values match Excel file exactly
- Mathematical calculations are accurate

### Manual Testing via Browser

1. Start the application:
```bash
source .venv/bin/activate
python app.py
```

2. Open `http://localhost:5000` in your browser

3. Test **Variable Annuity**:
   - Select "Variable" as Annuity Type
   - Enter: Current Age: 55, Withdrawal Age: 65, Amount: $100,000
   - Fill in required fields (Email, State)
   - Click "Get my free quote"
   - **Expected**: Shows table with 37 products sorted by Annual Lifetime Income, with columns: Sort, Annuity Type, Carrier, Rider Name, Withdrawal Rate, Benefit Base, Annual Lifetime Income, Monthly Income

4. Test **Fixed Annuity**:
   - Select "Fixed" as Annuity Type
   - Enter: Amount: $100,000
   - Fill in required fields
   - Click "Get my free quote"
   - **Expected**: Returns table of all 11 columns sorted by Base Rate descending
   - **Verify Math**: Future Value should change when you use a different amount (e.g., $525,000 should give a proportionally higher future value)
   - Example: $100,000 at 4.9% for 7 years = $139,774.65
   - Example: $525,000 at 4.9% for 7 years = $733,816.92

5. Test **Conditional Field**:
   - Switch between "Fixed" and "Variable" types
   - **Expected**: "Age of First Withdrawal" field appears/disappears

6. Test **Validation**:
   - Try amount below $50,000
   - Try withdrawal age less than current age
   - **Expected**: Shows error messages

### API Testing with cURL

Test the health endpoint:
```bash
curl http://localhost:5000/health
```

Test Variable Annuity calculation:
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "annuity_type": "variable",
    "current_age": 55,
    "withdrawal_age": 65
  }'
```

Test Fixed Annuity calculation:
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "annuity_type": "fixed"
  }'
```

Test validation error (missing required field):
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 40000,
    "annuity_type": "fixed"
  }'
```

### Responsive Design Testing

1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl/Cmd + Shift + M)
3. Test at various widths:
   - Desktop: 1200px+
   - Tablet: 768px
   - Mobile: 375px
4. **Expected**: Form fields stack vertically on mobile, two-column on desktop

## WordPress Integration

Add to any WordPress page using Custom HTML block:

```html
<div class="annuity-calculator-wrapper">
  <iframe 
    id="annuity-calculator"
    src="https://your-flask-app.com" 
    width="100%" 
    height="800" 
    frameborder="0"
    scrolling="no"
    style="border: none;">
  </iframe>
</div>

<script>
  window.addEventListener('message', function(e) {
    if (e.origin !== 'https://your-flask-app.com') return;
    if (e.data.type === 'resize') {
      document.getElementById('annuity-calculator').style.height = e.data.height + 'px';
    }
  });
</script>
```

## Configuration

Environment variables (optional):
- `PORT`: Server port (default: 5000)
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: Set to `production` for production

## Data Processing

### Excel Sheet Selection

**Fixed Annuity Rates.xlsx:**
- Reads from "FORMATTED 1" sheet (not "ORIGINAL DATA")
- This sheet contains pre-calculated results with user inputs at top

**Variable Annuity Rates.xlsx:**
- Reads from "Formatted" sheet (not "Original")
- Extracts specific columns as requested (B, C, E, S)

### Data Validation

The implementation includes validation to ensure only valid data rows are processed:
- Fixed: Checks for valid company names, skips header rows
- Variable: Validates Annuity Type is "Variable", ensures carrier name is present

## License

Private - For Annuity Nest internal use.

## Original Task

**MVP** = Minimum Viable Product

Using https://annuitynest.com/custom-quote/ as a template, capture user data, feed the spreadsheet, and output information back to the website.

Distinguish between:
- **Fixed Annuity**: Point-to-point investments paying interest over time
- **Variable Annuity**: Mutual fund-like investments with annual withdrawals at user-defined starting point (0-20 years)

Variable annuities require **Current Age** and **Age of First Withdrawal** fields.
