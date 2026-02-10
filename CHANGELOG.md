# Changelog

All notable changes to the Annuity Nest MVP project.

## [2026-02-10] - Calculator Fixes

### Fixed

#### Fixed Annuity Calculation
- **Issue**: Future value remained the same regardless of investment amount entered
- **Root Cause**: Reading pre-calculated future values directly from Excel instead of calculating dynamically
- **Solution**: Implemented Excel formula `=+$C$3*(1+(I10/100))^10` using:
  - User's investment amount (replaces $C$3)
  - Yield to Surrender rate from column I
  - Fixed 10 years (as per Excel formula - all products use 10-year calculation)
- **Result**: Future value now scales correctly with different investment amounts using the same calculation as the Excel

**Example:**
- Investment: $100,000 at 4.9% Yield to Surrender for 10 years → Future Value: $155,229.03
- Investment: $525,000 at 4.9% Yield to Surrender for 10 years → Future Value: $814,952.43
- Investment: $1,000,000 at 5.3% Yield to Surrender for 10 years → Future Value: $1,676,037.42 ✓ (matches Excel)

#### Variable Annuity Calculation
- **Issue**: Calculated values didn't match the Excel file values
- **Root Cause**: Using simple scaling instead of Excel's formula-based calculations
- **Solution**: Implemented Excel formulas:
  - Benefit Base = Investment + (Investment × Deferral Credit Rate × Deferral Period) [SIMPLE INTEREST]
  - Annual Lifetime Income = Benefit Base × Withdrawal Rate
- **Result**: Values now match Excel exactly and work correctly for any age/deferral period combination

**Example:** Age 60, Withdrawal 65 (5-year deferral), $525,000 investment
- Brighthouse FlexChoice Access - Level:
  - Deferral Credit Rate: 5%
  - Benefit Base: $525,000 + ($525,000 × 0.05 × 5) = $656,250.00 ✓
  - Annual Income: $656,250.00 × 6.4% = $42,000.00 ✓
- Corebridge Polaris Income Plus Daily Flex - Option 3:
  - Deferral Credit Rate: 6%
  - Benefit Base: $525,000 + ($525,000 × 0.06 × 5) = $682,500.00 ✓
  - Annual Income: $682,500.00 × 6.15% = $41,973.75 ✓

### Technical Changes

#### logic.py
- Added `calculate_fixed_future_value()` method using compound interest formula
- Updated `get_fixed_rates()` to calculate future value dynamically instead of reading from Excel
- Updated `get_fixed_rates()` to show ALL products (removed minimum contribution filtering)
- Updated `get_fixed_rates()` to use 10 years for all products (matching Excel formula `^10`)
- Updated `get_variable_income()` to use Excel formulas for Benefit Base and Annual Lifetime Income calculations
  - Uses simple interest: `=+$C$4+($C$4*F12*$C$5)` (not compound interest)
- Updated `get_variable_income()` to sort by Sort column (not by income)
- Future value now rounds to 2 decimal places for currency display

#### data_processor.py
- Modified `load_variable_annuity_data()` to load Deferral Credit Rate from column F
- Removed pre-calculated Benefit Base and Annual Lifetime Income columns (now calculated dynamically)
- Fixed bug where "Company" filter was matching all company names (changed to exact match)
- Dataframe now contains raw inputs needed for formula calculations

### Files Modified
- `logic.py` - Fixed annuity future value calculation, variable annuity formula implementation
- `data_processor.py` - Added Deferral Credit Rate loading, removed pre-calculated columns
- `excel files/Fixed Annuity Rates.xlsx` - Updated to latest version
- `excel files/Variable Annuity Rates.xlsx` - Updated to latest version
- `README.md` - Updated calculation documentation with formulas
- `CHANGELOG.md` - Updated with improved implementation details
- `test_fixes.py` - Added comprehensive test script for verification
- `test_variable_formula.py` - Added formula verification test

### Testing
All tests pass:
- `python3 test_implementation.py` - Original test suite passes
- `python3 test_fixes.py` - Detailed calculation verification passes

## [2026-02-09] - Initial Release

### Features
- Fixed Annuity calculator with all columns and rows from Excel
- Variable Annuity calculator with columns B, C, E, S
- Conditional fields (Age of First Withdrawal only shows for Variable)
- Responsive design matching Elementor/Astra theme
- iframe-ready for WordPress embedding
- Form validation (minimum $50,000 investment, age validation)

### Technical Stack
- Flask backend
- Pandas for Excel processing
- Vanilla JavaScript frontend
- Responsive CSS
