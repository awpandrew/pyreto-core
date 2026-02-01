"""Unit tests for Student's T distribution - validation only."""

import pytest
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pyreto import student_t


class TestStudentTValidation:
    """Test Student's T input validation only (not the math)."""
    
    def test_fit_validation_empty_array(self):
        """Test that fit raises error for empty array."""
        with pytest.raises(ValueError, match="Returns cannot be empty"):
            student_t.fit([])
    
    def test_fit_validation_nan_values(self):
        """Test that fit raises error for NaN values."""
        returns = [0.01, np.nan, 0.02]
        with pytest.raises(ValueError, match="Returns must be finite"):
            student_t.fit(returns)
    
    def test_fit_validation_inf_values(self):
        """Test that fit raises error for Inf values."""
        returns = [0.01, np.inf, 0.02]
        with pytest.raises(ValueError, match="Returns must be finite"):
            student_t.fit(returns)


class TestStudentTParameterValidation:
    """Test parameter validation in Student's T functions."""
    
    def test_var_alpha_validation(self):
        """Test that var validates alpha parameter."""
        par = {'df': 5.0, 'loc': 0.0, 'scale': 0.02}
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            student_t.var(1.5, par)
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            student_t.var(-0.1, par)
    
    def test_es_alpha_validation(self):
        """Test that es validates alpha parameter."""
        par = {'df': 5.0, 'loc': 0.0, 'scale': 0.02}
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            student_t.es(1.5, par)
        
        with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
            student_t.es(-0.1, par)
