"""Alpha-Stable distribution."""

import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm
from .base import DistributionFitter


class AlphaStable(DistributionFitter):
    """Alpha-Stable distribution."""
    
    def _char_func(self, t, alpha, beta, c, mu):
        if alpha == 1:
            return np.exp(1j * mu * t - c * np.abs(t) * (1 + 1j * beta * np.sign(t) * np.log(np.abs(t))))
        else:
            return np.exp(1j * mu * t - c**alpha * np.abs(t)**alpha * 
                         (1 - 1j * beta * np.sign(t) * np.tan(np.pi * alpha / 2)))
    
    def _pdf(self, x, alpha, beta, c, mu):
        if alpha == 2.0:
            return norm.pdf(x, loc=mu, scale=c)
        
        t = np.linspace(-50, 50, 1024)
        x = np.atleast_1d(x)
        results = np.zeros_like(x)
        
        for i, xi in enumerate(x):
            cf = self._char_func(t, alpha, beta, c, mu - xi)
            dt = t[1] - t[0]
            cf_sym = np.concatenate([cf, np.conj(cf[-1:0:-1])])
            pdf_component = np.fft.ifft(cf_sym).real[:len(t)] * len(t) / (2 * np.pi)
            results[i] = np.abs(pdf_component[0])
        
        return np.maximum(results, 1e-10)
    
    def fit(self) -> dict:
        """Fit using MLE. Returns dict with alpha, beta, c, mu."""
        def neg_loglik(params):
            alpha, beta, c, mu = params
            if not (0.1 < alpha <= 2.0) or not (-1 <= beta <= 1) or c <= 0:
                return 1e10
            try:
                pdf_vals = self._pdf(self.returns, alpha, beta, c, mu)
                if np.any(pdf_vals <= 0):
                    return 1e10
                return -np.sum(np.log(pdf_vals))
            except:
                return 1e10
        
        mu0 = np.mean(self.returns)
        c0 = np.std(self.returns) / np.sqrt(2)
        alpha0 = 1.8
        beta0 = 0.0
        x0 = np.array([alpha0, beta0, c0, mu0])
        bounds = [(0.1, 2.0), (-0.999, 0.999), (1e-6, 10.0), (None, None)]
        
        res = minimize(neg_loglik, x0, method='Nelder-Mead',
                      options={'maxiter': 500, 'xatol': 1e-6, 'fatol': 1e-6})
        
        alpha, beta, c, mu = res.x
        self.params = {'alpha': alpha, 'beta': beta, 'c': c, 'mu': mu}
        return self.params
    
    def pdf(self, x: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        params = self.params
        return self._pdf(x, params['alpha'], params['beta'], params['c'], params['mu'])
    
    def cdf(self, x: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        x = np.atleast_1d(x)
        results = np.zeros_like(x)
        for i, xi in enumerate(x):
            results[i], _ = quad(lambda xx: self.pdf(np.array([xx]))[0], -np.inf, xi)
        return results
    
    def ppf(self, q: np.ndarray) -> np.ndarray:
        if not self.params:
            self.fit()
        q = np.atleast_1d(q)
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