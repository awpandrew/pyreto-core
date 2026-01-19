# Pyreto Suckless Refactor - Summary

## 🎯 Philosophy
Ruthlessly minimal tail risk management library:
- Each function does **one thing**
- **No auto**, **no ensemble**, **no plot**
- **Fail loudly** on invalid inputs
- Return **plain dicts/arrays**
- **Single responsibility** throughout

## 📦 Installation

```bash
pip install pyreto
# Dependencies: numpy, scipy
# Optional: polars (for CSV/DataFrame support)
```

## 🚀 API Surface

### Main Function
```python
pyreto.dist.fit(data, column=None, model='student_t') → DistributionFitter
```
**Parameters:**
- `data`: CSV path, polars DataFrame, numpy array, or list
- `column`: Column name (for CSV/DataFrame)
- `model`: 'student_t', 'alpha_stable', or 'nig'

**Returns:** Fitted distribution object

### Distribution Methods (All Models)
```python
model.fit() → dict                    # Fit parameters
model.pdf(x) → np.ndarray            # Density function
model.cdf(x) → np.ndarray            # Distribution function  
model.ppf(q) → np.ndarray            # Quantile function
model.var(alpha) → float             # Value at Risk (0 < alpha < 1)
model.es(alpha) → float              # Expected Shortfall
model.params → dict                  # Fitted parameters
```

## 🎲 Models

### 1. StudentT (Recommended)
- **Fast** and **robust**
- Parameters: `df`, `loc`, `scale`
- Use for: Everyday risk measurement

### 2. AlphaStable (Most Flexible)  
- **Extreme tails** (alpha < 1)
- Parameters: `alpha`, `beta`, `c`, `mu`
- Use for: Crisis scenarios

### 3. NormalInverseGaussian (NIG)
- **Analytically tractable**
- Parameters: `alpha`, `beta`, `delta`, `mu`
- Use for: Good middle ground

## 💥 Error Handling

```python
# All invalid inputs raise ValueError
model.var(1.5)           # ValueError: Alpha must be between 0 and 1
model.var(-0.1)          # ValueError: Alpha must be between 0 and 1

model.es(0.05)           # OK
model.es(0)              # ValueError: Alpha must be between 0 and 1
```

## 📊 Usage Examples

### Basic Usage
```python
import pyreto
import numpy as np

# From CSV
model = pyreto.dist.fit('returns.csv', column='daily_return', 
                       model='student_t')

# From numpy array
returns = np.random.standard_t(3, 1000) * 0.01
model = pyreto.dist.fit(returns, model='student_t')

# Calculate risk
var_5 = model.var(0.05)    # 5% VaR
es_5 = model.es(0.05)      # 5% ES
params = model.params      # {'df': 3.2, 'loc': 0.001, 'scale': 0.008}
```

### Compare Models
```python
# Fit different models
student = pyreto.dist.fit(returns, model='student_t')
stable = pyreto.dist.fit(returns, model='alpha_stable')
nig = pyreto.dist.fit(returns, model='nig')

# Compare VaR
var_student = student.var(0.01)
var_stable = stable.var(0.01)
var_nig = nig.var(0.01)

# Choose most conservative
worst_var = min(var_student, var_stable, var_nig)
```

## 📁 File Structure

```
pyreto-lib/
├── .gitignore
├── pyproject.toml          # Minimal dependencies (numpy, scipy)
├── README.md               # One-page documentation
└── src/
    └── pyreto/
        ├── __init__.py
        └── distributions/
            ├── __init__.py
            ├── base.py                    # Minimal abstract base
            ├── fit.py                     # Single fit function
            ├── student_t.py               # Student's T implementation
            ├── alpha_stable.py            # Alpha stable implementation
            └── normal_inverse_gaussian.py # NIG implementation
```

## 📉 Statistics

- **Lines of code**: ~480 (down from ~1000+)
- **Dependencies**: 2 (down from 5+)
- **Runtime deps**: numpy, scipy only
- **API functions**: 1 main + 6 methods per model
- **Output**: Plain dicts/arrays only
- **Branches**: Each function has single responsibility
- **Error handling**: Loud failures, clear messages

## 🔄 Migration from v0.1.0

### Old (bloated)
```python
# Auto-fits everything, prints tons of output, generates plots
result = pyreto.dist.fit('returns.csv', column='returns')
result['print_summary']()  # Walls of text
result['comparison'].plot_comparison()  # Fancy plots
```

### New (suckless)
```python
# You decide what to fit and what to calculate
model = pyreto.dist.fit('returns.csv', column='returns', 
                       model='student_t')
var = model.var(0.05)  # Just what you need
```

## ✅ What's Gone

- ❌ **Plots** (matplotlib, seaborn)
- ❌ **Printing** (no summary prose, no tables)
- ❌ **Ensemble methods** (no auto-model-selection)
- ❌ **Pandas dependency** (use polars for CSV)
- ❌ **Synthetic data generation**
- ❌ **Multiple model fitting at once**
- ❌ **Complex comparison framework**
- ❌ **AIC/BIC metrics** (not essential)
- ❌ **99% of documentation**

## 🎯 Use Cases

### When to Use Suckless Version
- You know **exactly** what model you want
- You need **programmatic access** to risk metrics  
- You're **building** on top of pyreto
- You want **minimal dependencies**
- You prefer **explicit over implicit**
- You need **speed and simplicity**

### When NOT to Use This
- You want **out-of-the-box visualizations**
- You need **ensemble/consensus models**
- You want **automatic model selection**
- You prefer **batteries-included** libraries

## 🧪 Testing

```bash
# Install in virtual environment
uv venv
source .venv/bin/activate  
uv pip install numpy scipy polars

# Test manually
python -c "
import numpy as np
import pyreto
returns = np.random.standard_t(3, 1000) * 0.01
model = pyreto.dist.fit(returns, model='student_t')
print('VaR(5%):', model.var(0.05))
print('ES(5%):', model.es(0.05))
"
```

## 🏁 Summary

**Suckless pyreto** = 
- One fit function
- Six methods per model  
- Three models
- Zero magic
- Zero bloat

**Install**: `pip install pyreto`  
**Branch**: `suckless`  
**Version**: 0.2.0
