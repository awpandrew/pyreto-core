# pyreto

Tail risk management library.

## Installation

```bash
pip install pyreto
```

Requires: numpy, scipy
Optional: polars (for CSV/DataFrame support)

## Usage

```python
import pyreto

# Fit Student's T distribution
model = pyreto.dist.fit('returns.csv', column='daily_return', model='student_t')

# Calculate 1% Expected Shortfall
es_1 = model.es(0.01)

# Calculate 5% Value at Risk  
var_5 = model.var(0.05)

# Get fitted parameters
params = model.params
```

## Models

- `student_t`: Student's T distribution (recommended)
- `alpha_stable`: Alpha stable distribution (flexible, slower)
- `nig`: Normal-inverse Gaussian (good middle ground)

## API

All models support:
- `fit()` - Fit parameters
- `pdf(x)` - Density function
- `cdf(x)` - Distribution function
- `ppf(q)` - Quantile function
- `var(alpha)` - Value at Risk
- `es(alpha)` - Expected Shortfall
- `params` - Fitted parameters dict

## Example

```python
import numpy as np
import pyreto

# Generate heavy-tailed returns
returns = np.random.standard_t(3, 1000) * 0.01

# Fit and calculate tail risk
model = pyreto.dist.fit(returns, model='student_t')
print(f"5% VaR: {model.var(0.05):.4f}")
print(f"5% ES:  {model.es(0.05):.4f}")
```

## Error Handling

The library fails loudly on invalid inputs:
- Non-finite values (NaN, Inf) throw `ValueError`
- Invalid alpha values throw `ValueError`
- Missing parameters throw `ValueError`
