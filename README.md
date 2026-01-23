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

### Basic Risk Analysis

```python
import pyreto as pr

# Fit Student's T distribution
par = pr.student_t.fit(returns)

# Calculate 1% Expected Shortfall
es = pr.student_t.es(par, alpha=0.01)

# Calculate 5% Value at Risk
var = pr.student_t.var(par, alpha=0.05)
```

### Monte Carlo Simulation (Multi-Asset)

```python
import pyreto as pr
import numpy as np

# Define margins for each asset
margins = {
    "SPY": {"type": "student_t", "par": {"df": 3.5, "loc": 0.0, "scale": 0.012}},
    "TLT": {"type": "student_t", "par": {"df": 5.0, "loc": 0.0, "scale": 0.008}},
    "GLD": {"type": "nig", "par": {"alpha": 2.0, "beta": 0.0, "delta": 0.01, "mu": 0.0, "gamma": 2.0}}
}

# Simulate 50,000 correlated returns via Gaussian copula
mc_returns = pr.mc.simulate("gaussian", margins, n_draws=50_000, seed=42)

# Build portfolio (60% SPY, 30% TLT, 10% GLD)
weights = np.array([0.6, 0.3, 0.1])
port_returns = pr.mc.simulate_portfolio(weights, mc_returns)

# Calculate portfolio risk
var_99 = np.percentile(port_returns, 1)  # 1% VaR
es_99 = np.mean(port_returns[port_returns <= var_99])  # 1% ES

print(f"Portfolio VaR(1%): {var_99:.4f} ({var_99*100:.2f}%)")
print(f"Portfolio ES(1%): {es_99:.4f} ({es_99*100:.2f}%)")
```

### t-Copula for Heavier Tails

```python
# Use t-copula for more realistic tail dependence
t_margins = {
    "SPY": {"type": "student_t", "par": {"df": 4.0, "loc": 0.0, "scale": 0.01}}
}

# t-copula with 5 degrees of freedom (canonical choice)
t_returns = pr.mc.simulate("t", t_margins, n_draws=50_000, seed=42)
t_port = pr.mc.simulate_portfolio(np.array([1.0]), t_returns)

# t-copula produces more extreme tail events than Gaussian
t_var_99 = np.percentile(t_port, 1)
print(f"t-copula VaR(1%): {t_var_99:.4f} ({t_var_99*100:.2f}%)")
```

### Reproducible Results

```python
# Same seed produces identical results
sim1 = pr.mc.simulate("gaussian", margins, n_draws=10_000, seed=123)
sim2 = pr.mc.simulate("gaussian", margins, n_draws=10_000, seed=123)

assert (sim1["SPY"] == sim2["SPY"]).all()  # Exactly identical
```

## API

Each distribution module (student_t, alpha_stable, nig, gpd) exposes:

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

### Peaks Over Threshold (GPD)

```python
import pyreto as pr
import numpy as np

# For Peaks Over Threshold, extract exceedances above a threshold
returns = np.random.standard_t(3, 1000) * 0.01
threshold = np.percentile(returns, 95)  # 95th percentile threshold
exceedances = returns[returns > threshold] - threshold

# Fit Generalised Pareto Distribution to exceedances
par_gpd = pr.gpd.fit(exceedances)
print(f"GPD Parameters: {par_gpd}")

# Calculate VaR and ES for exceedances
var_exc = pr.gpd.var(0.05, par_gpd)
es_exc = pr.gpd.es(0.05, par_gpd)
print(f"Exceedance VaR(5%): {var_exc:.4f}")
print(f"Exceedance ES(5%): {es_exc:.4f}")

# Convert back to original scale if needed
var_original = threshold + var_exc
es_original = threshold + es_exc
print(f"Original scale VaR(5%): {var_original:.4f}")
print(f"Original scale ES(5%): {es_original:.4f}")
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
- `gpd`: Generalised Pareto Distribution (Peaks Over Threshold)

All models use identical function signatures.
### R‑vine Copulas (Multi‑asset dependence modelling)

*Requires:* `pip install pyvinecop`

```python
import pyreto as pr
import polars as pl
import numpy as np

# Load three‑asset returns (included CSV) 
df = pl.read_csv("spy_returns.csv").select(["SPY", "TLT", "VIX"])

# Fit R‑vine, select best family per pair via AIC
vine = pr.vine.fit(df, family_set=["gumbel", "joe", "t"], method="mle")
print(f"AIC = {vine['aic']:.2f}")

# Simulate 50 k uniforms from the vine
u = pr.vine.simulate(vine, n_draws=50_000, seed=42)

# Upper‑tail‑dependence (e.g. SPY–VIX in crisis)
lambda_U = pr.vine.upper_tail_dependence(vine, pair=("asset_0", "asset_2"))
print(f"λ_U(SPY,VIX) = {lambda_U:.3f}")
```