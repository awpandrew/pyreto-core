#!/usr/bin/env python3
"""Quick test for GPD implementation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from pyreto import gpd


def test_fit():
    """Test GPD fitting."""
    np.random.seed(42)
    returns = np.random.standard_t(3, 500) * 0.01
    threshold = np.percentile(returns, 95)
    exceedances = returns[returns > threshold] - threshold

    par = gpd.fit(exceedances)

    assert isinstance(par, dict)
    assert 'c' in par and 'loc' in par and 'scale' in par
    assert par['scale'] > 0
    print("✓ Test fit passed")


def test_var_es():
    """Test VaR and ES calculation."""
    np.random.seed(42)
    returns = np.random.standard_t(3, 500) * 0.01
    threshold = np.percentile(returns, 95)
    exceedances = returns[returns > threshold] - threshold
    par = gpd.fit(exceedances)

    for alpha in [0.1, 0.05, 0.01]:
        var = gpd.var(alpha, par)
        es = gpd.es(alpha, par)

        assert isinstance(var, float)
        assert isinstance(es, float)
        assert np.isfinite(var)
        assert np.isfinite(es)

    print("✓ Test var/es passed")


def test_pdf_cdf_ppf():
    """Test PDF, CDF, and PPF."""
    np.random.seed(42)
    returns = np.random.standard_t(3, 500) * 0.01
    threshold = np.percentile(returns, 95)
    exceedances = returns[returns > threshold] - threshold
    par = gpd.fit(exceedances)

    # Test scalar inputs
    pdf_val = gpd.pdf(0.01, par)
    cdf_val = gpd.cdf(0.01, par)
    ppf_val = gpd.ppf(0.5, par)

    assert isinstance(pdf_val, np.ndarray)
    assert isinstance(cdf_val, np.ndarray)
    assert isinstance(ppf_val, np.ndarray)
    assert pdf_val.shape == (1,)
    assert cdf_val.shape == (1,)
    assert ppf_val.shape == (1,)

    # Test roundtrip
    assert np.isclose(gpd.cdf(gpd.ppf(0.5, par), par)[0], 0.5, rtol=1e-5)

    print("✓ Test pdf/cdf/ppf passed")


def test_special_cases():
    """Test special cases (exponential, heavy tail, bounded)."""
    # Exponential case (c=0)
    par_exp = {'c': 0.0, 'loc': 0.0, 'scale': 1.0}
    var = gpd.var(0.05, par_exp)
    es = gpd.es(0.05, par_exp)
    assert isinstance(var, float) and np.isfinite(var)
    print("✓ Test exponential case passed")

    # Heavy tail (c>0)
    par_heavy = {'c': 0.3, 'loc': 0.0, 'scale': 1.0}
    var = gpd.var(0.05, par_heavy)
    es = gpd.es(0.05, par_heavy)
    assert isinstance(var, float) and np.isfinite(var)
    print("✓ Test heavy tail case passed")

    # Bounded tail (c<0)
    par_bounded = {'c': -0.3, 'loc': 0.0, 'scale': 1.0}
    var = gpd.var(0.05, par_bounded)
    es = gpd.es(0.05, par_bounded)
    assert isinstance(var, float) and np.isfinite(var)
    print("✓ Test bounded case passed")


def test_validation():
    """Test input validation."""
    # Test empty array
    try:
        gpd.fit([])
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test empty validation passed")

    # Test NaN values
    try:
        gpd.fit([0.01, np.nan, 0.02])
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Test NaN validation passed")


if __name__ == "__main__":
    print("=" * 60)
    print("GPD Quick Tests")
    print("=" * 60)

    test_fit()
    test_var_es()
    test_pdf_cdf_ppf()
    test_special_cases()
    test_validation()

    print("=" * 60)
    print("All GPD quick tests passed!")
    print("=" * 60)
