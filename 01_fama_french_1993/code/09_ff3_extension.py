"""
Fama-French 3-Factor Regressions: Extended Sample
Author: Paulo Jose Araujo
Description: Runs 3-factor regressions on the post-publication sample 
             (1992-2025) to test if the model still holds out-of-sample.
"""

import os
import pandas as pd
import statsmodels.api as sm

# --- 1. Load the Data ---
portfolios_df = pd.read_csv('01_fama_french_1993/data/ff_25_portfolios.csv', index_col='Date', parse_dates=True)
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)

# Sort and clean the index
portfolios_df = portfolios_df.sort_index()
factors_df = factors_df.sort_index()
portfolios_df = portfolios_df[~portfolios_df.index.duplicated(keep='first')]
portfolios_df = portfolios_df.loc[portfolios_df.index.isin(factors_df.index)]

# --- 2. Filter for the EXTENDED Sample Period ---
# The original paper ended in 1991. We start right after.
start_date = '1992-01-01'
end_date = '2025-12-31' # Assuming data goes through 2025

portfolios_df = portfolios_df.loc[start_date:end_date]
factors_df = factors_df.loc[start_date:end_date]

print(f"Extended Sample Period: {portfolios_df.index[0].date()} to {portfolios_df.index[-1].date()}")

# --- 3. Calculate Excess Returns ---
excess_returns_df = portfolios_df.sub(factors_df['RF'], axis=0)

# --- 4. Prepare the Independent Variables ---
X = sm.add_constant(factors_df[['Mkt-RF', 'SMB', 'HML']])

# --- 5. Run the Regressions ---
results_list = []

for portfolio in excess_returns_df.columns:
    y = excess_returns_df[portfolio]
    model = sm.OLS(y, X).fit()
    
    results_list.append({
        'Portfolio': portfolio,
        'Alpha': model.params['const'],
        'Alpha_tstat': model.tvalues['const'],
        'Beta_Mkt': model.params['Mkt-RF'],
        'Beta_SMB': model.params['SMB'],
        'Beta_HML': model.params['HML'],
        'Adj_R_squared': model.rsquared_adj
    })

# --- 6. Format and Save ---
results_df = pd.DataFrame(results_list).set_index('Portfolio')

OUTPUT_PATH = '01_fama_french_1993/output/table_2_ff3_extended_results.csv'
results_df.to_csv(OUTPUT_PATH)

print("\n--- FF3 Regression Results: Extended Sample (1992-2025) ---")
print(results_df.round(4))
print(f"\nResults saved to {OUTPUT_PATH}")