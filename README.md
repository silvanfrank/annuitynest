# Annuity Nest MVP

A Flask-based web application for generating annuity quotes. This MVP captures user data through a form, processes it against Excel spreadsheets containing annuity rates, and displays personalized results.

## Features

- **Fixed Annuities**: Point-to-point investments paying interest over a duration
- **Variable Annuities**: Mutual fund-like investments with annual withdrawals based on age
- **Conditional Fields**: "Age of First Withdrawal" field appears only for Variable annuity type
- **Responsive Design**: Mobile-friendly form matching Elementor/Astra theme styling
- **iframe Ready**: Auto-resize messaging for WordPress embedding

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
├── templates/
│   └── index.html       # Main form (matches Elementor design)
├── static/
│   ├── style.css        # Astra theme matching styles
│   └── script.js        # Form handling and API calls
└── excel files/         # Excel data files
    ├── Fixed Annuity Rates.xlsx
    └── Variable Annuity Rates.xlsx
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
    "withdrawal_rate": 6.35,
    "annual_income": 6350.0,
    "monthly_income": 529.17,
    "disclaimer": "Rates are estimates based on average market rates..."
  }
}
```

**Response (Fixed):**
```json
{
  "type": "fixed",
  "results": [
    {
      "company": "Integrity Life Insurance",
      "product": "New Momentum II",
      "base_rate": 3.55,
      "rate_term": 10,
      "min_contribution": 50000
    }
  ],
  "count": 10
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

## Variable Annuity Calculation

Withdrawal rates by age (simplified averages):
- Age 59-64: 4.75%
- Age 65-69: 6.35%
- Age 70-74: 6.55%
- Age 75-79: 6.75%
- Age 80+: 6.90%

Formula: `Annual Income = Investment Amount × Withdrawal Rate`

## Testing

### Manual Testing via Browser

1. Start the application:
```bash
source .venv/bin/activate
python app.py
```

2. Open `http://localhost:5000` in your browser

3. Test **Variable Annuity**:
   - Select "Variable" as Annuity Type
   - Enter: Current Age: 50, Withdrawal Age: 65, Amount: $100,000
   - Fill in required fields (Email, State)
   - Click "Get my free quote"
   - **Expected**: Shows Annual Income ~$6,350 with 6.35% withdrawal rate

4. Test **Fixed Annuity**:
   - Select "Fixed" as Annuity Type
   - Enter: Amount: $100,000
   - Fill in required fields
   - Click "Get my free quote"
   - **Expected**: Returns table of fixed annuity products

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
    "current_age": 50,
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

## Known Issues

- Fixed annuity data parsing needs adjustment for the two-row Excel format
- Currently returns 0 products for fixed annuities

## License

Private - For Annuity Nest internal use.

## Original Task

**MVP** = Minimum Viable Product

Using https://annuitynest.com/custom-quote/ as a template, capture user data, feed the spreadsheet, and output information back to the website.

Distinguish between:
- **Fixed Annuity**: Point-to-point investments paying interest over time
- **Variable Annuity**: Mutual fund-like investments with annual withdrawals at user-defined starting point (0-20 years)

Variable annuities require **Current Age** and **Age of First Withdrawal** fields.
