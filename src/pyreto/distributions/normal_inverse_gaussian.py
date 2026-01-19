"""Normal-Inverse Gaussian distribution."""

import numpy as np
from scipy.optimize import minimize
from scipy.special import kv as bessel_k
from scipy.integrate import quad
from scipy.optimize import brentq
from .base import DistributionFitter


class NormalInverseGaussian(DistributionFitter):
    """Normal-Inverse Gaussian distribution."""
    
    def _pdf(self, x, alpha, beta, delta, mu):
        gamma = np.sqrt(alpha**2 - beta**2)
        z = (x - mu) / delta
        factor = alpha * delta * np.sqrt(1 + z**2)
        numerator = alpha * delta * bessel_k(1, factor)
        denominator = np.pi * np.sqrt(1 + z**2)
        return (numerator / denominator) * np.exp(delta * gamma + beta * (x - mu))
    
    def fit(self) -> dict:
        """Fit using MLE. Returns dict with alpha, beta, delta, mu."""
        def neg_loglik(params):
            alpha, beta, delta, mu = params
            if alpha <= 0 or delta <= 0 or abs(beta) >= alpha:
                return 1e10
            try:
                pdf_vals = self._pdf(self.returns, alpha, beta, delta, mu)
                return -np.sum(np.log(pdf_vals))
            except:
                return 1e10
        
        mu0 = np.mean(self.returns)
        delta0 = np.std(self.returns) * 0.8
        alpha0 = 2.0
        beta0 = 0.0
        x0 = np.array([alpha0, beta0, delta0, mu0])
        bounds = [(1e-4, 50), (-49, 49), (1e-4, 50), (None, None)]
        
        res = minimize(neg_loglik, x0, method='SLSQP', bounds=bounds,
                      options={'ftol': 1e-8, 'maxiter': 1000})
        
        alpha, beta, delta, mu = res.x
        self.params = {'alpha': alpha, 'beta': beta, 'delta': delta, 'mu': mu, 
                      'gamma': np.sqrt(alpha**2 - beta**2)}
        return self.params
    
    def pdf(self, x: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        return self._pdf(x, **{k: self.params[k] for k in ['alpha', 'beta', 'delta', 'mu']})
    
    def cdf(self, x: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        results = np.zeros_like(x)
        for i, xi in enumerate(x):
            results[i], _ = quad(lambda xx: self.pdf(np.array([xx]))[0], -np.inf, xi)
        return results
    
    def ppf(self, q: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        results = np.zeros_like(q)
        for i, qi in enumerate(q):
            def f(x):
                return self.cdf(np.array([x]))[0] - qi
            results[i] = brentq(f, -10, 10)
        return results
    
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