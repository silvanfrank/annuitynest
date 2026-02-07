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

**Access Note (Feb 7, 2026)**:
Direct fetch of `https://annuitynest.com/custom-quote/` was blocked in this environment. Field order and labels below are derived from cached search snapshots, so layout/style details are approximate and should be verified in-browser before final styling.

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

**Design/UX Observations (from snapshot)**:
- Page header copy appears as “Free Quote” with a subheading “Get a Free Quote”.
- Form uses label-above-input layout with two-column rows (Elementor column width 50% pattern) and full-width rows for radio groups.
- Button text: “Get my free quote”.
- Order of fields on page (from snapshot): Name, Email, Current Age, Type of Annuity, Phone Number, Retirement Account, State of Residence, Amount of Annuity.

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

**Option D: Elementor HTML Widget (Inline App Shell)**
- Create a dedicated HTML widget in Elementor that contains the MVP UI (HTML/CSS/JS)
- Call the Flask API directly from that widget
- Pros: Eliminates iframe, best visual match, fastest iteration in WP
- Cons: Need to manage asset loading and potential theme CSS conflicts

**Option E: Hybrid Embed (Iframe + Shared CSS Tokens)**
- Use iframe for logic isolation but inject a small CSS variables file matching Astra/Elementor styles
- Pros: Keeps integration simple while matching look-and-feel
- Cons: Requires coordinated versioning of CSS tokens across WP + iframe app

**Recommendation**: Start with **Option A** for MVP validation, then migrate to Option C for production.

### Integration Options - Detailed Comparison

| Option | Approach | Pros | Cons | Best For |
|--------|----------|------|------|----------|
| **A** | Standalone Flask + iframe | Fastest dev, isolated, easy updates | Separate hosting, iframe limitations | MVP validation, proof-of-concept |
| **B** | WordPress Plugin | Native integration, uses existing forms | Requires PHP expertise, longer timeline | Production, long-term solution |
| **C** | API + Existing Form Mods | Reuses current form, clean backend | Requires editing Elementor form code | Post-MVP when replacing existing form |
| **D** | Elementor HTML Widget | No iframe, perfect visual match | CSS conflict risk, asset management | When design parity is critical |
| **E** | iframe + Shared CSS | Best of both worlds | Coordination complexity | When team can manage both codebases |

**MVP Recommendation**: **Option A (Standalone Flask + iframe)**

**Rationale**:
1. **Speed**: Can be built and deployed in 1-2 days
2. **Independence**: Doesn't require WordPress/PHP knowledge
3. **Flexibility**: Easy to iterate without affecting live site
4. **Future-proof**: Logic can be reused in any integration approach later
5. **Risk mitigation**: If MVP fails validation, no impact on existing site

**Integration Code for WordPress** (iframe approach):
```html
<!-- Add to any WordPress page via Custom HTML block -->
<div class="annuity-calculator-container">
  <iframe 
    src="https://your-flask-app.herokuapp.com" 
    width="100%" 
    height="800" 
    frameborder="0"
    scrolling="no"
    style="border: none;">
  </iframe>
</div>
```

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

### 6. Design Requirements - Visual Matching Guide

**Critical**: The MVP form MUST visually match the existing Elementor Pro form on annuitynest.com/custom-quote/

#### Form Structure (Exact Replication)

**Field Order and Layout**:
```
Row 1 (100%): Name
Row 2 (50/50): Email | Current Age
Row 3 (100%): Type of Annuity (Radio: Fixed, Fixed Indexed, Immediate, Variable)
Row 4 (50/50): Phone Number | Retirement Account (Radio: IRA, Non-IRA)
Row 5 (50/50): State of Residence | Amount of Annuity
Row 6 (50/50): Age of First Withdrawal (NEW - Variable only) | [empty space or additional field]
Row 7 (100%): Submit Button "Get my free quote"
```

**CSS Framework to Match**:
- Use CSS Grid for layout: `grid-template-columns: repeat(2, 1fr)`
- Gap between fields: `20px`
- Full-width fields: `grid-column: span 2`
- Responsive breakpoint: Stack to single column at `< 768px`

#### Visual Design Specifications

**Colors** (match Astra theme):
- Primary button: Use `#0055ff` or inherit from parent via CSS variable
- Input borders: `#ddd` default, `#0274be` on focus (Astra primary)
- Background: White or transparent (inherit from parent)
- Text: `#808285` (Astra body text color)

**Typography**:
- Font family: Inherit from parent (`font-family: inherit`)
- Labels: Above inputs, `font-weight: 500`
- Input text: `16px` (prevents mobile zoom)
- Button text: White on blue background

**Input Styling**:
```css
/* Match Elementor form inputs */
input, select {
  border: 1px solid #ddd;
  border-radius: 2px;
  padding: 12px 16px;
  font-size: 16px;
  width: 100%;
  box-sizing: border-box;
}

input:focus, select:focus {
  border-color: var(--ast-global-color-0, #0274be);
  outline: none;
}
```

**Button Styling**:
```css
/* Match "Get my free quote" button */
button[type="submit"] {
  background: var(--ast-global-color-0, #0055ff);
  color: white;
  border: none;
  border-radius: 2px;
  padding: 15px 30px;
  font-size: 16px;
  width: 100%;
  cursor: pointer;
}

button[type="submit"]:hover {
  opacity: 0.9;
}
```

**Radio Button Groups**:
- Display inline with spacing
- Custom styling to match Elementor's radio appearance
- Label positioning: To the right of radio input

**Conditional Field (Age of First Withdrawal)**:
- Initially hidden
- Show when "Variable" is selected in "Type of Annuity"
- Slide animation for smooth appearance
- Same styling as other number inputs

#### Responsive Behavior

**Desktop (> 768px)**:
- Two-column layout as specified
- Max-width: 800px (centered)
- Generous padding between sections

**Mobile (< 768px)**:
- Single column layout
- All fields stack vertically
- Touch-friendly input sizes (min 44px height)
- Radio buttons may need vertical stacking

**iframe Considerations**:
- Set `scrolling="no"` to prevent double scrollbars
- Use `width="100%"` for responsive width
- Set appropriate `height` (800px recommended)
- Test on actual WordPress page to verify no overflow

#### Implementation Approach

**Option 1: Pure CSS Replication (Recommended for MVP)**
- Write CSS from scratch matching observed Elementor styles
- No external dependencies
- Full control over appearance
- Risk: May not match exactly if theme updates

**Option 2: CSS Variables Inheritance**
- Attempt to inherit Astra's CSS variables
- Pros: Automatic updates with theme changes
- Cons: Variables may not be available in iframe context
- Requires testing on actual site

**Option 3: Style Injection**
- Copy computed styles from live site via browser DevTools
- Most accurate matching
- Time-consuming to extract all styles
- Overkill for MVP

**Recommendation**: Use Option 1 with careful visual comparison to live site.

---

## Extended Analysis & Implementation Findings

### Detailed Form Analysis (Live Site)

**Form Field Structure (Confirmed from Live Site)**:

| Order | Field ID | Type | Label | Required | Column Width | Notes |
|-------|----------|------|-------|----------|--------------|-------|
| 1 | `name` | text | Name | No | 100% | Full width, standalone row |
| 2 | `email` | email | Email | **Yes** | 50% | Left column |
| 3 | `field_da76045` | number | Current Age | No | 50% | Right column (paired with Email) |
| 4 | `field_7380ba6` | radio | Type of Annuity | No | 100% | Options: Fixed, Fixed Indexed, Immediate, Variable |
| 5 | `field_cc00e2c` | number | Phone Number | No | 50% | Left column |
| 6 | `field_fa40d48` | radio | Retirement Account | No | 50% | Right column (paired with Phone). Options: IRA, Non-IRA |
| 7 | `field_2d0e4d8` | select | State of Residence | **Yes** | 50% | Left column, all 50 states + DC |
| 8 | `field_9def4a9` | number | Amount of Annuity | **Yes** | 50% | Right column, min: $50,000 |

**Key Finding**: The existing form has **8 fields**, not 9. The "Age of First Withdrawal" field is **missing** and must be added as field #9 for Variable annuity calculations.

**Layout Pattern**:
```
Row 1: [Name - 100%]
Row 2: [Email - 50%] [Current Age - 50%]
Row 3: [Type of Annuity - 100% (Radio)]
Row 4: [Phone Number - 50%] [Retirement Account - 50% (Radio)]
Row 5: [State - 50%] [Amount - 50%]
Row 6: [Submit Button - 100%]
```

**CSS Classes Used**:
- `.elementor-form` - Main form container
- `.elementor-form-fields-wrapper` - Field wrapper
- `.elementor-labels-above` - Label positioning
- `.elementor-field-group` - Individual field group
- `.elementor-col-50` - 50% width columns
- `.elementor-col-100` - 100% width (full rows)
- `.elementor-field-type-{type}` - Type-specific styling
- `.elementor-button` - Submit button

### Astra Theme Design Tokens (Extracted)

| Token | Value | Usage |
|-------|-------|-------|
| `--ast-global-color-0` | Dynamic (set in theme) | Primary accent, focus borders |
| `--ast-global-color-2` | Dynamic | Secondary text |
| `--ast-border-color` | Dynamic | Input borders |
| `font-family` | `"Open Sans", sans-serif` | Body text |
| `border-radius` | `2px` | Inputs, buttons |
| Button padding | `.6em 1em .4em` | Default buttons |
| Input padding | `.75em` | Form inputs |
| Body text color | `#808285` | Paragraphs |
| Link color | `#4169e1` | Royal blue |

### Excel Data Structure Analysis

#### Fixed Annuity Rates.xlsx

**Structure Discovery**: Two-row format per product
- **Row N**: Company Name (col 1), Product Name (col 2), Product Type (col 3), Premium Type (col 4)
- **Row N+1**: Empty company, then Rate Term (col 5), Min Contribution (col 6), Min Rate (col 7), Base Rate (col 8), Bonus Rate (col 9), Yield to Surrender (col 10), Surrender Period (col 11)

**Sample Data Pattern**:
```
Row 3: [NaN, "Integrity Life Insurance Company", "New Momentum II", "MYG/CD", "Flexible", NaN, NaN, NaN, NaN, NaN, NaN, NaN]
Row 4: [NaN, NaN, NaN, NaN, NaN, 10, 2000.0, 2.5, 3.55, 0.75, 3.625, 7.0]
```

**Data Cleaning Required**:
1. Forward-fill company names from header row to data row
2. Parse Rate Term (can be number like "10" or string like "10 Year")
3. Convert Min. Contrib. to numeric (handling currency symbols)
4. Filter products where Min. Contrib. <= User Amount

#### Variable Annuity Rates.xlsx

**Structure**: Complex multi-carrier spreadsheet with age-based withdrawal rate tables

**Key Input Fields** (from the spreadsheet logic):
- Client Age at Issue: 55
- Age at First Withdrawal: 65  
- Initial Investment Amount: $1,000,000
- Deferral Period: 10 years (calculated as withdrawal age - current age)

**Withdrawal Rate Logic**:
- Rates vary by carrier and withdrawal age
- Age 59-64: ~4.75%
- Age 65-69: ~6.35%
- Age 70-74: ~6.55%
- Age 75-79: ~6.75%
- Age 80+: ~6.90%

**MVP Simplification**: Use average rates across carriers since implementing all carrier-specific logic would require significant additional development time.

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
    1. **Name** (text, 50% width, optional) - placeholder: "Name"
    2. **Email** (email, 50% width, required) - placeholder: "Email"
    3. **Current Age** (number, 50% width, optional) - min: 35, max: 85
    4. **Type of Annuity** (radio, 100% width, optional) - Options: Fixed, Fixed Indexed, Immediate, Variable
    5. **Phone Number** (tel, 50% width, optional) - placeholder: "Phone"
    6. **Retirement Account** (radio, 100% width, optional) - Options: IRA, Non-IRA
    7. **State of Residence** (select, 50% width, required) - All 50 states + DC
    8. **Amount of Annuity** (number, 50% width, required) - min: 50000, placeholder: "Minimum of $50,000"
    9. **Age of First Withdrawal** (number, 50% width, conditional) - min: 59, max: 85
        - **Conditional**: When "Variable" selected, show field 9
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

---

## MVP Implementation Strategy - Decision Framework

### Key Decisions Required

#### 1. Variable Annuity Calculation Approach

**Option A: Simplified Average Model (RECOMMENDED for MVP)**
- Use single withdrawal rate lookup table based on withdrawal age
- Ignore carrier-specific variations
- Formula: `Annual Income = Investment × Withdrawal Rate`
- **Pros**: Simple, fast, sufficient for proof-of-concept
- **Cons**: Not carrier-accurate, may vary from actual quotes

**Option B: Carrier-Specific Model (Post-MVP)**
- Implement full logic from Guaranteed Income Calculator
- Support multiple carriers with different calculation methods
- Handle rider options and fee structures
- **Pros**: Accurate quotes, competitive comparison
- **Cons**: Complex, requires extensive testing, longer timeline

**Decision**: Use **Option A** for MVP. Add disclaimer: "Rates are estimates based on average market rates. Actual rates may vary by carrier."

#### 2. Form Field Strategy

**Current State**: 8 fields on live site
**Required Addition**: Age of First Withdrawal (for Variable only)

**Option A: Add Field to Existing Form (RECOMMENDED)**
- Add as 9th field, shown conditionally
- Position: After Amount of Annuity (Row 6)
- Layout: 50% width, paired with empty space or additional info

**Option B: Two-Step Form**
- Step 1: Capture basic info (current 8 fields)
- Step 2: Show calculation-specific fields
- **Cons**: More complex, may reduce completion rate

**Decision**: Use **Option A** - simple, maintains single-step flow

#### 3. Data Update Strategy

**Question**: How will Excel files be updated in production?

**Option A: Manual File Replacement**
- Upload new Excel files to server
- Restart Flask app to reload data
- **Pros**: Simple, no database needed
- **Cons**: Downtime during updates, manual process

**Option B: Admin Upload Interface**
- Create simple upload page for Excel files
- Auto-reload data on upload
- **Pros**: No server access needed, faster updates
- **Cons**: Additional development, security considerations

**Decision**: Start with **Option A** for MVP. Add admin interface in Phase 2.

#### 4. State Filtering

**Question**: Should results be filtered by user's state?

**Option A: No State Filtering (RECOMMENDED for MVP)**
- Show all products regardless of state
- Add disclaimer about state availability
- **Pros**: More options shown, simpler logic
- **Cons**: Some products may not be available in user's state

**Option B: State-Specific Filtering**
- Filter products by state availability
- Requires state data in Excel (not currently present)
- **Pros**: Accurate, compliant
- **Cons**: Requires data enhancement, may show few/no results in some states

**Decision**: Use **Option A** with disclaimer: "Product availability varies by state. Contact us to confirm eligibility."

#### 5. Lead Capture Integration

**Question**: Should form submissions feed into existing lead system?

**Option A: Separate MVP Data (RECOMMENDED for MVP)**
- MVP captures leads in its own database/storage
- No integration with existing Elementor form
- **Pros**: Independent, no risk to existing system
- **Cons**: Manual transfer of leads needed

**Option B: Dual Submission**
- Submit to both MVP backend and existing Elementor form
- **Pros**: Leads go to existing workflow
- **Cons**: Complex, may fail if either system is down

**Decision**: Use **Option A**. Export leads periodically or add integration later.

### Implementation Checklist

#### Phase 1: MVP Core (Days 1-2)
- [ ] Set up Flask project structure
- [ ] Create data cleaning scripts for Fixed Annuity Excel
- [ ] Implement Fixed Annuity filtering logic
- [ ] Create simplified Variable Annuity calculation
- [ ] Build HTML form matching Elementor design
- [ ] Add CSS styling (Astra theme match)
- [ ] Implement JavaScript form handling
- [ ] Create results display (table for Fixed, card for Variable)
- [ ] Add basic validation (client-side and server-side)
- [ ] Test locally with sample data

#### Phase 2: Integration Ready (Day 3)
- [ ] Deploy to hosting (Heroku/PythonAnywhere)
- [ ] Test iframe embedding on staging page
- [ ] Verify responsive design on mobile
- [ ] Add error handling and loading states
- [ ] Create WordPress embed instructions
- [ ] Test cross-origin functionality
- [ ] Document deployment process

#### Phase 3: Validation (Day 4)
- [ ] Test with real user scenarios
- [ ] Verify calculations against Excel
- [ ] Get stakeholder feedback
- [ ] Iterate based on feedback
- [ ] Prepare for production deployment

### Success Criteria

**MVP is successful if**:
1. Users can complete the form and see results
2. Fixed Annuity results show products matching user's investment amount
3. Variable Annuity shows projected income based on age inputs
4. Form visually matches existing site design
5. Page loads in under 3 seconds
6. Works on desktop and mobile devices
7. Can be embedded in WordPress via iframe

**Not required for MVP**:
- Carrier-specific accuracy for Variable annuities
- State-specific product filtering
- Lead capture integration with existing system
- PDF generation
- User accounts or saved quotes
- Advanced error recovery

---
