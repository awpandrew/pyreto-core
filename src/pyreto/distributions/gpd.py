""" Generalized Pareto """

import numpy as np
from scipy.optimize import minimize
from scipy.special import kv as bessel_k
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import genpareto


def __validate_returns(returns):
    returns =
