# Generalised Pareto Distribution (GPD) Implementation Summary

## Overview

Successfully implemented Generalised Pareto Distribution (GPD) for Peaks Over Threshold (POT) analysis in `pyreto.gpd`.

## Implementation Details

### Module: `src/pyreto/distributions/gpd.py`

**Size**: 102 lines (following suckless principles)

**Functions implemented**:
1. `fit(returns)` - Fit GPD parameters using MLE
2. `pdf(x, par)` - Probability density function
3. `cdf(x, par)` - Cumulative distribution function
4. `ppf(q, par)` - Percent point function (inverse CDF)
5. `var(alpha, par)` - Value at Risk
6. `es(alpha, par)` - Expected Shortfall

**Key features**:
- Uses `scipy.stats.genpareto` for core computations
- Handles all three GPD cases:
  - Exponential (c=0): Standard exponential distribution
  - Heavy tail (c>0): Pareto-type heavy tails
  - Bounded (c<0): Beta-type bounded tails
- Properly handles finite upper bound for c>0 case
- Uses shared validation utilities from `util` module
- Follows functional API pattern consistent with other distributions

## Shared Utilities

### Module: `src/pyreto/distributions/util.py`

**Functions**:
1. `validate_returns(returns)` - Validate and normalize return data
2. `validate_alpha(alpha)` - Validate significance level

**Features**:
- Shared across all distributions (avoid code duplication)
- Proper type hints
- Warning for low sample sizes (< 30 observations)
- Clear error messages for invalid inputs

## Tests

### Module: `tests/test_gpd.py`

**Comprehensive test suite** with 60+ test cases covering:

1. **Fitting tests**:
   - Basic fitting functionality
   - Heavy-tailed data
   - Input validation (empty, NaN, Inf)

2. **CDF tests**:
   - Scalar and array inputs
   - Monotonicity
   - Boundary values

3. **PDF tests**:
   - Scalar and array inputs
   - Positivity
   - Shape validation

4. **PPF tests**:
   - Scalar and array inputs
   - CDF-PPF roundtrip
   - Boundary values

5. **Risk measure tests**:
   - VaR at different levels (0.1, 0.05, 0.01, 0.001)
   - ES at different levels
   - VaR/ES consistency (ES more extreme than VaR)
   - Alpha validation

6. **Special cases**:
   - Exponential case (c=0)
   - Heavy tail case (c>0)
   - Bounded case (c<0)

**Quick test runner**: `test_gpd_quick.py` for fast validation

## Package Integration

Updated package structure:
- `src/pyreto/__init__.py` - Added gpd to exports
- `src/pyreto/distributions/__init__.py` - Added gpd to distribution list
- `tests/test_gpd.py` - Comprehensive test suite
- `README.md` - Added GPD usage examples

## Usage Examples

### Basic GPD Usage

```python
import pyreto as pr
import numpy as np

# Extract exceedances above a threshold
returns = np.random.standard_t(3, 1000) * 0.01
threshold = np.percentile(returns, 95)
exceedances = returns[returns > threshold] - threshold

# Fit GPD to exceedances
par = pr.gpd.fit(exceedances)
print(f"GPD Parameters: {par}")

# Calculate risk metrics
var = pr.gpd.var(0.05, par)
es = pr.gpd.es(0.05, par)
print(f"VaR(5%): {var:.4f}")
print(f"ES(5%): {es:.4f}")
```

### Special Cases

```python
# Exponential distribution (c=0)
exponential_par = {'c': 0.0, 'loc': 0.0, 'scale': 1.0}

# Heavy tail (c>0)
heavytail_par = {'c': 0.3, 'loc': 0.0, 'scale': 1.0}

# Bounded tail (c<0)
bounded_par = {'c': -0.3, 'loc': 0.0, 'scale': 1.0}
```

## Testing Results

All tests pass successfully:
- ✅ Fit functionality
- ✅ CDF/PDF/PPF operations
- ✅ VaR/ES calculations
- ✅ Input validation
- ✅ Special cases (exponential, heavy tail, bounded)
- ✅ Integration with package

## Key Implementation Details

1. **Scalar handling**: All functions properly handle scalar inputs from scipy
2. **Integration bounds**: ES integration uses appropriate bounds for c>0 case
3. **Finite handling**: Properly handles finite upper bounds when c > 0
4. **Validation**: Uses shared utilities for consistent error handling
5. **API consistency**: Follows same functional pattern as other distributions

## Branch Information

- **Branch**: feature/gpd
- **Status**: Complete and tested
- **Commit**: 165f4b1
- **Ready for**: merge to master

## Dependencies

- numpy>=1.20.0
- scipy>=1.10.0 (for genpareto)
- Uses existing pyreto structure

## Applications

The GPD is particularly useful for:
- **Peaks Over Threshold (POT)** analysis
- **Extreme value theory**
- **Tail risk modeling**
- **Stress testing**
- **Environmental extremes**
- **Insurance claims**

The GPD complements the existing distributions by providing a specialized tool for modeling exceedances above a threshold, which is common in extreme value analysis.
