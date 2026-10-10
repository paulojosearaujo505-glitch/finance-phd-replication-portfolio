"""
Format Table 2: Combining CAPM and FF3 Results
Author: Paulo Jose Araujo
Description: Combines the CAPM and Fama-French 3-Factor regression results
             into a single, publication-quality table.
"""

import pandas as pd

# --- 1. Load Both Result Sets ---
capm_df = pd.read_csv('01_fama_french_1993/output/table_2_capm_results.csv', index_col='Portfolio')
ff3_df = pd.read_csv('01_fama_french_1993/output/table_2_ff3_results.csv', index_col='Portfolio')

# --- 2. Format Coefficients with T-Stats in Parentheses ---
# We create string columns like "0.0015 (2.04)"
capm_df['CAPM_Alpha_Formatted'] = capm_df.apply(lambda row: f"{row['Alpha']:.4f} ({row['Alpha_tstat']:.2f})", axis=1)
ff3_df['FF3_Alpha_Formatted'] = ff3_df.apply(lambda row: f"{row['Alpha']:.4f} ({row['Alpha_tstat']:.2f})", axis=1)

# --- 3. Combine into One Table ---
formatted_table = pd.DataFrame(index=capm_df.index)
formatted_table['CAPM Alpha (t-stat)'] = capm_df['CAPM_Alpha_Formatted']
formatted_table['FF3 Alpha (t-stat)'] = ff3_df['FF3_Alpha_Formatted']
formatted_table['CAPM R-squared'] = capm_df['R_squared'].round(4)
formatted_table['FF3 Adj. R-squared'] = ff3_df['Adj_R_squared'].round(4)

# --- 4. Save and Preview ---
OUTPUT_PATH = '01_fama_french_1993/output/table_2_formatted.csv'
formatted_table.to_csv(OUTPUT_PATH)

print("--- Formatted Table 2: Original Sample (1963-1991) ---")
print(formatted_table)
print(f"\nTable successfully saved to {OUTPUT_PATH}")