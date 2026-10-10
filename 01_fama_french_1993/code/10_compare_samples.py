"""
Comparison Analysis: Original vs. Extended Sample
Author: Paulo Jose Araujo
Description: Compares the Fama-French 3-factor regression results from the
             original sample (1963-1991) and the extended sample (1992-2025).
             Generates a grouped bar chart of the alphas.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Both Result Sets ---
original_df = pd.read_csv('01_fama_french_1993/output/table_2_ff3_results.csv', index_col='Portfolio')
extended_df = pd.read_csv('01_fama_french_1993/output/table_2_ff3_extended_results.csv', index_col='Portfolio')

# --- 2. Combine into a Single Comparison Table ---
comparison = pd.DataFrame(index=original_df.index)
comparison['Alpha_Original'] = original_df['Alpha']
comparison['Alpha_Extended'] = extended_df['Alpha']
comparison['Alpha_Difference'] = comparison['Alpha_Extended'] - comparison['Alpha_Original']

# We also check if the alphas were significant in each period
# (A t-stat greater than 2 or less than -2 is considered significant)
comparison['Sig_Original'] = original_df['Alpha_tstat'].abs() > 2
comparison['Sig_Extended'] = extended_df['Alpha_tstat'].abs() > 2

# --- 3. Save the Comparison Table ---
OUTPUT_CSV = '01_fama_french_1993/output/alpha_comparison.csv'
comparison.to_csv(OUTPUT_CSV)

print("--- Alpha Comparison: Original vs. Extended Sample ---")
print(comparison.round(5))
print(f"\nComparison table saved to {OUTPUT_CSV}")

# --- 4. Visualization: Grouped Bar Chart ---
# This will visually show how the alphas have changed for each portfolio.
fig, ax = plt.subplots(figsize=(16, 8))

x = np.arange(len(comparison.index))
width = 0.35

bars1 = ax.bar(x - width/2, comparison['Alpha_Original'] * 100, width, label='Original Sample (1963-1991)', color='#1f77b4')
bars2 = ax.bar(x + width/2, comparison['Alpha_Extended'] * 100, width, label='Extended Sample (1992-2025)', color='#ff7f0e')

# Add a horizontal line at zero for reference
ax.axhline(0, color='black', linestyle='--', linewidth=1)

ax.set_title('Comparison of 3-Factor Model Alphas: Original vs. Extended Sample', fontsize=16, fontweight='bold')
ax.set_ylabel('Monthly Alpha (%)', fontsize=12)
ax.set_xlabel('Portfolio', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(comparison.index, rotation=90, fontsize=9)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
OUTPUT_PLOT = '01_fama_french_1993/output/alpha_comparison.png'
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"Plot saved to {OUTPUT_PLOT}")