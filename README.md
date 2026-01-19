# pyreto

Tail risk management library (classless / functional API).

## Installation

```bash
pip install pyreto
```

Requires: numpy, scipy

## Usage

```python
import pyreto as pr

# Fit Student's T distribution
par = pr.student_t.fit(returns)

# Calculate 1% Expected Shortfall
es = pr.student_t.es(par, alpha=0.01)

# Calculate 5% Value at Risk
var = pr.student_t.var(par, alpha=0.05)
```

## API

Each distribution module (student_t, alpha_stable, nig) exposes:

- `fit(returns)` → dict (fitted parameters)
- `pdf(x, par)` → ndarray (density)
- `cdf(x, par)` → ndarray (distribution)
- `ppf(q, par)` → ndarray (quantile)
- `var(alpha, par)` → float (Value at Risk)
- `es(alpha, par)` → float (Expected Shortfall)

## Example

```python
import numpy as np
import pyreto as pr

# Generate heavy-tailed returns
returns = np.random.standard_t(3, 1000) * 0.01

# Fit Student's T
par = pr.student_t.fit(returns)
print(f"Parameters: {par}")

# Calculate tail risk
var_5 = pr.student_t.var(par, alpha=0.05)
es_5 = pr.student_t.es(par, alpha=0.05)
print(f"5% VaR: {var_5:.4f}")
print(f"5% ES: {es_5:.4f}")

# Try different models
par_stable = pr.alpha_stable.fit(returns)
es_stable = pr.alpha_stable.es(par_stable, alpha=0.01)
print(f"Alpha-Stable ES(1%): {es_stable:.4f}")

par_nig = pr.nig.fit(returns)
es_nig = pr.nig.es(par_nig, alpha=0.01)
print(f"NIG ES(1%): {es_nig:.4f}")
```

## Error Handling

```python
import pyreto as pr

# Invalid alpha raises ValueError
pr.student_t.es(par, alpha=1.5)   # ValueError
pr.student_t.var(par, alpha=-0.1)  # ValueError

# NaN in returns raises ValueError
returns = [1, 2, np.nan, 4]
pr.student_t.fit(returns)  # ValueError

# Empty returns raises ValueError
pr.student_t.fit([])  # ValueError
```

## Models

- `student_t`: Student's T distribution (recommended, fastest)
- `alpha_stable`: Alpha stable distribution (most flexible, slower)
- `nig`: Normal-inverse Gaussian (good balance)

All models use identical function signatures.
