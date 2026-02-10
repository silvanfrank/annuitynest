# Changelog

All notable changes to the Annuity Nest MVP project.

## [2026-02-10] - Calculator Fixes

### Fixed

#### Fixed Annuity Calculation
- **Issue**: Future value remained the same regardless of investment amount entered
- **Root Cause**: Reading pre-calculated future values directly from Excel instead of calculating dynamically
- **Solution**: Implemented compound interest formula `FV = P × (1 + r)^n` to calculate future value based on user's actual investment amount
- **Result**: Future value now scales correctly with different investment amounts

**Example:**
- Investment: $100,000 at 4.9% for 7 years → Future Value: $139,774.65
- Investment: $525,000 at 4.9% for 7 years → Future Value: $733,816.92

#### Variable Annuity Calculation
- **Issue**: Calculated values didn't match the Excel file values
- **Root Cause**: Hardcoded scaling factor of $1,000,000, but Excel was using $525,000 as the base amount
- **Solution**: Modified data processor to read the actual investment amount from Excel's input cells (row 3, column 2) and use that as the scaling base
- **Result**: Values now match Excel exactly for the same input parameters

**Example:** Age 60, Withdrawal 65, $525,000 investment
- Brighthouse FlexChoice Access - Level:
  - Benefit Base: $670,047.82 ✓ (matches Excel)
  - Annual Income: $42,883.06 ✓ (matches Excel)

### Technical Changes

#### logic.py
- Added `calculate_fixed_future_value()` method using compound interest formula
- Updated `get_fixed_rates()` to calculate future value dynamically instead of reading from Excel
- Updated `get_variable_income()` to use Excel's base investment amount from dataframe attributes
- Future value now rounds to 2 decimal places for currency display

#### data_processor.py
- Modified `load_variable_annuity_data()` to read investment amount from Excel input cells
- Added base investment detection from row 3, column 2 of the Formatted sheet
- Stored base investment as dataframe attribute for use by calculator

### Files Modified
- `logic.py` - Fixed annuity future value calculation, variable annuity scaling
- `data_processor.py` - Added base investment detection from Excel
- `excel files/Fixed Annuity Rates.xlsx` - Updated to latest version
- `excel files/Variable Annuity Rates.xlsx` - Updated to latest version
- `README.md` - Updated calculation documentation
- `test_fixes.py` - Added comprehensive test script for verification

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
