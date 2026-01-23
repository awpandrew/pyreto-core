#!/usr/bin/env python3
"""Quick test for bootstrap implementation."""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np
import pyreto as pr

print("Testing bootstrap implementation...")
print("=" * 60)

# Test 1: Basic functionality
print("\n1. Testing basic blocks() functionality...")
try:
    returns = np.random.normal(0, 0.02, 100)
    boot = pr.bootstrap.blocks(returns, n_draws=10, method="circular", seed=42)
    print(f"✓ Circular bootstrap successful, shape: {boot.shape}")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n2. Testing stationary bootstrap...")
try:
    returns = np.random.normal(0, 0.02, 100)
    boot = pr.bootstrap.blocks(returns, n_draws=10, method="stationary", seed=42)
    print(f"✓ Stationary bootstrap successful, shape: {boot.shape}")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n3. Testing es_conf()...")
try:
    returns = np.random.normal(0, 0.02, 500)
    conf = pr.bootstrap.es_conf(returns, alpha=0.05, n_draws=100, method="circular", seed=42)
    print(f"✓ ES confidence successful: {conf}")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n4. Testing speed requirement...")
try:
    returns = np.random.normal(0, 0.02, 1000)
    start = time.time()
    boot = pr.bootstrap.blocks(returns, n_draws=10_000, method="circular", seed=42)
    elapsed = time.time() - start
    print(f"✓ Speed test: {elapsed*1000:.0f} ms (need <300 ms)")
    if elapsed > 0.3:
        print(f"⚠ WARNING: Too slow for requirement!")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n5. Testing seed reproducibility...")
try:
    returns = np.random.normal(0, 0.02, 100)
    boot1 = pr.bootstrap.blocks(returns, n_draws=10, method="circular", seed=42)
    boot2 = pr.bootstrap.blocks(returns, n_draws=10, method="circular", seed=42)
    
    if (boot1["draw_0"] == boot2["draw_0"]).all():
        print(f"✓ Seed reproducibility verified")
    else:
        print(f"✗ Seed reproducibility failed")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "=" * 60)
print("Quick bootstrap tests completed!")
print("=" * 60)
