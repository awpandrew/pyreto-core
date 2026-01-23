#!/usr/bin/env python3
"""
Example: Analyze SPY returns with pyreto

This example uses the included spy_returns.csv file so you can 
test pyreto immediately without downloading your own data.

Uses Student's T distribution (fastest and most robust).
"""

import sys
sys.path.insert(0, 'src')

import pyreto as pr
import numpy as np
import time


def load_spy_returns():
    """Load SPY returns from included CSV file."""
    # Use Polars for fastest I/O (Rust backend)
    import polars as pl
    df = pl.read_csv('spy_returns.csv')
    returns = df[df.columns[1]].to_numpy()
    return returns


def main():
    print("=" * 70)
    print("PYRETO SPY ANALYSIS EXAMPLE")
    print("=" * 70)
    print()
    print("Loading SPY daily returns from spy_returns.csv...")
    print()
    
    try:
        returns = load_spy_returns()
    except FileNotFoundError:
        print("ERROR: spy_returns.csv not found.")
        print("  Please run this script from the repository root.")
        sys.exit(1)
    
    # Basic statistics
    print(f"Data loaded: {len(returns)} daily returns")
    print(f"Mean: {np.mean(returns):.6f}")
    print(f"Std:  {np.std(returns):.6f}")
    print()
    
    print(f"{'-' * 70}")
    print(f"STUDENT'S T DISTRIBUTION (fastest and most robust)")
    print(f"{'-' * 70}")
    
    # Fit the model
    start_time = time.time()
    print("Fitting...")
    par = pr.student_t.fit(returns)
    elapsed = time.time() - start_time
    print(f"✓ Parameters: {par} ({elapsed:.3f}s)")
    print()
    
    # Calculate risk metrics at multiple levels
    for alpha in [0.05, 0.01, 0.001]:
        var = pr.student_t.var(alpha, par)
        es = pr.student_t.es(alpha, par)
        print(f"  {alpha*100:.1f}% VaR: {var:.6f} ({var*100:.2f}%)")
        print(f"  {alpha*100:.1f}% ES:  {es:.6f} ({es*100:.2f}%)")
    print()
    
    # Show fitted distribution vs normal
    normal_var_5 = -1.645 * np.std(returns)  # Theoretical 5% normal VaR
    student_var_5 = pr.student_t.var(0.05, par)
    ratio = student_var_5 / normal_var_5
    
    print("Comparison with Normal distribution:")
    print(f"  Normal 5% VaR:   {normal_var_5:.6f} ({normal_var_5*100:.2f}%)")
    print(f"  Student 5% VaR:  {student_var_5:.6f} ({student_var_5*100:.2f}%)")
    print(f"  Ratio: {ratio:.2f}x (shows fat tail severity)")
    print()
    
    print("=" * 70)
    print("Analysis complete!")
    print()
    print("Key insights:")
    print(f"  - Using normal distribution would underestimate 5% VaR by {(ratio-1)*100:.0f}%")
    print(f"  - Expected Shortfall is {abs(es/var):.1f}x worse than VaR at 1% level")
    print()
    print("To use with your own data:")
    print("  1. Save returns to CSV with any column name")
    print("  2. Load with: returns = np.genfromtxt('file.csv', delimiter=',', skip_header=1)")
    print("  3. Analyze: par = pr.student_t.fit(returns)")


if __name__ == "__main__":
    main()
