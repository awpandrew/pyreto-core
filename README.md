# pyreto

Tail risk management library (classless / functional API).

## Installation

```bash
pip install pyreto
```

Requires: numpy, scipy

## Quick Start with Included SPY Data

pyreto includes **5 years of SPY daily returns (1260 trading days)** so you can test immediately without downloading data:

```bash
# Run the included example
python example_spy_analysis.py
```

Or manually:
```python
import pyreto as pr
import numpy as np

# Load included SPY data
returns = np.genfromtxt('spy_returns.csv', delimiter=',', skip_header=1)

# Analyze with Student's T (fastest)
par = pr.student_t.fit(returns)
var = pr.student_t.var(0.05, par)
es = pr.student_t.es(0.05, par)

print(f"SPY 5% VaR: {var:.4f}")
print(f"SPY 5% ES: {es:.4f}")
```

**Example output:**
```
SPY 5% VaR: -0.0273 (-2.73%)
SPY 5% ES: -0.0392 (-3.92%)
SPY 1% VaR: -0.0459 (-4.59%)
SPY 1% ES: -0.0606 (-6.06%)
```

The data shows realistic SPY characteristics:
- Mean: ~-0.0007 (slight negative drift)
- Std: 0.0187 (1.87% daily volatility)
- Fat tails ~1.2x normal distribution

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

## Testing with Included Data

The repository includes `spy_returns.csv` with 5 years of daily SPY returns.
Run the example analysis:

```bash
git clone https://github.com/user/pyreto
cd pyreto
pip install -e .

# Run example
python example_spy_analysis.py
```

Or manually:
```python
import pyreto as pr
import polars as pl

# Load included SPY data
returns = pl.read_csv('spy_returns.csv')['daily_return'].to_numpy()

# Analyze with all models
for model_name in ['student_t', 'alpha_stable', 'nig']:
    model = getattr(pr, model_name)
    par = model.fit(returns)
    var = model.var(par, alpha=0.05)
    es = model.es(par, alpha=0.05)
    print(f"{model_name}: VaR={var:.4f}, ES={es:.4f}")
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
