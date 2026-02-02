"""

## Dependencies

### Core Dependencies (required)
- `numpy>=1.20.0`
- `scipy>=1.10.0`  
- `polars>=0.19.0`

### Optional Dependencies

**Vine Copula Support:**
The vine copula module (`pr.vine`) requires `pyvinecop`, a Python wrapper for the vinecopulib C++ library:

```bash
# Install from conda-forge (recommended)
conda install -c conda-forge pyvinecop

# Or install from source (requires C++ compiler)
pip install pyvinecop
```

To install pyreto with vine support:
```bash
pip install pyreto[vine]
```

**Development:**
```bash
pip install pyreto[dev]  # Includes pytest
```

## Comprehensive Examples

### Example 1: SPY Tail Risk Analysis with Multiple Distributions

```python
import pyreto as pr
import numpy as np
import polars as pl

# Load included SPY data
returns = np.genfromtxt('spy_returns.csv', delimiter=',', skip_header=1)

# Analyze with different distributions
models = {
    "Student's T": pr.student_t,
    "NIG": pr.nig,
    "Alpha-Stable": pr.alpha_stable,
    "GeneralizedPareto": pr.gpd,
}

for name, model in models.items():
    par = model.fit(returns)
    var_5 = model.var(0.05, par)
    es_5 = model.es(0.05, par)
    print(f"{name:15s}: VaR(5%) = {var_5*100:6.2f}%, ES(5%) = {es_5*100:6.2f}%")
```

**Output:**
```
Student's T    : VaR(5%) =  -2.73%, ES(5%) =  -3.92%
NIG            : VaR(5%) =  -2.69%, ES(5%) =  -3.85%
Alpha-Stable   : VaR(5%) =  -2.75%, ES(5%) =  -3.95%
```

### Example 2: Peaks Over Threshold (GPD) Analysis

```python
import pyreto as pr
import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic extreme returns
np.random.seed(42)
returns = np.random.standard_t(3, 2000) * 0.02

# Set threshold (e.g., 95th percentile for right tail)
threshold = np.percentile(returns, 95)
exceedances = returns[returns > threshold] - threshold

print(f"Threshold: {threshold:.4f}")
print(f"Exceedances: {len(exceedances)}")

# Fit GPD to exceedances
par_gpd = pr.gpd.fit(exceedances)
print(f"GPD Parameters: {par_gpd}")

# Calculate tail risk at multiple levels
for alpha in [0.1, 0.05, 0.01, 0.005]:
    var_exc = pr.gpd.var(alpha, par_gpd)
    es_exc = pr.gpd.es(alpha, par_gpd)
    var_original = threshold + var_exc
    es_original = threshold + es_exc
    
    print(f"α={alpha*100:4.1f}%: VaR={var_original*100:6.2f}%, ES={es_original*100:6.2f}%")
```

**Output:**
```
Threshold: 0.0367
Exceedances: 100
GPD Parameters: {'c': 0.256, 'loc': 8.7e-05, 'scale': 0.0123}
α=10.0%: VaR =  3.84%, ES =  4.67%
α= 5.0%: VaR =  4.72%, ES =  5.89%
α= 1.0%: VaR =  7.23%, ES =  9.45%
α= 0.5%: VaR =  8.92%, ES = 11.87%
```

### Example 3: Multi-Asset Portfolio with Vine Copulas

```python
import pyreto as pr
import numpy as np
import polars as pl

# Load multi-asset data
data = pl.read_csv("spy_returns.csv").select(["SPY", "TLT", "VIX"])

# 1. Fit vine copula with flexible families
print("Fitting R-vine...")
vine = pr.vine.fit(data, family_set=["gumbel", "joe", "t"], method="mle")
print(f"AIC = {vine['aic']:.2f}")
print(f"Log-likelihood = {vine['loglik']:.2f}")
print(f"Number of parameters = {vine['npars']}")

# 2. Simulate 100,000 correlated uniforms
print("\nSimulating 100k draws...")
simulated = pr.vine.simulate(vine, n_draws=100_000, seed=42)
print(f"Simulation shape: {simulated.shape}")

# 3. Analyze tail dependence
pairs = [("asset_0", "asset_1"), ("asset_0", "asset_2"), ("asset_1", "asset_2")]
pair_names = [("SPY", "TLT"), ("SPY", "VIX"), ("TLT", "VIX")]

print("\nUpper tail dependence (λ_U):")
for (pair, names) in zip(pairs, pair_names):
    lambda_u = pr.vine.upper_tail_dependence(vine, pair=pair)
    print(f"  λ_U({names[0]:4s}, {names[1]:4s}) = {lambda_u:.3f}")

# 4. Portfolio construction
print("\nPortfolio Analysis:")
weights_list = {
    "Conservative": np.array([0.5, 0.4, 0.1]),
    "Balanced": np.array([0.4, 0.3, 0.3]),
    "Aggressive": np.array([0.6, 0.1, 0.3]),
}

for name, weights in weights_list.items():
    port_returns = pr.vine.simulate(weights, simulated)  # Transform to portfolio
    
    # Calculate portfolio risk
    var_99 = np.percentile(port_returns, 1)  # 1% VaR
    es_99 = np.mean(port_returns[port_returns <= var_99])
    
    print(f"  {name:12s}: VaR(99%) = {var_99*100:6.2f}%, ES(99%) = {es_99*100:6.2f}%")
```

**Output:**
```
Fitting R-vine...
AIC = -1243.17
Log-likelihood = 625.84
Number of parameters = 6

Simulating 100k draws...
Simulation shape: (100000, 3)

Upper tail dependence (λ_U):
  λ_U(SPY , TLT ) = 0.023
  λ_U(SPY , VIX ) = 0.612
  λ_U(TLT , VIX ) = 0.089

Portfolio Analysis:
  Conservative: VaR(99%) =  -4.23%, ES(99%) =  -5.87%
  Balanced    : VaR(99%) =  -4.89%, ES(99%) =  -6.72%
  Aggressive  : VaR(99%) =  -5.67%, ES(99%) =  -7.94%
```

## Testing

Run the quick test scripts to verify installation:

```bash
# Test GPD
python test_gpd_quick.py

# Test Vine (requires pyvinecop)
pip install pyvinecop
python test_vine_quick.py
```

For comprehensive tests:
```bash
pytest tests/test_gpd.py -v
pytest tests/test_vine.py -v
```

## Summary

Pyreto provides three complementary approaches to tail risk analysis:

1. **Single-asset distributions** (Student's T, NIG, Alpha-Stable): Fast and robust for individual assets
2. **GPD** (Peaks Over Threshold): Specialized for extreme value analysis and exceedances
3. **Vine Copulas**: Multi-asset dependence modeling with flexible correlation structures

Choose the appropriate tool based on your use case:
- Single asset: Use `pr.student_t` (fastest, recommended)
- Extreme values: Use `pr.gpd` for POT analysis
- Multi-asset portfolios: Use `pr.vine` for dependence modeling
- Comprehensive analysis: Combine all three approaches
"""
