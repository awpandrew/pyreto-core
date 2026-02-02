"""Pyreto: Tail risk management library with Monte Carlo simulation (classless functional API)."""

__version__ = "0.5.1"

# Make distributions available at pyreto.*
from .distributions import student_t
from .distributions import alpha_stable
from .distributions import nig
from .distributions import gpd
from . import mc
from . import vine
from . import bootstrap

# Import model registry
from .models import list_models, get_model_info, describe_model, models, ModelInfo

__all__ = [
    "student_t", "alpha_stable", "nig", "gpd", "mc", "vine", "bootstrap",
    "list_models", "get_model_info", "describe_model", "models", "ModelInfo"
]
