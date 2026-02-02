"""Tests for model registry functionality."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pyreto import list_models, get_model_info, describe_model, models, ModelInfo


class TestListModels:
    """Test list_models function."""
    
    def test_returns_list(self):
        """list_models returns a list."""
        result = list_models()
        assert isinstance(result, list)
    
    def test_contains_expected_models(self):
        """list_models includes expected distribution models."""
        result = list_models()
        assert "student_t" in result
        assert "alpha_stable" in result
        assert "nig" in result
        assert "gpd" in result
    
    def test_returns_strings(self):
        """All items in list are strings."""
        result = list_models()
        for model in result:
            assert isinstance(model, str)


class TestGetModelInfo:
    """Test get_model_info function."""
    
    def test_returns_model_info(self):
        """get_model_info returns ModelInfo object."""
        info = get_model_info("student_t")
        assert isinstance(info, ModelInfo)
    
    def test_student_t_params(self):
        """Student's T has correct parameters."""
        info = get_model_info("student_t")
        assert info.params == ["df", "loc", "scale"]
        assert "df" in info.param_descriptions
    
    def test_alpha_stable_params(self):
        """Alpha-Stable has correct parameters."""
        info = get_model_info("alpha_stable")
        assert info.params == ["alpha", "beta", "c", "mu"]
    
    def test_nig_params(self):
        """NIG has correct parameters."""
        info = get_model_info("nig")
        assert info.params == ["alpha", "beta", "delta", "mu", "gamma"]
    
    def test_gpd_params(self):
        """GPD has correct parameters."""
        info = get_model_info("gpd")
        assert info.params == ["c", "loc", "scale"]
    
    def test_invalid_model_raises_error(self):
        """Invalid model name raises ValueError."""
        with pytest.raises(ValueError):
            get_model_info("invalid_model")
    
    def test_error_includes_available_models(self):
        """Error message includes available models."""
        with pytest.raises(ValueError) as exc_info:
            get_model_info("unknown")
        error_msg = str(exc_info.value)
        assert "student_t" in error_msg
        assert "alpha_stable" in error_msg


class TestModelsRegistry:
    """Test models registry object."""
    
    def test_models_all(self):
        """models.all() returns list of models."""
        result = models.all()
        assert isinstance(result, list)
        assert "student_t" in result
    
    def test_models_info(self):
        """models.info() returns ModelInfo."""
        info = models.info("student_t")
        assert isinstance(info, ModelInfo)
        assert info.name == "Student's T"
    
    def test_models_attribute_access(self):
        """Can access models via attribute."""
        student = models.student_t
        assert student.params == ["df", "loc", "scale"]
        assert student.name == "Student's T"
    
    def test_models_attribute_invalid(self):
        """Invalid model attribute raises AttributeError."""
        with pytest.raises(AttributeError):
            _ = models.invalid_model
    
    def test_model_proxy_params(self):
        """Model proxy has params property."""
        assert models.gpd.params == ["c", "loc", "scale"]
    
    def test_model_proxy_description(self):
        """Model proxy has description property."""
        desc = models.nig.description
        assert isinstance(desc, str)
        assert len(desc) > 0
    
    def test_model_proxy_param_info(self):
        """Model proxy has param_info property."""
        param_info = models.alpha_stable.param_info
        assert isinstance(param_info, dict)
        assert "alpha" in param_info
    
    def test_model_proxy_functions(self):
        """Model proxy has functions property."""
        funcs = models.student_t.functions
        assert isinstance(funcs, list)
        assert "fit" in funcs
        assert "var" in funcs
        assert "es" in funcs


class TestModelInfoDataclass:
    """Test ModelInfo dataclass."""
    
    def test_model_info_creation(self):
        """Can create ModelInfo object."""
        info = ModelInfo(
            name="Test Model",
            description="A test model",
            params=["a", "b"],
            param_descriptions={"a": "Parameter A", "b": "Parameter B"},
            functions=["fit", "pdf"]
        )
        assert info.name == "Test Model"
        assert info.params == ["a", "b"]
    
    def test_model_info_repr(self):
        """ModelInfo has repr."""
        info = ModelInfo(
            name="Test",
            description="Test",
            params=["x"],
            param_descriptions={"x": "X"},
            functions=["fit"]
        )
        repr_str = repr(info)
        assert "ModelInfo" in repr_str
        assert "Test" in repr_str
