#!/usr/bin/env python3
"""Test the IndexError fix for var() function."""

import sys
sys.path.insert(0, 'src')

import pyreto as pr
import numpy as np

# Sample returns data
np.random.seed(42)
returns = np.random.normal(0, 0.02, 100)

print("Testing var() function fix...")
print("=" * 50)

# Test all three distributions
distros = [
    ("Student's T", pr.student_t),
    ("Alpha-Stable", pr.alpha_stable),
    ("NIG", pr.nig)
]

for name, distro in distros:
    print(f"\n{name}:")
    try:
        # Fit the model
        par = distro.fit(returns)
        print(f"  ✓ Fit successful: {type(par).__name__}")
        
        # Test var() with scalar alpha (this was causing IndexError)
        var = distro.var(0.05, par)
        print(f"  ✓ var(0.05) = {var:.6f}")
        
        # Test es() too
        es = distro.es(0.05, par)
        print(f"  ✓ es(0.05) = {es:.6f}")
        
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("All tests completed!")
