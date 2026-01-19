"""Student's T distribution - pure functions."""

import numpy as np
from scipy.stats import t as student_t
from scipy.integrate import quad


def _validate_returns(returns):
    """Validate returns array."""
    returns = np.array(returns, dtype=np.float64).flatten()
    if not np.isfinite(returns).all():
        raise ValueError("Returns must be finite (no NaN or Inf)")
    if len(returns) == 0:
        raise ValueError("Returns cannot be empty")
    return returns


def _validate_alpha(alpha):
    """Validate alpha parameter."""
    if not (0 < alpha < 1):
        raise ValueError("Alpha must be between 0 and 1")


def fit(returns):
    """Fit Student's T distribution using MLE.
    
    Parameters
    ----------
    returns : array-like
        Array of returns
        
    Returns
    -------
    dict
        Fitted parameters: {'df': float, 'loc': float, 'scale': float}
    """
    returns = _validate_returns(returns)
    df, loc, scale = student_t.fit(returns)
    return {'df': df, 'loc': loc, 'scale': scale}


def pdf(x, par):
    """Probability density function.
    
    Parameters
    ----------
    x : array-like
        Points at which to evaluate PDF
    par : dict
        Parameters from fit()
        
    Returns
    -------
    ndarray
        PDF values
    """
    return student_t.pdf(x, **par)


def cdf(x, par):
    """Cumulative distribution function.
    
    Parameters
    ----------
    x : array-like
        Points at which to evaluate CDF
    par : dict
        Parameters from fit()
        
    Returns
    -------
    ndarray
        CDF values
    """
    return student_t.cdf(x, **par)


def ppf(q, par):
    """Percent point function (inverse CDF).
    
    Parameters
    ----------
    q : array-like
        Quantiles to evaluate
    par : dict
        Parameters from fit()
        
    Returns
    -------
    ndarray
        PPF values
    """
    return student_t.ppf(q, **par)


def var(alpha, par):
    """Value at Risk at significance level alpha.
    
    Parameters
    ----------
    alpha : float
        Significance level (0 < alpha < 1)
    par : dict
        Parameters from fit()
        
    Returns
    -------
    float
        VaR value
    """
    _validate_alpha(alpha)
    return ppf(alpha, par)[0]


def es(alpha, par):
    """Expected Shortfall at significance level alpha.
    
    Parameters
    ----------
    alpha : float
        Significance level (0 < alpha < 1)
    par : dict
        Parameters from fit()
        
    Returns
    -------
    float
        ES value
    """
    _validate_alpha(alpha)
    var_val = var(alpha, par)
    
    def integrand(x):
        return x * pdf(x, par)[0]
    
    es_val, _ = quad(integrand, -np.inf, var_val)
    return es_val / alpha