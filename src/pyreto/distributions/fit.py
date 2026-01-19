"""Main fit function."""

import numpy as np
from .student_t import StudentT
from .alpha_stable import AlphaStable
from .normal_inverse_gaussian import NormalInverseGaussian


MODEL_MAP = {
    'student_t': StudentT,
    'alpha_stable': AlphaStable,
    'nig': NormalInverseGaussian,
    'normal_inverse_gaussian': NormalInverseGaussian
}


def load_returns(data, column=None):
    """Load and validate returns from various input types."""
    try:
        import polars as pl
    except ImportError:
        raise ImportError("Polars is required for DataFrame/CSV support. Install with: pip install polars")
    
    if isinstance(data, str):
        df = pl.read_csv(data)
        if column is None:
            numeric_cols = [col for col, dtype in df.schema.items() 
                           if dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]]
            if len(numeric_cols) == 1:
                column = numeric_cols[0]
            else:
                raise ValueError("Multiple numeric columns found. Specify column parameter.")
        returns = df[column].to_numpy()
    elif hasattr(data, 'to_numpy'):
        if column is None:
            numeric_cols = [col for col, dtype in data.schema.items() 
                           if dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]]
            if len(numeric_cols) == 1:
                column = numeric_cols[0]
            else:
                raise ValueError("Multiple numeric columns found. Specify column parameter.")
        returns = data[column].to_numpy()
    elif isinstance(data, np.ndarray):
        returns = data.flatten()
    elif isinstance(data, list):
        returns = np.array(data)
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")
    
    returns = returns.astype(np.float64)
    if not np.isfinite(returns).all():
        raise ValueError("Returns contain non-finite values (NaN or Inf)")
    if len(returns) == 0:
        raise ValueError("Returns cannot be empty")
    
    return returns


def fit(data, column=None, model='student_t'):
    """Fit a single distribution model to returns data.
    
    Parameters
    ----------
    data : str, DataFrame, np.ndarray, or list
        Returns data
    column : str, optional
        Column name if data is DataFrame or CSV
    model : str
        Model to fit: 'student_t', 'alpha_stable', 'nig'
        
    Returns
    -------
    DistributionFitter
        Fitted distribution object
    """
    returns = load_returns(data, column)
    model_name = model.lower()
    
    if model_name not in MODEL_MAP:
        raise ValueError(f"Unknown model: {model}. Available: {list(MODEL_MAP.keys())}")
    
    ModelClass = MODEL_MAP[model_name]
    instance = ModelClass(returns)
    instance.fit()
    
    return instance
