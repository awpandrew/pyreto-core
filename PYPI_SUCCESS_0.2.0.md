# ✅ Pyreto v0.2.0 Successfully Published on PyPI!

## 📦 Package Details

**Package:** https://pypi.org/project/pyreto/0.2.0/
**Version:** 0.2.0 (Suckless Edition)
**Status:** ✅ Live and Available

## 🎯 What's New in v0.2.0

### Suckless Philosophy
- **One function, one job**: `pyreto.dist.fit()` does exactly one thing
- **No bloat**: Removed all plotting, printing, ensemble methods
- **Fail loudly**: Immediate errors on invalid inputs
- **Plain returns**: Dicts and arrays only, no custom classes
- **Minimal dependencies**: Only numpy + scipy (polars optional)
- **480 lines total**: Ruthlessly minimal codebase

### API - One Function to Rule Them All
```python
pyreto.dist.fit(data, column=None, model='student_t')
```

**Arguments:**
- `data`: CSV path, polars DataFrame, numpy array, or list
- `column`: Column name (if CSV/DataFrame)
- `model`: 'student_t', 'alpha_stable', or 'nig'

**Returns:** Distribution object with methods:
- `.fit()` → dict (fit parameters)
- `.pdf(x)` → np.ndarray (density)
- `.cdf(x)` → np.ndarray (distribution)
- `.ppf(q)` → np.ndarray (quantile)
- `.var(alpha)` → float (Value at Risk)
- `.es(alpha)` → float (Expected Shortfall)
- `.params` → dict (fitted parameters)

## 📦 Installation

```bash
# Standard install
pip install pyreto==0.2.0

# With CSV support
pip install pyreto[polars]==0.2.0
```

## 🚀 Quick Start

```python
import pyreto
import numpy as np

# Generate test data
returns = np.random.standard_t(3, 1000) * 0.01

# Fit Student's T distribution
model = pyreto.dist.fit(returns, model='student_t')

# Get 5% tail risk metrics
var_5 = model.var(0.05)  # Value at Risk
es_5 = model.es(0.05)    # Expected Shortfall
params = model.params    # {'df': 3.12, 'loc': 0.001, 'scale': 0.008}

print(f"VaR(5%): {var_5:.4f}")
print(f"ES(5%): {es_5:.4f}")
```

## 📊 Three Models Available

### 1. Student's T (Recommended)
```python
model = pyreto.dist.fit(data, model='student_t')
# Fast, robust, good for most use cases
# Parameters: df, loc, scale
```

### 2. Alpha-Stable (Most Flexible)
```python
model = pyreto.dist.fit(data, model='alpha_stable')
# Handles extreme tails (alpha < 1)
# Parameters: alpha, beta, c, mu
# Slower but most general
```

### 3. Normal-Inverse Gaussian (NIG)
```python
model = pyreto.dist.fit(data, model='nig')
# Analytically tractable, good balance
# Parameters: alpha, beta, delta, mu
```

## 💥 Error Handling

```python
# Invalid alpha raises ValueError
model.var(1.5)   # ValueError: Alpha must be between 0 and 1
model.var(-0.1)  # ValueError: Alpha must be between 0 and 1

# Non-finite data raises ValueError
returns = [1, 2, np.nan, 4]
model = pyreto.dist.fit(returns)  # ValueError: Returns must be finite

# Empty data raises ValueError
model = pyreto.dist.fit([])  # ValueError: Returns cannot be empty
```

## 📂 File Structure

```
src/pyreto/
├── __init__.py (v0.2.0, exports fit function)
└── distributions/
    ├── __init__.py
    ├── base.py (abstract base class, 30 lines)
    ├── fit.py (load_returns + fit function, 80 lines)
    ├── student_t.py (Student's T, 50 lines)
    ├── alpha_stable.py (Alpha-Stable, 100 lines)
    └── normal_inverse_gaussian.py (NIG, 85 lines)
```

**Total: 7 files, ~480 lines of code**

## 📈 Usage Examples

### CSV Input
```python
model = pyreto.dist.fit('returns.csv', column='daily_return', 
                       model='student_t')
var = model.var(0.01)
```

### Polars DataFrame
```python
import polars as pl
df = pl.read_csv('returns.csv')
model = pyreto.dist.fit(df, column='returns', model='student_t')
```

### Numpy Array
```python
import numpy as np
returns = np.array([...])
model = pyreto.dist.fit(returns, model='student_t')
```

### Compare Models
```python
student = pyreto.dist.fit(data, model='student_t')
stable = pyreto.dist.fit(data, model='alpha_stable')
nig = pyreto.dist.fit(data, model='nig')

# Get most conservative VaR
var_student = student.var(0.01)
var_stable = stable.var(0.01)
var_nig = nig.var(0.01)
worst_var = min(var_student, var_stable, var_nig)
```

## 🔧 Dependencies

**Required:**
- `numpy>=1.20.0` (array operations)
- `scipy>=1.7.0` (optimization, integration, statistics)

**Optional:**
- `polars` (CSV/DataFrame support)

**No longer required (removed from v0.1.0):**
- matplotlib (no plotting)
- seaborn (no plotting)
- pandas (replaced with polars)

## 🏁 Distribution Files

```bash
dist/
├── pyreto-0.2.0-py3-none-any.whl (11.1 kB)
└── pyreto-0.2.0.tar.gz (9.5 kB)
```

**Size reduction**: 28.5 kB → 11.1 kB (61% smaller)

## 🎯 Version History

- **v0.1.0**: Full-featured with plotting, printing, ensembles
- **v0.2.0**: Suckless edition - minimal, focused, single-purpose

## 🔥 Key Improvements

| Feature | v0.1.0 | v0.2.0 |
|---------|--------|--------|
| Lines of code | ~1000+ | ~480 (52% reduction) |
| Runtime dependencies | 5+ | 2 (60% reduction) |
| API complexity | High (dicts of objects) | Low (single objects) |
| Error handling | Lenient | Strict (fail fast) |
| Philosophy | Batteries-included | Suckless |
| Distribution size | 28.5 kB | 11.1 kB (61% reduction) |

## ✨ TL;DR

```bash
pip install pyreto==0.2.0
```

```python
import pyreto
model = pyreto.dist.fit('returns.csv', model='student_t')
var = model.var(0.05)
es = model.es(0.05)
```

**6 lines. 3 imports. 2 dependencies. Zero bloat.**

Package is live at: https://pypi.org/project/pyreto/0.2.0/