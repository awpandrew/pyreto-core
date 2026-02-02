"""Model registry for pyreto distributions.

Provides metadata and parameter information for all available models.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Information about a distribution model."""
    name: str
    description: str
    params: List[str]
    param_descriptions: Dict[str, str]
    functions: List[str]
    
    def __repr__(self):
        return f"ModelInfo(name='{self.name}', params={self.params})"


# Registry of all distribution models
_MODELS: Dict[str, ModelInfo] = {
    "student_t": ModelInfo(
        name="Student's T",
        description="Student's t-distribution - heavy tails, good for financial returns",
        params=["df", "loc", "scale"],
        param_descriptions={
            "df": "Degrees of freedom (>0). Lower values = heavier tails",
            "loc": "Location parameter (mean)",
            "scale": "Scale parameter (spread)"
        },
        functions=["fit", "pdf", "cdf", "ppf", "var", "es", "rvs"]
    ),
    "alpha_stable": ModelInfo(
        name="Alpha-Stable",
        description="Alpha-stable distribution - flexible heavy tails, skewness",
        params=["alpha", "beta", "c", "mu"],
        param_descriptions={
            "alpha": "Stability index (0,2]. alpha=2 is Gaussian",
            "beta": "Skewness parameter [-1,1]. 0 = symmetric",
            "c": "Scale parameter (>0)",
            "mu": "Location parameter"
        },
        functions=["fit", "pdf", "cdf", "ppf", "var", "es", "rvs"]
    ),
    "nig": ModelInfo(
        name="Normal-Inverse Gaussian",
        description="NIG distribution - semi-heavy tails, analytically tractable",
        params=["alpha", "beta", "delta", "mu", "gamma"],
        param_descriptions={
            "alpha": "Tail heaviness parameter (>|beta|)",
            "beta": "Skewness parameter (-alpha, alpha)",
            "delta": "Scale parameter (>0)",
            "mu": "Location parameter",
            "gamma": "sqrt(alpha^2 - beta^2), derived parameter"
        },
        functions=["fit", "pdf", "cdf", "ppf", "var", "es", "rvs"]
    ),
    "gpd": ModelInfo(
        name="Generalized Pareto",
        description="GPD - Peaks Over Threshold for extreme value analysis",
        params=["c", "loc", "scale"],
        param_descriptions={
            "c": "Shape parameter. c>0 = heavy tail, c<0 = bounded",
            "loc": "Location/threshold parameter",
            "scale": "Scale parameter (>0)"
        },
        functions=["fit", "pdf", "cdf", "ppf", "var", "es", "rvs"]
    )
}


def list_models() -> List[str]:
    """List all available distribution models.
    
    Returns
    -------
    list of str
        Names of available models
        
    Examples
    --------
    >>> import pyreto as pr
    >>> pr.list_models()
    ['student_t', 'alpha_stable', 'nig', 'gpd']
    """
    return list(_MODELS.keys())


def get_model_info(model_name: str) -> ModelInfo:
    """Get information about a specific model.
    
    Parameters
    ----------
    model_name : str
        Name of the model (e.g., 'student_t', 'alpha_stable')
        
    Returns
    -------
    ModelInfo
        Information about the model including parameters and descriptions
        
    Raises
    ------
    ValueError
        If model_name is not found
        
    Examples
    --------
    >>> import pyreto as pr
    >>> info = pr.get_model_info('student_t')
    >>> info.params
    ['df', 'loc', 'scale']
    >>> info.param_descriptions['df']
    'Degrees of freedom (>0). Lower values = heavier tails'
    """
    if model_name not in _MODELS:
        available = ", ".join(list_models())
        raise ValueError(f"Unknown model '{model_name}'. Available: {available}")
    return _MODELS[model_name]


def describe_model(model_name: str) -> None:
    """Print a formatted description of a model.
    
    Parameters
    ----------
    model_name : str
        Name of the model to describe
        
    Examples
    --------
    >>> import pyreto as pr
    >>> pr.describe_model('student_t')
    """
    info = get_model_info(model_name)
    print(f"\n{'='*60}")
    print(f"Model: {info.name}")
    print(f"{'='*60}")
    print(f"\nDescription: {info.description}")
    print(f"\nParameters:")
    for param in info.params:
        desc = info.param_descriptions.get(param, "No description")
        print(f"  • {param}: {desc}")
    print(f"\nAvailable functions: {', '.join(info.functions)}")
    print(f"{'='*60}\n")


class ModelRegistry:
    """Registry providing access to all pyreto models and their metadata.
    
    This class provides a convenient interface to access model information
    and can be used interactively to explore available distributions.
    
    Examples
    --------
    >>> import pyreto as pr
    >>> pr.models.all()
    ['student_t', 'alpha_stable', 'nig', 'gpd']
    
    >>> pr.models.student_t.params
    ['df', 'loc', 'scale']
    
    >>> pr.models.student_t.describe()
    # Prints formatted description
    """
    
    def all(self) -> List[str]:
        """List all available models."""
        return list_models()
    
    def info(self, model_name: str) -> ModelInfo:
        """Get information about a specific model.
        
        Parameters
        ----------
        model_name : str
            Name of the model
            
        Returns
        -------
        ModelInfo
            Model information object
        """
        return get_model_info(model_name)
    
    def describe(self, model_name: str) -> None:
        """Print formatted description of a model.
        
        Parameters
        ----------
        model_name : str
            Name of the model to describe
        """
        describe_model(model_name)
    
    def __getattr__(self, name: str) -> '_ModelProxy':
        """Allow access to models via attribute (e.g., pr.models.student_t)."""
        if name in _MODELS:
            return _ModelProxy(name)
        raise AttributeError(f"Model '{name}' not found. Available: {self.all()}")
    
    def __repr__(self) -> str:
        models = self.all()
        return f"ModelRegistry(models={models})"


class _ModelProxy:
    """Proxy object providing access to model metadata."""
    
    def __init__(self, model_name: str):
        self._name = model_name
        self._info = get_model_info(model_name)
    
    @property
    def name(self) -> str:
        """Full name of the model."""
        return self._info.name
    
    @property
    def description(self) -> str:
        """Description of the model."""
        return self._info.description
    
    @property
    def params(self) -> List[str]:
        """List of parameter names."""
        return self._info.params
    
    @property
    def param_info(self) -> Dict[str, str]:
        """Dictionary mapping parameter names to descriptions."""
        return self._info.param_descriptions
    
    @property
    def functions(self) -> List[str]:
        """List of available functions for this model."""
        return self._info.functions
    
    def describe(self) -> None:
        """Print a formatted description of this model."""
        describe_model(self._name)
    
    def __repr__(self) -> str:
        return f"Model(name='{self._name}', params={self.params})"


# Create singleton registry instance
models = ModelRegistry()
