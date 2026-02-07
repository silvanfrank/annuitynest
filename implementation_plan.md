# Annuity Nest MVP Implementation Plan

## Original Task Description

**MVP** = Minimum Viable Product

Using this page as a template https://annuitynest.com/custom-quote/ we need to capture user data, feed the spreadsheet and output the information back to the website.

We need to distinguish between a **Fixed Annuity** and a **Variable Annuity**. And for a Variable Annuity we need to ascertain a **Current Age** and **Age of First Withdrawal**. The Age of First Withdrawal is currently not on my site, so you'll need to build it in for this project.

**File Explanations**:
- **Fixed Annuity Rates** - point to point investments that pay interest over a certain amount of time
- **Variable Annuity Rates** - mutual fund like investments that pay annual withdrawals at a user defined starting point anywhere from immediately (0 years) up to 20 years. The annual withdrawals continue even if the investment performance does not sustain the withdrawal amounts and the account runs out of money.
- **Guaranteed Income Calculator 1 26 26** - our master file. Just good to have. I built Variable Annuity Rates from this as I did not know if you could properly extract info from it in its original state.

---

## Overview

**Goal**: Build a Minimum Viable Product (MVP) for an annuity quote generation tool that captures user data, processes it against Excel spreadsheets, and displays results.

**Key Requirements**:
- Form based on `annuitynest.com/custom-quote/` structure
- Support **Fixed** and **Variable** annuity types
- **Variable-specific fields**: Current Age + Age of First Withdrawal
- Data sources: `Fixed Annuity Rates.xlsx` and `Variable Annuity Rates.xlsx`
- Master logic reference: `Guaranteed Income Calculator 1 26 26.xlsx`

---

## Research Summary

### Current Website Structure

**Platform**: WordPress 6.9.1 + Astra Theme 4.12.3 + Elementor Pro 3.35.3

**Existing Form Fields** (8 fields):

| # | Field | Type | Required | Width | Notes |
|---|-------|------|----------|-------|-------|
| 1 | Name | text | No | 100% | |
| 2 | Email | email | **Yes** | 50% | |
| 3 | Current Age | number | No | 50% | |
| 4 | Type of Annuity | radio | No | 100% | Fixed, Fixed Indexed, Immediate, Variable |
| 5 | Phone Number | tel | No | 50% | |
| 6 | Retirement Account | radio | No | 50% | IRA, Non-IRA |
| 7 | State of Residence | select | **Yes** | 50% | 50 states + DC |
| 8 | Amount of Annuity | number | **Yes** | 50% | Min: $50,000 |

**Critical Gap**: Missing "Age of First Withdrawal" field required for Variable annuity calculations. This must be added as field #9.

---

## CRITICAL FINDINGS & IMPLEMENTATION DETAILS

### Fixed Annuity Data Structure

**Excel File**: `Fixed Annuity Rates.xlsx`

**Sheet to Use**: **FORMATTED 1** (not ORIGINAL DATA)
- This sheet contains pre-calculated results with user inputs at the top
- Data rows start at row 10 (index 9)

**Output Requirements**: 
> "I would show all columns and all rows for output"

**Columns (11 total)**:
1. Sort - Product sort order
2. Company - Insurance carrier name
3. Product - Product name
4. Years - Rate term in years
5. Min Contribution - Minimum investment required
6. Min Rate - Minimum interest rate
7. Base Rate - Base interest rate
8. Bonus Rate - Bonus interest rate (if any)
9. Yield to Surrender - Yield to surrender percentage
10. Surrender Period - Surrender charge period in years
11. Future Value - Calculated future value after term

**Filter Logic**: 
- Filter where `Min Contribution ≤ User Amount`
- Sort by `Base Rate` descending
- Return **ALL** matching rows (not limited to top 10)

---

### Variable Annuity Data Structure

**Excel File**: `Variable Annuity Rates.xlsx`

**Sheet to Use**: **Formatted** (not Original)
- This is the web calculation sheet with inputs at top
- Data rows start at row 11 (index 10), headers at row 10 (index 9)

**Output Requirements**: 
> "There are many hidden columns. I would only output B, C, E and S. This is the sheet to use for calculations. For now let's export all rows."

**Columns to Output**:
- **Column B** (index 1): Annuity Type (e.g., "Variable")
- **Column C** (index 2): Carrier (e.g., "Brighthouse", "Corebridge", "Delaware Life")
- **Column E** (index 4): Rider Name (e.g., "FlexChoice Access - Level")
- **Column S** (index 18): Annual Lifetime Income

**Additional Columns for Calculation**:
- Column 15: Benefit Base Amount
- Column 16: Withdrawal Rate

**Scaling Calculation**:
The Excel file calculates based on a default $1,000,000 investment. Must scale to user's actual investment:

```python
scale_factor = user_amount / 1000000.0
scaled_income = excel_income * scale_factor
scaled_benefit_base = excel_benefit_base * scale_factor
```

**Output**:
- Return **ALL** 37+ variable annuity products
- Sort by Annual Lifetime Income descending
- Display as table with columns: Sort, Annuity Type, Carrier, Rider Name, Withdrawal Rate, Benefit Base, Annual Lifetime Income, Monthly Income

---

## Technical Design

### Integration Approach

| Option | Approach | Best For |
|--------|----------|----------|
| **A** | Standalone Flask + iframe | **MVP** - Fastest to develop, isolated, easy updates |
| B | WordPress Plugin | Production - Native integration, longer timeline |
| C | API + Existing Form Mods | Post-MVP - Reuses current form, clean backend |
| D | Elementor HTML Widget | No iframe, design parity, CSS conflict risk |

**Recommendation**: Option A for MVP validation, then migrate to deeper integration.

### File Structure

```
annuitynest/
├── app.py                 # Flask app, routes, API
├── logic.py              # AnnuityCalculator class
├── data_processor.py     # Excel cleaning and parsing
├── requirements.txt      # Flask, pandas, openpyxl
├── test_implementation.py # Automated tests
├── templates/
│   └── index.html       # Main form (matches Elementor design)
├── static/
│   ├── style.css        # Navy blue theme matching annuitynest.com
│   └── script.js        # Form handling, API calls
└── excel files/
    ├── Fixed Annuity Rates.xlsx
    ├── Variable Annuity Rates.xlsx
    └── Guaranteed Income Calculator 1 26 26.xlsx
```

### Design Requirements

Match Elementor Pro form styling with navy blue theme:
- **Layout**: Two-column grid, responsive to single column at <768px
- **Field Order**: Name → Email/Current Age → Annuity Type → Phone/Retirement → State/Amount → [Variable only: Age of First Withdrawal] → Submit
- **Colors**: Primary navy blue `#1e3a5f`, input borders `#ced4da`, focus `#1e3a5f`
- **Typography**: Inherit from parent, 16px inputs (prevents mobile zoom)
- **Button**: Full width, "Get My Free Quote" uppercase with letter-spacing, navy blue background

**Responsive Table Layout**:
- Default container width: 600px (for form)
- When results displayed: Expand to 1400px max-width
- Tables have horizontal scroll on mobile
- Blue table headers (#1e3a5f background, white text)

---

## Implementation Phases

### Phase 1: MVP Core (Days 1-2)
- [x] Data cleaning scripts for Excel files
- [x] Read from correct sheets (FORMATTED 1 for Fixed, Formatted for Variable)
- [x] Implement column filtering (all for Fixed, B/C/E/S for Variable)
- [x] Implement scaling calculation for Variable annuities
- [x] Flask app with basic form (matching Elementor structure)
- [x] Fixed annuity filtering logic (all rows, all columns)
- [x] Variable annuity calculation from Excel data (not hardcoded)
- [x] Basic results display (table for both Fixed and Variable)
- [x] Form validation (client + server side)

### Phase 2: Integration Ready (Day 3)
- [x] CSS styling match with navy blue theme
- [x] Responsive design (mobile-first)
- [x] Wider container for table display
- [x] iframe embed code for WordPress
- [x] Error handling and loading states
- [ ] Deploy to hosting (PythonAnywhere/Heroku)

### Phase 3: Validation (Day 4)
- [ ] Test with real user scenarios
- [x] Verify calculations against Excel
- [ ] Cross-origin functionality test
- [ ] Stakeholder feedback and iteration

---

## WordPress Integration

Add to any WordPress page via Custom HTML block:

```html
<div class="annuity-calculator-wrapper">
  <iframe 
    id="annuity-calculator"
    src="https://your-flask-app.herokuapp.com" 
    width="100%" 
    height="800" 
    frameborder="0"
    scrolling="no"
    style="border: none;">
  </iframe>
</div>

<script>
  // Auto-resize iframe based on content height
  window.addEventListener('message', function(e) {
    if (e.origin !== 'https://your-flask-app.herokuapp.com') return;
    if (e.data.type === 'resize') {
      document.getElementById('annuity-calculator').style.height = e.data.height + 'px';
    }
  });
</script>
```

---

## Deployment

**Recommended**: PythonAnywhere (free tier available, easy Flask deployment)

**Environment Variables**:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5000
```

**Files to Deploy**:
```
excel files/Fixed Annuity Rates.xlsx
excel files/Variable Annuity Rates.xlsx
app.py
logic.py
data_processor.py
requirements.txt
templates/index.html
static/style.css
static/script.js
```

---

## API Response Examples

### Fixed Annuity Response

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

### Variable Annuity Response

```json
{
  "type": "variable",
  "result": {
    "current_age": 55,
    "withdrawal_age": 65,
    "deferral_period": 10,
    "investment_amount": 100000,
    "count": 37,
    "products": [
      {
        "sort": 51,
        "annuity_type": "Variable",
        "carrier": "Protective",
        "rider_name": "SecurePay Protector - Advance 3yr",
        "withdrawal_rate": 9.0,
        "benefit_base": 196715.14,
        "annual_lifetime_income": 17704.36,
        "monthly_income": 1475.36
      }
    ]
  }
}
```

---

## Testing

### Automated Tests

Run `python3 test_implementation.py` to verify:
- Fixed annuity data loading (all 11 columns)
- Variable annuity data loading (columns B, C, E, S)
- Proper Excel sheet selection
- Scaling calculations
- Filtering logic

### Manual Testing

1. **Fixed Annuity**:
   - Select "Fixed" type
   - Enter amount: $100,000
   - Submit
   - **Expected**: Table with 11 columns, sorted by Base Rate descending

2. **Variable Annuity**:
   - Select "Variable" type
   - Enter: Current Age 55, Withdrawal Age 65, Amount $100,000
   - Submit
   - **Expected**: Table with 37+ products, columns B/C/E/S + calculated fields
   - Container should expand to accommodate wide table

3. **Responsive**:
   - Test on mobile (375px width)
   - Tables should scroll horizontally
   - Form should stack vertically

---

## Future Enhancements (Post-MVP)

1. **State filtering** - Filter products by state availability (requires data enhancement)
2. **Lead integration** - Connect to existing Elementor form submissions
3. **PDF generation** - Save/print quotes as PDF
4. **Admin interface** - Upload and manage Excel files without server access
5. **Analytics** - Track form completions and quote views
6. **Email notifications** - Send quotes to users via email

---

## Success Criteria

**MVP is successful if**:
- [x] Users can complete the form and see results
- [x] Fixed Annuity results show ALL columns and ALL matching rows
- [x] Variable Annuity shows products with columns B, C, E, S from Excel
- [x] Variable calculations properly scale from Excel's $1M default
- [x] Form visually matches existing site design (navy blue theme)
- [x] Page loads in under 3 seconds
- [x] Works on desktop and mobile devices
- [x] Can be embedded in WordPress via iframe
- [x] Container expands to show wide tables properly

**Not required for MVP**:
- State-specific product filtering
- Lead capture integration with existing system
- PDF generation
- User accounts or saved quotes
- Email notifications
