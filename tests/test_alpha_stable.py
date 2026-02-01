"""Unit tests for Alpha-Stable distribution - validation only."""

import pytest
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pyreto import alpha_stable


class TestAlphaStableValidation:
    """Test Alpha-Stable input validation only (not the math)."""
    
    def test_fit_validation_empty_array(self):
        """Test that fit raises error for empty array."""
        with pytest.raises(ValueError, match="Returns cannot be empty"):
            alpha_stable.fit([])
    
    def test_fit_validation_nan_values(self):
        """Test that fit raises error for NaN values."""
        returns = [0.01, np.nan, 0.02]
        with pytest.raises(ValueError, match="Returns must be finite"):
            alpha_stable.fit(returns)
    
    def test_fit_validation_inf_values(self):
        """Test that fit raises error for Inf values."""
        returns = [0.01, np.inf, 0.02]
        with pytest.raises(ValueError, match="Returns must be finite"):
            alpha_stable.fit(returns)


class TestAlphaStableParameterValidation:
    """Test parameter validation in Alpha-Stable functions."""
    
    def test_var_alpha_validation(self):
        """Test that var validates alpha parameter."""
        par = {'alpha': 1.8, 'beta': 0.1, 'c': 0.02, 'mu': 0.0}
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            alpha_stable.var(1.5, par)
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            alpha_stable.var(-0.1, par)
    
    def test_es_alpha_validation(self):
        """Test that es validates alpha parameter."""
        par = {'alpha': 1.8, 'beta': 0.1, 'c': 0.02, 'mu': 0.0}
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            alpha_stable.es(1.5, par)
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            alpha_stable.es(-0.1, par)
