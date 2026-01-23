#!/usr/bin/env python3
"""Quick test for vine copula implementation."""

import sys
sys.path.insert(0, 'src')

import numpy as np
import polars as pl
import scipy.stats as stats
import pyreto as pr

print("Testing vine copula implementation...")
print("=" * 60)

# Test 1: Basic fit
print("\n1. Testing vine.fit()...")
np.random.seed(42)
rho = 0.7
cov = np.array([[1, rho, 0.5], [rho, 1, 0.3], [0.5, 0.3, 1]])
z = np.random.multivariate_normal(mean=[0, 0, 0], cov=cov, size=500)
u = 1 - stats.norm.cdf(z)
df = pl.DataFrame(u, schema=["SPY", "TLT", "VIX"])

try:
    vine_dict = pr.vine.fit(df, family_set=["gumbel", "t"], method="mle")
    print(f"✓ Fit successful")
    print(f"  Trees: {len(vine_dict['trees'])}")
    print(f"  AIC: {vine_dict['aic']:.2f}")
    print(f"  LogLik: {vine_dict['loglik']:.2f}")
except Exception as e:
    print(f"✗ Fit failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Simulate
print("\n2. Testing vine.simulate()...")
try:
    sim = pr.vine.simulate(vine_dict, n_draws=5_000, seed=123)
    print(f"✓ Simulate successful")
    print(f"  Shape: {sim.shape}")
    print(f"  Columns: {sim.columns}")
    print(f"  Min: {sim.min().min():.4f}, Max: {sim.max().max():.4f}")
except Exception as e:
    print(f"✗ Simulate failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Upper tail dependence
print("\n3. Testing vine.upper_tail_dependence()...")
try:
    lambda_u = pr.vine.upper_tail_dependence(vine_dict, pair=("asset_0", "asset_2"))
    print(f"✓ Upper tail dependence successful")
    print(f"  λ_U(SPY,VIX): {lambda_u:.3f}")
except Exception as e:
    print(f"✗ Upper tail dependence failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Reproducibility
print("\n4. Testing reproducibility...")
try:
    s1 = pr.vine.simulate(vine_dict, n_draws=1_000, seed=99)
    s2 = pr.vine.simulate(vine_dict, n_draws=1_000, seed=99)
    if (s1["asset_0"] == s2["asset_0"]).all():
        print(f"✓ Reproducibility verified")
    else:
        print(f"✗ Reproducibility failed")
except Exception as e:
    print(f"✗ Reproducibility test failed: {e}")

print("\n" + "=" * 60)
print("Vine copula tests completed!")
