#!/usr/bin/env python3
"""Download 5 years of SPY data for testing."""

import sys
try:
    import yfinance as yf
    import pandas as pd
    from datetime import datetime, timedelta
except ImportError:
    print("Please install yfinance and pandas:")
    print("pip install yfinance pandas")
    sys.exit(1)

# Download 5 years of SPY data
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

print(f"Downloading SPY data from {start_date.date()} to {end_date.date()}...")
spy = yf.download('SPY', start=start_date, end=end_date, progress=False)

# Calculate daily returns
spy['daily_return'] = spy['Adj Close'].pct_change()

# Remove NaN and save only returns column
spy_returns = spy[['daily_return']].dropna()

# Save to CSV
output_file = 'spy_returns.csv'
spy_returns.to_csv(output_file, index=False)

print(f"✓ Saved {len(spy_returns)} days of SPY returns to {output_file}")
print(f"  Date range: {spy_returns.index[0].date()} to {spy_returns.index[-1].date()}")
print(f"  Mean return: {spy_returns['daily_return'].mean():.6f}")
print(f"  Std deviation: {spy_returns['daily_return'].std():.6f}")
print(f"  Skewness: {spy_returns['daily_return'].skew():.4f}")
print(f"  Kurtosis: {spy_returns['daily_return'].kurtosis():.4f}")
