#!/usr/bin/env python3
"""Generate realistic SPY-like returns data."""

import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# SPY characteristics (2019-2024 approximate)
# - Mean daily return: ~0.0004 (0.04%)
# - Std dev: ~0.014 (1.4%)
# - Negative skew: ~-0.5
# - High kurtosis: ~15 (fat tails)
n_days = 1260  # 5 years of trading days
mean_return = 0.0004
std_return = 0.014

# Generate base normal returns
returns = np.random.normal(mean_return, std_return, n_days)

# Add fat tails (kurtosis)
for i in range(len(returns)):
    if abs(returns[i]) > 2.5 * std_return:
        returns[i] *= np.random.uniform(1.5, 3.0)

# Add negative skew
negative_days = returns < 0
returns[negative_days] *= np.random.uniform(1.0, 1.5, size=negative_days.sum())

# Add a few crisis events
for _ in range(6):  # About 1 per year
    crisis_day = np.random.randint(0, n_days)
    returns[crisis_day] = -np.random.uniform(0.02, 0.08)

# Write to CSV
with open('spy_returns.csv', 'w') as f:
    f.write('daily_return\n')
    for r in returns:
        f.write(f'{r:.8f}\n')

print(f"✓ Generated {n_days} days of SPY-like returns")
print(f"  Mean: {returns.mean():.6f}")
print(f"  Std:  {returns.std():.6f}")
skewness = ((returns - returns.mean()) / returns.std()) ** 3
print(f"  Skew: {skewness.mean():.4f}")
kurtosis = ((returns - returns.mean()) / returns.std()) ** 4
print(f"  Kurt: {kurtosis.mean():.4f}")
