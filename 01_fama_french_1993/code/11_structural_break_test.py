"""
Structural Break Test: Original vs. Extended Sample
Author: Paulo Jose Araujo
Description: Tests whether the factor loadings (betas) and alpha of the
             Fama-French 3-factor model have structurally changed after 1991.
             Uses a dummy variable interaction approach (Chow Test analog).
"""

import os
import pandas as pd
import statsmodels.api as sm

# --- 1. Load the Data ---
portfolios_df = pd.read_csv('01_fama_french_1993/data/ff_25_portfolios.csv', index_col='Date', parse_dates=True)
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)

# Clean and align
portfolios_df = portfolios_df.sort_index()
factors_df = factors_df.sort_index()
portfolios_df = portfolios_df[~portfolios_df.index.duplicated(keep='first')]
portfolios_df = portfolios_df.loc[portfolios_df.index.isin(factors_df.index)]

# --- 2. Calculate Excess Returns (Full Sample) ---
excess_returns_df = portfolios_df.sub(factors_df['RF'], axis=0)

# --- 3. Create the Post-1991 Dummy Variable ---
# This is 0 for the original period (1963-1991) and 1 for the extended period (1992+)
post_1991 = (excess_returns_df.index >= '1992-01-01').astype(int)

# --- 4. Build the Interaction Terms ---
# We create interaction variables: Dummy * Mkt-RF, Dummy * SMB, Dummy * HML
X = pd.DataFrame(index=excess_returns_df.index)
X['const'] = 1
X['Mkt-RF'] = factors_df['Mkt-RF']
X['SMB'] = factors_df['SMB']
X['HML'] = factors_df['HML']
X['Dummy'] = post_1991
X['Dummy_MktRF'] = post_1991 * factors_df['Mkt-RF']
X['Dummy_SMB'] = post_1991 * factors_df['SMB']
X['Dummy_HML'] = post_1991 * factors_df['HML']

# --- 5. Run the Regression for a Representative Portfolio (e.g., SMALL HiBM) ---
# We test the small value portfolio, which had the strongest original premium.
portfolio = 'SMALL HiBM'
y = excess_returns_df[portfolio]

model = sm.OLS(y, X).fit()

print(f"--- Structural Break Test for Portfolio: {portfolio} ---")
print(model.summary().tables[1])
print("\n--- Interpretation ---")
print("If the 'Dummy_*' coefficients are statistically significant (p < 0.05),")
print("then the factor loadings have structurally changed after 1991.")