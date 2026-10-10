"""
Fama-French 3-Factor Time-Series Regressions
Author: Paulo Jose Araujo
Description: Runs 3-factor regressions (Mkt-RF, SMB, HML) for each of the 
             25 Size/Book-to-Market portfolios. Replicates Table 2 (Part B).
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

# --- 2. Filter for the Original Sample Period ---
start_date = '1963-07-01'
end_date = '1991-12-31'

portfolios_df = portfolios_df.loc[start_date:end_date]
factors_df = factors_df.loc[start_date:end_date]

# --- 3. Calculate Excess Returns ---
excess_returns_df = portfolios_df.sub(factors_df['RF'], axis=0)

# --- 4. Prepare the Independent Variables (All 3 Factors) ---
X = sm.add_constant(factors_df[['Mkt-RF', 'SMB', 'HML']])

# --- 5. Run the 3-Factor Regressions in a Loop ---
results_list = []

for portfolio in excess_returns_df.columns:
    y = excess_returns_df[portfolio]
    model = sm.OLS(y, X).fit()
    
    # Extract the key statistics
    alpha = model.params['const']
    alpha_tstat = model.tvalues['const']
    beta_mkt = model.params['Mkt-RF']
    beta_smb = model.params['SMB']
    beta_hml = model.params['HML']
    adj_r_squared = model.rsquared_adj
    
    results_list.append({
        'Portfolio': portfolio,
        'Alpha': alpha,
        'Alpha_tstat': alpha_tstat,
        'Beta_Mkt': beta_mkt,
        'Beta_SMB': beta_smb,
        'Beta_HML': beta_hml,
        'Adj_R_squared': adj_r_squared
    })

# --- 6. Format the Results into a Clean Table ---
results_df = pd.DataFrame(results_list)
results_df = results_df.set_index('Portfolio')

# --- 7. Save and Preview ---
OUTPUT_PATH = '01_fama_french_1993/output/table_2_ff3_results.csv'
os.makedirs('01_fama_french_1993/output', exist_ok=True)
results_df.to_csv(OUTPUT_PATH)

print("\n--- Fama-French 3-Factor Regression Results (Table 2, Part B) ---")
print(results_df.round(4))
print(f"\nResults successfully saved to {OUTPUT_PATH}")