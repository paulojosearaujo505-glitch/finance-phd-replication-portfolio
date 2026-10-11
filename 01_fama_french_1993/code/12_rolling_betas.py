"""
Rolling Betas: Visualizing Factor Exposure Over Time
Author: Paulo Jose Araujo
Description: Calculates rolling 5-year betas for the SMALL HiBM portfolio
             to visually show when the factor loadings structurally changed.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# --- 1. Load the Data ---
portfolios_df = pd.read_csv('01_fama_french_1993/data/ff_25_portfolios.csv', index_col='Date', parse_dates=True)
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)

# Clean and align
portfolios_df = portfolios_df.sort_index()
factors_df = factors_df.sort_index()
portfolios_df = portfolios_df[~portfolios_df.index.duplicated(keep='first')]
portfolios_df = portfolios_df.loc[portfolios_df.index.isin(factors_df.index)]

# --- 2. Target Portfolio and Excess Returns ---
target_portfolio = 'SMALL HiBM'
y = portfolios_df[target_portfolio].sub(factors_df['RF'])
X = factors_df[['Mkt-RF', 'SMB', 'HML']]

# --- 3. Calculate Rolling Betas (60-month window) ---
window = 60
rolling_betas = []

# We loop through the data, starting at the end of the first window
for i in range(window, len(X) + 1):
    # Slice the data for the current window
    X_window = sm.add_constant(X.iloc[i-window:i])
    y_window = y.iloc[i-window:i]
    
    # Run the regression
    model = sm.OLS(y_window, X_window).fit()
    
    # Store the betas
    rolling_betas.append({
        'Date': X.index[i-1], # The date at the end of the window
        'Beta_Mkt': model.params['Mkt-RF'],
        'Beta_SMB': model.params['SMB'],
        'Beta_HML': model.params['HML']
    })

# Convert to DataFrame
rolling_betas_df = pd.DataFrame(rolling_betas).set_index('Date')

# --- 4. Visualization ---
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(rolling_betas_df.index, rolling_betas_df['Beta_SMB'], label='Rolling Beta (SMB)', color='#d62728', linewidth=2)
ax.plot(rolling_betas_df.index, rolling_betas_df['Beta_HML'], label='Rolling Beta (HML)', color='#2ca02c', linewidth=2)

# Add a vertical line to mark the end of the original Fama-French sample
ax.axvline(pd.to_datetime('1991-12-31'), color='black', linestyle='--', linewidth=2, label='End of Original Sample (1991)')

ax.set_title(f'Rolling 5-Year Factor Betas: {target_portfolio}', fontsize=16, fontweight='bold')
ax.set_ylabel('Beta', fontsize=12)
ax.set_xlabel('Year', fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
OUTPUT_PLOT = '01_fama_french_1993/output/rolling_betas.png'
os.makedirs('01_fama_french_1993/output', exist_ok=True)
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"Rolling beta plot saved to {OUTPUT_PLOT}")

# Save the underlying data
OUTPUT_CSV = '01_fama_french_1993/output/rolling_betas.csv'
rolling_betas_df.to_csv(OUTPUT_CSV)
print(f"Rolling beta data saved to {OUTPUT_CSV}")