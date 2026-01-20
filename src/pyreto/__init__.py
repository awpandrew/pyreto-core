"""Pyreto: Tail risk management library with Monte Carlo simulation (classless functional API)."""

__version__ = "0.4.0"

# Make distributions available at pyreto.*
from .distributions import student_t
from .distributions import alpha_stable
from .distributions import nig

__all__ = ["student_t", "alpha_stable", "nig"]
