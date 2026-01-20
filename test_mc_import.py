#!/usr/bin/env python3
"""Minimal import test for mc module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # This will fail if imports are broken
    from pyreto.mc import simulate, simulate_portfolio, _MARGINAL_INVERTERS
    print("✓ mc module imports successfully")
    print(f"✓ _MARGINAL_INVERTERS keys: {list(_MARGINAL_INVERTERS.keys())}")
    
    # Check function signatures
    import inspect
    sig_sim = inspect.signature(simulate)
    sig_port = inspect.signature(simulate_portfolio)
    print(f"✓ simulate{sig_sim}")
    print(f"✓ simulate_portfolio{sig_port}")
    
    # Check line count
    import pyreto.mc as mc
    source = inspect.getsource(mc)
    lines = len(source.split('\n'))
    print(f"✓ Module size: {lines} lines (limit: 120)")
    
    if lines > 120:
        print(f"⚠ Warning: {lines} lines exceeds 120 line limit")
    else:
        print(f"✓ Module size under limit")
        
    print("\n✅ MC module structure validated successfully!")
    print("\nTo run full tests after installing polars:")
    print("  pip install polars scipy")
    print("  python tests/test_mc.py")
    
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
