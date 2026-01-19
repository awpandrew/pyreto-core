"""Student's T distribution."""

import numpy as np
from scipy.stats import t as student_t
from scipy.integrate import quad
from .base import DistributionFitter


class StudentT(DistributionFitter):
    """Student's T distribution."""
    
    def fit(self) -> dict:
        """Fit using MLE. Returns dict with df, loc, scale."""
        df, loc, scale = student_t.fit(self.returns)
        self.params = {'df': df, 'loc': loc, 'scale': scale}
        return self.params
    
    def pdf(self, x: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        return student_t.pdf(x, **self.params)
    
    def cdf(self, x: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        return student_t.cdf(x, **self.params)
    
    def ppf(self, q: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        return student_t.ppf(q, **self.params)
    
    def es(self, alpha: float) -> float:
        if not (0 < alpha < 1):
            raise ValueError("Alpha must be between 0 and 1")
        if not self.params:
            self.fit()
        var = self.var(alpha)
        
        def integrand(x):
            return x * self.pdf(np.array([x]))[0]
        
        es_val, _ = quad(integrand, -np.inf, var)
        return es_val / alpha