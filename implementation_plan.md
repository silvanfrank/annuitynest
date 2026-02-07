# Annuity Nest MVP Implementation Plan

## Original Task Description

**MVP** = Minimum Viable Product

Using this page as a template https://annuitynest.com/custom-quote/ we need to capture user data, feed the spreadsheet and output the information back to the website.

We need to distinguish between a **Fixed Annuity** and a **Variable Annuity**. And for a Variable Annuity we need to ascertain a **Current Age** and **Age of First Withdrawal**. The Age of First Withdrawal is currently not on my site, so you'll need to build it in for this project.

**File Explanations**:
- **Fixed Annuity Rates** - point to point investments that pay interest over a certain amount of time
- **Variable Annuity Rates** - mutual fund like investments that pay annual withdrawals at a user defined starting point anywhere from immediately (0 years) up to 20 years. The annual withdrawals continue even if the investment performance does not sustain the withdrawal amounts and the account runs out of money.
- **Guaranteed Income Calculator 1 26 26** - our master file. Just good to have. I built Variable Annuity Rates from this as I did not know if you could properly extract info from it in its original state.

Ask questions as necessary and I think this MVP should be doable to prove the concept.

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

### Data Structure

**Fixed Annuity Rates.xlsx**:
- 348 products across multiple carriers
- Two-row format per product (company name on row N, details on row N+1)
- Key columns: Company, Product, Product Type, Rate Term, Min. Contrib., Base Rate
- **MVP Logic**: Filter where `Min. Contrib. ≤ User Amount`, sort by `Base Rate` descending

**Variable Annuity Rates.xlsx**:
- Complex multi-carrier structure with age-based withdrawal tables
- Deferral Period = Withdrawal Age - Current Age
- **MVP Simplification**: Use averaged withdrawal rates by age bracket instead of carrier-specific calculations

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
├── static/
│   ├── style.css        # Astra theme matching
│   └── script.js        # Form handling, API calls
└── templates/
    └── index.html       # Main form
```

### Design Requirements

Match Elementor Pro form styling:
- **Layout**: Two-column grid, responsive to single column at <768px
- **Field Order**: Name → Email/Current Age → Annuity Type → Phone/Retirement → State/Amount → [Variable only: Age of First Withdrawal] → Submit
- **Colors**: Primary blue `#0055ff`, input borders `#ddd`, focus `#0274be`
- **Typography**: Inherit from parent, 16px inputs (prevents mobile zoom)
- **Button**: Full width, "Get my free quote", blue background

### Variable Annuity Calculation (MVP Simplified)

```python
# Simplified withdrawal rates by withdrawal age
WITHDRAWAL_RATES = {
    59: 0.0475, 60: 0.0475, 61: 0.0475, 62: 0.0475, 63: 0.0475,
    64: 0.0475, 65: 0.0635, 66: 0.0635, 67: 0.0635, 68: 0.0635,
    69: 0.0635, 70: 0.0655, 71: 0.0655, 72: 0.0655, 73: 0.0655,
    74: 0.0655, 75: 0.0675, 76: 0.0675, 77: 0.0675, 78: 0.0675,
    79: 0.0675, 80: 0.0690, 81: 0.0690  # 81+
}

# Formula
Annual Income = Investment Amount × Withdrawal Rate
Deferral Period = Withdrawal Age - Current Age
```

**Disclaimer**: "Rates are estimates based on average market rates. Actual rates may vary by carrier."

---

## Implementation Phases

### Phase 1: MVP Core (Days 1-2)
- [ ] Data cleaning scripts for Excel files
- [ ] Flask app with basic form (matching Elementor structure)
- [ ] Fixed annuity filtering logic
- [ ] Variable annuity simplified calculation
- [ ] Basic results display (table for Fixed, card for Variable)
- [ ] Form validation (client + server side)

### Phase 2: Integration Ready (Day 3)
- [ ] CSS styling match with Astra theme
- [ ] Responsive design (mobile-first)
- [ ] iframe embed code for WordPress
- [ ] Error handling and loading states
- [ ] Deploy to hosting (PythonAnywhere/Heroku)

### Phase 3: Validation (Day 4)
- [ ] Test with real user scenarios
- [ ] Verify calculations against Excel
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
```

---

## Future Enhancements (Post-MVP)

1. **Carrier-specific variable calculations** - Implement full logic from Guaranteed Income Calculator
2. **State filtering** - Filter products by state availability (requires data enhancement)
3. **Lead integration** - Connect to existing Elementor form submissions
4. **PDF generation** - Save/print quotes as PDF
5. **Admin interface** - Upload and manage Excel files without server access
6. **Analytics** - Track form completions and quote views

---

## Success Criteria

**MVP is successful if**:
- [ ] Users can complete the form and see results
- [ ] Fixed Annuity results show products matching user's investment amount
- [ ] Variable Annuity shows projected income based on age inputs
- [ ] Form visually matches existing site design
- [ ] Page loads in under 3 seconds
- [ ] Works on desktop and mobile devices
- [ ] Can be embedded in WordPress via iframe

**Not required for MVP**:
- Carrier-specific accuracy for Variable annuities
- State-specific product filtering
- Lead capture integration with existing system
- PDF generation
- User accounts or saved quotes
