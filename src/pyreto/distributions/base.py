"""Base class for distribution fitters."""

import numpy as np
from abc import ABC, abstractmethod


class DistributionFitter(ABC):
    """Abstract base class for distribution fitting."""
    
    def __init__(self, returns: np.ndarray):
        returns = np.array(returns, dtype=np.float64).flatten()
        if not np.isfinite(returns).all():
            raise ValueError("Returns must be finite (no NaN or Inf)")
        if len(returns) == 0:
            raise ValueError("Returns cannot be empty")
        self.returns = returns
        self.params = {}
    
    @abstractmethod
    def fit(self) -> dict:
        """Fit distribution and return parameters."""
        pass
    
    @abstractmethod
    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Probability density function."""
        pass
    
    @abstractmethod
    def cdf(self, x: np.ndarray) -> np.ndarray:
        """Cumulative distribution function."""
        pass
    
    @abstractmethod
    def ppf(self, q: np.ndarray) -> np.ndarray:
        """Percent point function (inverse CDF)."""
        pass
    
    @abstractmethod
    def es(self, alpha: float) -> float:
        """Expected Shortfall at significance level alpha."""
        pass
    
    def var(self, alpha: float) -> float:
        """Value at Risk (quantile) at significance level alpha."""
        if not (0 < alpha < 1):
            raise ValueError("Alpha must be between 0 and 1")
        return self.ppf(np.array([alpha]))[0]