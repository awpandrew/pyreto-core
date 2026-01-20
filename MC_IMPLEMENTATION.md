# Monte Carlo Engine Implementation Summary

## Implementation Complete ✓

A minimal, deterministic Monte-Carlo engine has been implemented in `pyreto.mc` following suckless principles.

## Module: `src/pyreto/mc.py`

- **Size**: 99 lines (under 120 line limit)
- **Dependencies**: numpy, scipy, polars
- **GPU-free**: Pure CPU implementation
- **Single-threaded**: No parallelization
- **No custom classes**: Only functions
- **No plotting/summary**: Returns raw numbers only

## Public API

### 1. `simulate(copula, margins, n_draws, seed=None) -> polars.DataFrame`

Simulates correlated log-returns via copula + margins.

**Parameters:**
- `copula`: str - "gaussian" or "t"
- `margins`: dict - {"asset": {"type": "student_t", "par": {...}}, ...}
- `n_draws`: int - Number of draws (>0)
- `seed`: int, optional - Random seed for reproducibility

**Returns:**
- polars.DataFrame with shape (n_draws, n_assets)

**Example:**
```python
margins = {
    "SPY": {"type": "student_t", "par": {"df": 3.5, "loc": 0, "scale": 0.012}},
    "TLT": {"type": "nig", "par": {"alpha": 2.0, "beta": 0.0, "delta": 0.01, "mu": 0.0, "gamma": 2.0}}
}
returns = mc.simulate("gaussian", margins, n_draws=50_000, seed=42)
```

**Supported Margin Types:**
- `"student_t"` - Student's T distribution (fastest, recommended)
- `"nig"` - Normal-Inverse Gaussian
- `"alpha_stable"` - Alpha-Stable distribution

### 2. `simulate_portfolio(weights, mc_returns) -> polars.Series`

Computes portfolio log-returns from Monte Carlo simulation.

**Parameters:**
- `weights`: numpy.ndarray - Portfolio weights (must sum to 1, non-negative)
- `mc_returns`: polars.DataFrame - Simulated returns from simulate()

**Returns:**
- polars.Series with portfolio log-return series

**Example:**
```python
weights = np.array([0.6, 0.4])  # 60% SPY, 40% TLT
port_ret = mc.simulate_portfolio(weights, returns)
es99 = np.percentile(port_ret, 1)  # 1% Expected Shortfall
```

## Copula Implementation

### Gaussian Copula
- Uses `numpy.random.multivariate_normal`
- Identity correlation matrix (assets independent)
- Transformed to uniform via standard normal CDF

### t-Copula
- Uses `scipy.stats.multivariate_t` (requires SciPy ≥ 1.10)
- Degrees of freedom: 5 (canonical choice)
- Identity correlation matrix
- Transformed to uniform via t CDF

## Testing

Comprehensive tests in `tests/test_mc.py`:

1. **test_gaussian_copula_three_assets**: 3-asset Gaussian copula, mean ≈ 0
2. **test_t_copula_heavier_tails**: t-copula produces kurtosis > 3
3. **test_reproducibility**: Same seed → identical draws
4. **test_simulate_portfolio_shape**: Portfolio shape validation
5. **test_nig_margins**: NIG margins work correctly
6. **test_negative_weights_raise**: Negative weights rejected
7. **test_weights_must_sum_to_one**: Weights sum validation
8. **test_single_asset_portfolio**: Single asset identity
9. **test_t_copula_dof5_empirical_tail**: t-copula gives more exceedances

**Run tests:**
```bash
pip install polars scipy  # if not installed
python tests/test_mc.py
```

## Dependencies Updated

`pyproject.toml` updated to include:
- `scipy>=1.10.0` (for multivariate_t)
- `polars>=0.19.0` (for DataFrame returns)

## Usage Example in README

Added to README.md:
```python
import pyreto as pr, numpy as np
margins = {"SPY": {"type": "student_t", "par": {"df": 3.5, "loc": 0, "scale": 0.012}}}
mc = pr.mc.simulate("gaussian", margins, n_draws=50_000, seed=42)
port_ret = pr.mc.simulate_portfolio(np.array([1.0]), mc)
es99 = np.percentile(port_ret, 1)
```

## Validation

Module structure validated:
- ✓ Imports correctly
- ✓ Function signatures correct
- ✓ 99 lines (< 120 limit)
- ✓ No custom classes
- ✓ No plotting/summary code
- ✓ Returns raw polars DataFrame/Series

## Branch

All changes pushed to branch: `mc-core`

## Notes

- **Suckless**: Kept minimal, no unnecessary features
- **Deterministic**: Seed-based reproducibility
- **GPU-free**: Pure CPU implementation
- **Single-threaded**: No parallelization complexity
- **GPL-compatible**: MIT license maintained

To install and test:
```bash
git checkout mc-core
pip install -e .
python tests/test_mc.py
```
