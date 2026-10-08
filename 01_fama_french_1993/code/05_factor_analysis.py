"""
Factor Analysis: Fama-French 3 Factors
Author: Paulo Jose Araujo
Description: Loads the 3-factor data and analyzes:
             1. Correlation matrix between Mkt-RF, SMB, HML
             2. Cumulative returns of each factor over time
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Load the Factors Data ---
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)
factors_df = factors_df.sort_index()

print(f"Factors data loaded. Shape: {factors_df.shape}")
print(f"Date range: {factors_df.index[0].date()} to {factors_df.index[-1].date()}")

# --- 2. Correlation Matrix ---
# Correlations between Mkt-RF, SMB, HML (we exclude RF as it is not a risk factor)
corr_matrix = factors_df[['Mkt-RF', 'SMB', 'HML']].corr()

print("\n--- Correlation Matrix (Full Sample) ---")
print(corr_matrix.round(4))

# --- 3. Cumulative Returns ---
# We compound the monthly returns: (1 + r).cumprod() - 1
# This shows the total growth of $1 invested in each factor.
cumulative_returns = (1 + factors_df[['Mkt-RF', 'SMB', 'HML']]).cumprod() - 1

# --- 4. Visualization: 3-Panel Plot ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Panel 1: Cumulative Returns
axes[0].plot(cumulative_returns.index, cumulative_returns['Mkt-RF'], label='Mkt-RF', color='#1f77b4', linewidth=1.5)
axes[0].plot(cumulative_returns.index, cumulative_returns['SMB'], label='SMB', color='#d62728', linewidth=1.5)
axes[0].plot(cumulative_returns.index, cumulative_returns['HML'], label='HML', color='#2ca02c', linewidth=1.5)
axes[0].set_title('Cumulative Returns of Fama-French Factors (1926 - Present)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Cumulative Return', fontsize=12)
axes[0].legend(fontsize=12)
axes[0].grid(True, alpha=0.5)

# Panel 2: Rolling 12-Month Volatility of SMB and HML
rolling_vol = factors_df[['SMB', 'HML']].rolling(window=12).std() * (12 ** 0.5)
axes[1].plot(rolling_vol.index, rolling_vol['SMB'], label='SMB Volatility', color='#d62728', linewidth=1.2)
axes[1].plot(rolling_vol.index, rolling_vol['HML'], label='HML Volatility', color='#2ca02c', linewidth=1.2)
axes[1].set_title('Rolling 12-Month Annualized Volatility of SMB and HML', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Annualized Volatility', fontsize=12)
axes[1].set_xlabel('Year', fontsize=12)
axes[1].legend(fontsize=12)
axes[1].grid(True, alpha=0.5)

plt.tight_layout()
OUTPUT_PLOT = '01_fama_french_1993/output/factor_analysis.png'
os.makedirs('01_fama_french_1993/output', exist_ok=True)
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"\nPlot saved to {OUTPUT_PLOT}")

# --- 5. Save the Correlation Matrix ---
OUTPUT_CSV = '01_fama_french_1993/output/factor_correlations.csv'
corr_matrix.to_csv(OUTPUT_CSV)
print(f"Correlation matrix saved to {OUTPUT_CSV}")

# --- 6. Summary of Factor Performance ---
print("\n--- Factor Performance Summary (Full Sample) ---")
annual_return = factors_df[['Mkt-RF', 'SMB', 'HML']].mean() * 12
annual_vol = factors_df[['Mkt-RF', 'SMB', 'HML']].std() * (12 ** 0.5)
sharpe = annual_return / annual_vol

summary = pd.DataFrame({
    'Annualized Mean (%)': (annual_return * 100).round(2),
    'Annualized Vol (%)': (annual_vol * 100).round(2),
    'Annualized Sharpe': sharpe.round(3)
})
print(summary)