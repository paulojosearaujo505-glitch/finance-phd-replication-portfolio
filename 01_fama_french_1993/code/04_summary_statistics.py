"""
Summary Statistics: Fama-French 25 Portfolios
Author: Paulo Jose Araujo
Description: Loads the 25 Size/Book-to-Market portfolios and the Risk-Free rate.
             Calculates the average monthly excess return, standard deviation,
             and Sharpe ratio for each portfolio (replicating Table 1).
"""

import os
import pandas as pd

# --- 1. Load the Data ---
portfolios_df = pd.read_csv('01_fama_french_1993/data/ff_25_portfolios.csv', index_col='Date', parse_dates=True)
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)

# --- 2. DEFINITIVE FIX: Align Frequencies ---
# Sort the indices
portfolios_df = portfolios_df.sort_index()
factors_df = factors_df.sort_index()

# Drop duplicate dates in portfolios
portfolios_df = portfolios_df[~portfolios_df.index.duplicated(keep='first')]

# Filter portfolios to only keep dates that exist in the clean factors file.
# This instantly drops the annual data because the factors file is 100% monthly.
portfolios_df = portfolios_df.loc[portfolios_df.index.isin(factors_df.index)]

# --- 3. Filter for the Original Sample Period ---
start_date = '1963-07-01'
end_date = '1991-12-31'

portfolios_df = portfolios_df.loc[start_date:end_date]
factors_df = factors_df.loc[start_date:end_date]

print(f"Data loaded for period: {start_date} to {end_date}")

# --- 4. Calculate Excess Returns ---
excess_returns_df = portfolios_df.sub(factors_df['RF'], axis=0)

# --- 5. Calculate Summary Statistics ---
mean_returns = excess_returns_df.mean()
std_devs = excess_returns_df.std()
sharpe_ratios = mean_returns / std_devs

# --- 6. Combine into a Clean Table ---
summary_table = pd.DataFrame({
    'Mean Excess Return': mean_returns,
    'Standard Deviation': std_devs,
    'Sharpe Ratio': sharpe_ratios
})

# --- 7. Save and Preview ---
OUTPUT_PATH = '01_fama_french_1993/output/table_1_summary_stats.csv'
os.makedirs('01_fama_french_1993/output', exist_ok=True)
summary_table.to_csv(OUTPUT_PATH)

print("\n--- Summary Statistics (Table 1 Replication) ---")
print(summary_table.round(4))
print(f"\nTable successfully saved to {OUTPUT_PATH}")