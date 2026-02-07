# Annuity Nest MVP Implementation Plan

## Original Task Description
**Goal**: Create a Minimum Viable Product (MVP) for an annuity quote generation tool. This involves capturing user data on a webpage, feeding it into a spreadsheet, and then displaying the relevant annuity information back to the user.

**Key Requirements**:
1.  **Template**: Use [annuitynest.com/custom-quote/](https://annuitynest.com/custom-quote/) as a reference for the form.
2.  **Product Types**:
    *   **Fixed Annuities**: Point-to-point investments paying interest over a duration.
    *   **Variable Annuities**: Mutual-fund-like investments paying annual withdrawals.
3.  **Data Capture**:
    *   Standard form fields (Amount, State, etc.)
    *   **Variable Specific**: Must capture **Current Age** and **Age of First Withdrawal**.
        *   *Note*: "Age of First Withdrawal" is a new field not currently on the live site.
4.  **Logic**:
    *   **Fixed**: Use `Fixed Annuity Rates.xlsx`.
    *   **Variable**: Use `Variable Annuity Rates.xlsx`. Retrieve withdrawal % based on age/deferral period.
    *   *Reference*: `Guaranteed Income Calculator 1 26 26.xlsx` is the master file (logic source).

**MVP Definition**: PROVE THE CONCEPT. It doesn't need to be perfect, but it must functional: Input -> Process -> Output.

This plan outlines the steps to build the Minimum Viable Product (MVP) for the Annuity Nest custom quote calculator.

---

## Research Findings & Analysis

### 1. Current Website Analysis

**Platform Stack**:
- WordPress 6.9.1 with Astra Theme 4.12.3
- Elementor Pro 3.35.3 (page builder)
- Existing form at `/custom-quote/` uses Elementor Pro Form widget

**Current Form Fields (8 total)**:
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Name | text | No | |
| Email | email | **Yes** | |
| Current Age | number | No | |
| Type of Annuity | radio | No | Options: Fixed, Fixed Indexed, Immediate, Variable |
| Phone Number | number | No | |
| Retirement Account | radio | No | Options: IRA, Non-IRA |
| State of Residence | select | **Yes** | All 50 states + DC |
| Amount of Annuity | number | **Yes** | Min: $50,000 |

**Critical Gap Identified**: The current form has "Variable" as an option but lacks the **"Age of First Withdrawal"** field required for variable annuity calculations.

**Form Submission**: Uses Elementor Pro's built-in AJAX handler to `wp-admin/admin-ajax.php` - appears to be a lead capture form only (no real-time calculations).

### 2. Data Structure Analysis

#### Fixed Annuity Rates (`Fixed Annuity Rates.xlsx`)
- **Rows**: 348 products across multiple carriers
- **Key Columns**: Company Name, Product Name, Product Type, Premium Type, Rate Term, Min. Contrib., Min. Rate, Base Rate, Bonus Rate, Yield to Surr., Surrender Period
- **Data Quality Issues**: 
  - Header row has offset (actual data starts at row 2)
  - Company names appear on separate rows from product details
  - Missing values in several columns (NaN values present)
  - Rate Term values need parsing (mix of numbers and strings)

**MVP Logic**: Filter by Min. Contrib. ≤ User Amount, sort by Base Rate descending

#### Variable Annuity Rates (`Variable Annuity Rates.xlsx` + `Guaranteed Income Calculator`)
- **Complex Structure**: Multiple carriers with different rider types
- **Key Calculation Factors**:
  - Current Age (at issue)
  - Age at First Withdrawal
  - Initial Investment Amount
  - Deferral Period = Withdrawal Age - Current Age
  - Withdrawal % varies by carrier and age

**Withdrawal Rate Tables Found**:
- `single life agebands` sheet contains age-based lookup tables
- Example: Lincoln ProtectedPay Secure Core - rates range from 4.75% (age 59) to 6.9% (age 80+)
- Different carriers use different calculation methods (Simple Interest, Compound Interest, Stackable vs Greater Of)

**MVP Simplification**: For MVP, use a simplified average withdrawal rate based on age brackets rather than carrier-specific calculations.

### 3. Integration Strategy

**Option A: Standalone MVP** (Recommended for initial proof-of-concept)
- Build separate Flask application
- Embed via iframe on existing WordPress page
- Pros: Fastest to develop, isolated from existing site issues
- Cons: Separate hosting, iframe limitations

**Option B: WordPress Plugin**
- Create custom WordPress plugin
- Hook into existing Elementor form
- Pros: Native integration, uses existing styling
- Cons: Requires PHP/WordPress expertise, longer development time

**Option C: API Integration**
- Flask backend as API service
- Modify existing Elementor form to call API via JavaScript
- Pros: Reuses existing form, clean separation
- Cons: Requires editing Elementor form custom code

**Recommendation**: Start with **Option A** for MVP validation, then migrate to Option C for production.

### 4. Technical Requirements

**Dependencies**:
```
Flask==3.x
pandas==2.x
openpyxl==3.x
numpy==2.x
```

**Data Processing Needs**:
1. **Fixed Annuity Data Cleaning**:
   - Handle missing company names (forward-fill from previous row)
   - Parse Rate Term strings to numeric values
   - Convert currency columns to numeric
   
2. **Variable Annuity Logic**:
   - Create simplified withdrawal rate lookup table
   - Calculate deferral period: `deferral = withdrawal_age - current_age`
   - Formula: `Annual Income = Amount × Withdrawal Rate`
   - Annual Income = Amount × Withdrawal Rate

### 5. User Experience Considerations

**Form Flow**:
1. User selects Annuity Type first (Fixed/Variable)
2. Conditional display:
   - Fixed: Show standard fields only
   - Variable: Show additional "Age of First Withdrawal" field
3. Real-time validation (client-side):
   - Minimum amount: $50,000
   - Age validation: Current Age < Withdrawal Age
   - Withdrawal age minimum: 59.5

**Results Display**:
- **Fixed Annuities**: Table with columns - Company, Product, Rate, Term, Min Investment
- **Variable Annuities**: Single result card showing - Projected Annual Income, Withdrawal Rate %, Deferral Period

### 6. Styling Requirements

**Visual Match**:
- Use Astra theme color palette (blues: #0055ff, #007bff)
- Match Elementor form styling (rounded inputs, label-above layout)
- Responsive: 50/50 columns on desktop, stacked on mobile
- Typography: System fonts matching Astra (inherit from parent when iframe embedded)

---

# Goal Description
Create a web-based MVP that captures user data, processes it against provided Excel spreadsheets ("Fixed Annuity Rates" and "Variable Annuity Rates"), and displays the results to the user. The application will be a simple full-stack app (Python/Flask + HTML/JS) to demonstrate the concept.

## Implementation Phases

### Phase 1: MVP Core (Proof of Concept)
**Goal**: Functional Input -> Process -> Output

**Deliverables**:
- [ ] Data cleaning scripts for Excel files
- [ ] Flask app with basic form
- [ ] Fixed annuity filtering logic
- [ ] Variable annuity simplified calculation
- [ ] Basic results display

**Timeline**: 1-2 days

### Phase 2: Integration Ready
**Goal**: Production-ready for WordPress embedding

**Deliverables**:
- [ ] iframe embed code for WordPress
- [ ] Styling match with Astra theme
- [ ] Responsive design
- [ ] Error handling and validation
- [ ] Loading states

**Timeline**: 1 day

### Phase 3: Enhanced Features (Post-MVP)
**Goal**: Full-featured calculator

**Deliverables**:
- [ ] Carrier-specific variable annuity calculations
- [ ] State-specific filtering
- [ ] PDF quote generation
- [ ] Lead capture integration
- [ ] Analytics tracking

**Timeline**: 1-2 weeks (future work)

---

## User Review Required
> [!IMPORTANT]
> **Variable Annuity Logic Confirmed**: The data shows complex carrier-specific calculations with age-based withdrawal rate tables. For MVP, I recommend using a simplified average rate model. The detailed carrier logic can be implemented in Phase 3.

> [!NOTE]
> **Integration Approach**: The MVP will be a standalone Flask app designed for iframe embedding on the existing WordPress site. This provides the fastest path to validation while maintaining the ability to integrate more deeply later.

> [!WARNING]
> **Data Quality**: The Excel files require cleaning - missing company names need forward-filling, and rate term parsing is inconsistent. A data preprocessing step is required before calculations.

## Proposed Changes

### Backend (Python/Flask)
I will create a simple Flask application to serve the frontend and handle the calculation logic.

#### [NEW] [app.py](file:///Users/silvanfrank/Github/annuitynest/app.py)
- **Framework**: Flask with CORS support for iframe embedding
- **Routes**:
    - `/`: Serves the main form.
    - `/api/calculate`: POST endpoint to receive user data and return annuity options.
    - `/health`: Health check endpoint for monitoring.
- **Configuration**:
    - Load Excel files once at startup (singleton pattern)
    - Cache cleaned data in memory for performance
- **Logic**:
    - **Fixed Annuity Handler**: 
      - Clean data: forward-fill company names, parse rate terms
      - Filter: `Min. Contrib. <= User Amount`
      - Sort: by `Base Rate` descending
      - Return: Top 10 results with columns [Company, Product, Base Rate, Term, Min Investment]
    - **Variable Annuity Handler**: 
      - Calculate deferral period: `withdrawal_age - current_age`
      - Lookup withdrawal rate from simplified age-based table
      - Calculate: `Annual Income = Amount × Withdrawal Rate`
      - Return: Annual income, monthly income, withdrawal rate %, deferral years

#### [NEW] [data_processor.py](file:///Users/silvanfrank/Github/annuitynest/data_processor.py)
- **Purpose**: Clean and normalize Excel data for calculations
- **Functions**:
    - `clean_fixed_annuity_data(df)`: Handle missing company names, standardize columns
    - `parse_rate_term(term)`: Convert string terms ("10 Year") to numeric
    - `create_variable_lookup_table()`: Build simplified withdrawal rate dictionary by age
- **Caching**: Store cleaned DataFrames in module-level variables

#### [NEW] [logic.py](file:///Users/silvanfrank/Github/annuitynest/logic.py)
- Encapsulate the calculation logic here to keep `app.py` clean.
- `AnnuityCalculator` class:
    - `__init__()`: Load and cache cleaned data
    - `get_fixed_rates(amount, state=None)`: Returns filtered fixed annuity rates (top 10)
    - `get_variable_income(current_age, withdrawal_age, amount)`: Returns projected guaranteed income
    - `validate_input(data)`: Returns validation errors or None
- **Variable Rate Simplification**:
  ```python
  # Simplified withdrawal rates by age (averaged from carrier data)
  WITHDRAWAL_RATES = {
      59: 0.0475, 60: 0.0475, 61: 0.0475, 62: 0.0475, 63: 0.0475,
      64: 0.0475, 65: 0.0635, 66: 0.0635, 67: 0.0635, 68: 0.0635,
      69: 0.0635, 70: 0.0655, 71: 0.0655, 72: 0.0655, 73: 0.0655,
      74: 0.0655, 75: 0.0675, 76: 0.0675, 77: 0.0675, 78: 0.0675,
      79: 0.0675, 80: 0.0690, 81+: 0.0690
  }
  ```

### Frontend (HTML/CSS/JS)
I will recreate the form from `annuitynest.com/custom-quote/` matching the Elementor Pro form structure.

#### [NEW] [templates/index.html](file:///Users/silvanfrank/Github/annuitynest/templates/index.html)
- **Layout**: Two-column responsive grid (50%/50%) matching Elementor
- **Form Structure** (9 fields total):
    1. **Name** (text, 100% width, optional) - placeholder: "Name"
    2. **Email** (email, 50% width, required) - placeholder: "Email"
    3. **Current Age** (number, 50% width, optional) - min: 35, max: 85
    4. **Phone Number** (tel, 50% width, optional) - placeholder: "Phone"
    5. **State of Residence** (select, 50% width, required) - All 50 states + DC
    6. **Retirement Account** (radio, 50% width, optional) - Options: IRA, Non-IRA
    7. **Amount of Annuity** (number, 50% width, required) - min: 50000, placeholder: "Minimum of $50,000"
    8. **Type of Annuity** (radio, 100% width, optional) - Options: Fixed, Variable
        - **Conditional**: When "Variable" selected, show field 9
    9. **Age of First Withdrawal** (number, 50% width, conditional) - min: 59, max: 85
- **Submit Button**: "Get my free quote" - full width, blue background
- **Results Container**: Empty div below form for dynamic results insertion

#### [NEW] [static/script.js](file:///Users/silvanfrank/Github/annuitynest/static/script.js)
- **Event Listeners**:
    - Form submit: Prevent default, validate, submit via fetch API
    - Annuity type change: Toggle visibility of "Age of First Withdrawal" field
    - Input validation: Real-time validation with visual feedback
- **API Call**:
  ```javascript
  fetch('/api/calculate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(formData)
  })
  ```
- **Results Rendering**:
    - **Fixed Results**: HTML table with columns [Company, Product, Rate, Term, Min Investment]
    - **Variable Results**: Card layout showing [Annual Income, Monthly Income, Withdrawal Rate, Deferral Period]
- **Error Handling**: Display user-friendly error messages for validation failures or API errors
- **Loading State**: Show spinner during API call

#### [NEW] [static/style.css](file:///Users/silvanfrank/Github/annuitynest/static/style.css)
- **Container**: Max-width 800px, centered, white background
- **Form Layout**:
    - Two-column grid using CSS Grid (repeat(2, 1fr))
    - Gap: 20px
    - 100% width fields span both columns
- **Inputs**:
    - Border: 1px solid #ddd
    - Border-radius: 4px (matching Elementor)
    - Padding: 12px 16px
    - Font-size: 16px
- **Labels**: Above inputs, font-weight: 500, margin-bottom: 8px
- **Radio Groups**: Inline display with proper spacing
- **Button**:
    - Background: #0055ff (Astra primary blue)
    - Color: white
    - Border-radius: 4px
    - Padding: 15px 30px
    - Hover: darken 10%
- **Results Table**:
    - Striped rows
    - Header: background #f5f5f5
    - Hover: background #e8f4fd
- **Responsive**:
    - Mobile (<768px): Single column layout
    - Maintain readability on small screens
- **iframe Optimization**:
    - No external dependencies (all styles inline)
    - Minimal CSS reset to avoid conflicts
    - Auto-height adjustment script for parent page

## Verification Plan

### Automated Tests
Create `test_logic.py` using pytest:

**Test Cases**:
1. **Data Loading Tests**:
   - Test that Fixed Annuity Rates loads without errors
   - Test that all required columns are present
   - Test data cleaning (company name forward-fill)

2. **Fixed Annuity Logic Tests**:
   - Test filtering: $100k amount should exclude products with Min. Contrib. > 100k
   - Test sorting: Results sorted by Base Rate descending
   - Test state filtering (if implemented)
   - Edge case: Amount exactly equals minimum contribution

3. **Variable Annuity Logic Tests**:
   - Test deferral calculation: Age 55 -> 65 = 10 year deferral
   - Test withdrawal rate lookup: Age 65 should return ~6.35%
   - Test income calculation: $100k × 6.35% = $6,350/year
   - Test age validation: Withdrawal age must be > current age
   - Test minimum withdrawal age: 59.5 validation

4. **API Endpoint Tests**:
   - Test `/api/calculate` with valid fixed annuity data
   - Test `/api/calculate` with valid variable annuity data
   - Test error handling for invalid input
   - Test response format (JSON structure)

### Manual Verification

**Setup**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

**Test Scenarios**:

1. **Fixed Annuity - Basic Test**:
   - Navigate to `http://localhost:5000`
   - Enter: Age: 60, Amount: $100,000, State: California
   - Select: Annuity Type = Fixed
   - Submit
   - **Expected**: Table with 5-10 products, all with Min. Contrib. ≤ $100k, sorted by highest rate first

2. **Fixed Annuity - High Amount Test**:
   - Amount: $500,000
   - **Expected**: More product options including those with higher minimums

3. **Variable Annuity - Young Client**:
   - Current Age: 45, Withdrawal Age: 65, Amount: $200,000
   - **Expected**: Deferral = 20 years, Rate ~6.35%, Annual Income ~$12,700

4. **Variable Annuity - Near Retirement**:
   - Current Age: 60, Withdrawal Age: 65, Amount: $300,000
   - **Expected**: Deferral = 5 years, Rate ~6.35%, Annual Income ~$19,050

5. **Validation Tests**:
   - Amount: $40,000 (below minimum) → Should show validation error
   - Withdrawal Age: 55 (below 59.5) → Should show validation error
   - Withdrawal Age: 60, Current Age: 65 → Should show error (withdrawal must be in future)

6. **Responsive Design Test**:
   - Resize browser to mobile width (375px)
   - **Expected**: Form fields stack vertically, readable on small screen

7. **iframe Embedding Test**:
   - Create test HTML page with iframe pointing to `http://localhost:5000`
   - **Expected**: Form displays correctly, no scrollbars, styling isolated

### Integration Verification

**WordPress Embedding**:
1. Create new page in WordPress
2. Add HTML block with iframe code:
   ```html
   <iframe src="http://localhost:5000" width="100%" height="800" frameborder="0"></iframe>
   ```
3. Preview page
4. **Expected**: Form matches existing site styling, functions correctly

**Cross-Origin Test**:
- Test from different origin (if deployed)
- **Expected**: CORS headers allow embedding, form submits successfully

---

## WordPress Integration Guide

### Option 1: iframe Embed (Recommended for MVP)

Add this code to any WordPress page using the "Custom HTML" block:

```html
<div class="annuity-calculator-wrapper">
  <iframe 
    id="annuity-calculator"
    src="https://your-flask-app.com" 
    width="100%" 
    height="700" 
    frameborder="0"
    scrolling="no"
    style="border: none; overflow: hidden;">
  </iframe>
</div>

<script>
  // Auto-resize iframe based on content
  window.addEventListener('message', function(e) {
    if (e.origin !== 'https://your-flask-app.com') return;
    if (e.data.type === 'resize') {
      document.getElementById('annuity-calculator').style.height = e.data.height + 'px';
    }
  });
</script>
```

### Option 2: WordPress Shortcode Plugin

Create a simple plugin for easier embedding:

**File**: `wp-content/plugins/annuity-calculator/annuity-calculator.php`

```php
<?php
/**
 * Plugin Name: Annuity Calculator Embed
 * Description: Embeds the Annuity Nest calculator
 * Version: 1.0
 */

function annuity_calculator_shortcode($atts) {
    $atts = shortcode_atts(array(
        'height' => '700',
    ), $atts);
    
    return '<iframe src="https://your-flask-app.com" width="100%" height="' . esc_attr($atts['height']) . '" frameborder="0" scrolling="no"></iframe>';
}
add_shortcode('annuity_calculator', 'annuity_calculator_shortcode');
```

**Usage**: `[annuity_calculator height="800"]`

---

## Deployment Options

### Option A: PythonAnywhere (Recommended for MVP)
- Free tier available
- Easy Flask deployment
- Built-in MySQL if needed later
- Steps:
  1. Upload files via Git or SFTP
  2. Configure WSGI file
  3. Set virtual environment
  4. Install requirements

### Option B: Heroku
- Free tier (with limitations)
- Git-based deployment
- Good for prototyping

### Option C: VPS/Dedicated Server
- Full control
- Better for production
- Requires server management

### Environment Variables Required:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
EXCEL_FILES_PATH=/path/to/excel/files
```

---

## Future Enhancements (Post-MVP)

### Phase 3 Features:
1. **Advanced Variable Annuity Logic**:
   - Carrier-specific calculations
   - Multiple rider options per carrier
   - Joint life calculations
   - Fee impact modeling

2. **Lead Integration**:
   - Connect to existing Elementor form submissions
   - Save quotes to database
   - Email notifications to agents

3. **User Experience**:
   - Save/print quote as PDF
   - Compare multiple scenarios
   - Interactive charts
   - Mobile app

4. **Data Management**:
   - Admin panel for updating rates
   - Automated Excel import
   - Rate change notifications

5. **Compliance**:
   - Disclaimer text
   - Terms acceptance
   - Audit logging

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Excel data format changes | High | Create data validation layer, version control data files |
| iframe blocked by security | Medium | Provide direct link fallback, implement CORS properly |
| Performance with large data | Low | Cache cleaned data, implement pagination |
| Browser compatibility | Low | Test on major browsers, use polyfills if needed |
| WordPress theme conflicts | Medium | Use highly specific CSS selectors, test in staging |
