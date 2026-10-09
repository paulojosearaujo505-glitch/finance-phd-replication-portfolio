"""
CAPM Time-Series Regressions
Author: Paulo Jose Araujo
Description: Runs CAPM regressions for each of the 25 Size/Book-to-Market portfolios.
             Replicates Table 2 (Part A) of Fama & French (1993).
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

# --- 4. Prepare the Independent Variable (Market Factor) ---
market_excess = factors_df['Mkt-RF']

# Add a constant to the market factor to capture the intercept (alpha)
X = sm.add_constant(market_excess)

# --- 5. Run the CAPM Regressions in a Loop ---
results_list = []

for portfolio in excess_returns_df.columns:
    # Dependent variable: Excess return of the specific portfolio
    y = excess_returns_df[portfolio]
    
    # Run the OLS regression
    model = sm.OLS(y, X).fit()
    
    # Extract the key statistics
    alpha = model.params['const']
    alpha_tstat = model.tvalues['const']
    beta = model.params['Mkt-RF']
    beta_tstat = model.tvalues['Mkt-RF']
    r_squared = model.rsquared
    
    # Store the results
    results_list.append({
        'Portfolio': portfolio,
        'Alpha': alpha,
        'Alpha_tstat': alpha_tstat,
        'Beta': beta,
        'Beta_tstat': beta_tstat,
        'R_squared': r_squared
    })

# --- 6. Format the Results into a Clean Table ---
results_df = pd.DataFrame(results_list)
results_df = results_df.set_index('Portfolio')

# --- 7. Save and Preview ---
OUTPUT_PATH = '01_fama_french_1993/output/table_2_capm_results.csv'
os.makedirs('01_fama_french_1993/output', exist_ok=True)
results_df.to_csv(OUTPUT_PATH)

print("\n--- CAPM Regression Results (Table 2, Part A) ---")
print(results_df.round(4))
print(f"\nResults successfully saved to {OUTPUT_PATH}")