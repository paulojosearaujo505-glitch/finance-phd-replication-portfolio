"""
Sub-Period Analysis: Fama-French 3-Factor Model
Author: Paulo Jose Araujo
Description: Runs the 3-factor model on three distinct sub-periods:
             1. Original (1963-1991)
             2. Post-Publication (1992-2007)
             3. Modern Era (2008-2025)
             Compares the average alpha and factor loadings across regimes.
"""

import os
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load and Clean Data ---
portfolios_df = pd.read_csv('01_fama_french_1993/data/ff_25_portfolios.csv', index_col='Date', parse_dates=True)
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)

portfolios_df = portfolios_df.sort_index()
factors_df = factors_df.sort_index()
portfolios_df = portfolios_df[~portfolios_df.index.duplicated(keep='first')]
portfolios_df = portfolios_df.loc[portfolios_df.index.isin(factors_df.index)]

# Calculate excess returns
excess_returns_df = portfolios_df.sub(factors_df['RF'], axis=0)

# --- 2. Define Sub-Periods ---
sub_periods = {
    'Original (1963-1991)': ('1963-07-01', '1991-12-31'),
    'Post-Pub (1992-2007)': ('1992-01-01', '2007-12-31'),
    'Modern (2008-2025)': ('2008-01-01', '2025-12-31')
}

# --- 3. Run Regressions for Each Sub-Period ---
all_results = {}

for period_name, (start, end) in sub_periods.items():
    print(f"\n{'='*60}")
    print(f"Running FF3 Regressions for: {period_name}")
    print(f"{'='*60}")
    
    # Slice data
    y_period = excess_returns_df.loc[start:end]
    X_period = sm.add_constant(factors_df.loc[start:end, ['Mkt-RF', 'SMB', 'HML']])
    
    results_list = []
    for portfolio in y_period.columns:
        model = sm.OLS(y_period[portfolio], X_period).fit()
        results_list.append({
            'Portfolio': portfolio,
            'Alpha': model.params['const'],
            'Alpha_tstat': model.tvalues['const'],
            'Beta_Mkt': model.params['Mkt-RF'],
            'Beta_SMB': model.params['SMB'],
            'Beta_HML': model.params['HML'],
            'Adj_R_squared': model.rsquared_adj
        })
    
    results_df = pd.DataFrame(results_list).set_index('Portfolio')
    all_results[period_name] = results_df
    
    # Save individual period results
    safe_name = period_name.replace(' ', '_').replace('(', '').replace(')', '')
    output_path = f'01_fama_french_1993/output/subperiod_{safe_name}.csv'
    results_df.to_csv(output_path)
    print(f"Results saved to {output_path}")

# --- 4. Summary Comparison Table ---
print("\n" + "="*60)
print("SUMMARY: Average Statistics Across Sub-Periods")
print("="*60)

summary = pd.DataFrame(index=sub_periods.keys())
for period_name, results_df in all_results.items():
    summary.loc[period_name, 'Avg Alpha'] = results_df['Alpha'].mean()
    summary.loc[period_name, 'Avg |Alpha|'] = results_df['Alpha'].abs().mean()
    summary.loc[period_name, 'Sig. Alphas (# of 25)'] = (results_df['Alpha_tstat'].abs() > 2).sum()
    summary.loc[period_name, 'Avg Beta_SMB'] = results_df['Beta_SMB'].mean()
    summary.loc[period_name, 'Avg Beta_HML'] = results_df['Beta_HML'].mean()
    summary.loc[period_name, 'Avg Adj_R_squared'] = results_df['Adj_R_squared'].mean()

print(summary.round(4))

OUTPUT_SUMMARY = '01_fama_french_1993/output/subperiod_summary.csv'
summary.to_csv(OUTPUT_SUMMARY)
print(f"\nSummary table saved to {OUTPUT_SUMMARY}")

# --- 5. Visualization: Average Alpha and Significant Alphas ---
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Panel 1: Average Absolute Alpha by Period
periods = list(sub_periods.keys())
avg_alphas = [all_results[p]['Alpha'].abs().mean() * 100 for p in periods]
colors = ['#1f77b4', '#ff7f0e', '#d62728']

axes[0].bar(periods, avg_alphas, color=colors)
axes[0].set_title('Average Absolute Alpha by Sub-Period', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Avg |Alpha| (Monthly %)', fontsize=12)
axes[0].grid(True, alpha=0.3, axis='y')

# Panel 2: Number of Significant Alphas by Period
sig_alphas = [(all_results[p]['Alpha_tstat'].abs() > 2).sum() for p in periods]
axes[1].bar(periods, sig_alphas, color=colors)
axes[1].set_title('Number of Significant Alphas (|t| > 2) by Sub-Period', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Count (out of 25 portfolios)', fontsize=12)
axes[1].axhline(1.25, color='black', linestyle='--', linewidth=1, label='Expected by chance (5% of 25)')
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
OUTPUT_PLOT = '01_fama_french_1993/output/subperiod_comparison.png'
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"Comparison plot saved to {OUTPUT_PLOT}")