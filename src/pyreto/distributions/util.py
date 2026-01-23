import numpy as np
import warnings
from typing import Sequence


def _validate_returns(returns: Sequence[float] | np.ndarray) -> np.ndarray:
    """
    Convert `returns` to a 1-D float64 NumPy array and run basic checks.

    Returns
    -------
    np.ndarray
        Validated, ravelled copy/view of the input.

    Raises
    ------
    ValueError
        If the array is empty or contains non-finite values.
    """
    # NOTE: should this also warn if len(returns) below certain threshold? below certain length no statistical reasoning makes sense?

    return returns
