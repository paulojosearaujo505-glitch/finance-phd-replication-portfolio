"""
Data Visualization: Macroeconomic Dashboard
Author: Paulo Jose Araujo
Description: Loads the cleaned macroeconomic data and generates a 
             multi-panel visualization (GDP Growth, Unemployment, Inflation).
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Load Cleaned Data ---
INPUT_CSV = '01_fama_french_1993/data/cleaned_macro_data.csv'
OUTPUT_PLOT = '01_fama_french_1993/output/macro_dashboard.png'

df = pd.read_csv(INPUT_CSV, index_col='Date', parse_dates=True)
print("Cleaned data loaded successfully. Shape:", df.shape)

# --- 2. Setup the Visualization Style ---
plt.style.use('seaborn-v0_8-whitegrid') # Clean, professional look
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14, 12), sharex=True)

# --- 3. Plot 1: GDP Growth ---
axes[0].plot(df.index, df['GDP_Growth'], color='#1f77b4', linewidth=2)
axes[0].axhline(0, color='black', linestyle='--', linewidth=1) # Add a zero line
axes[0].set_title('US GDP Year-over-Year Growth', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Percent Change (%)', fontsize=12)
axes[0].grid(True, alpha=0.5)

# --- 4. Plot 2: Unemployment Rate ---
axes[1].plot(df.index, df['UNRATE'], color='#d62728', linewidth=2)
axes[1].set_title('US Unemployment Rate', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Percent (%)', fontsize=12)
axes[1].grid(True, alpha=0.5)

# --- 5. Plot 3: Inflation Rate ---
axes[2].plot(df.index, df['Inflation_Rate'], color='#2ca02c', linewidth=2)
axes[2].axhline(0, color='black', linestyle='--', linewidth=1)
axes[2].set_title('US Inflation Rate (CPI YoY)', fontsize=14, fontweight='bold')
axes[2].set_ylabel('Percent Change (%)', fontsize=12)
axes[2].set_xlabel('Year', fontsize=12)
axes[2].grid(True, alpha=0.5)

# --- 6. Final Formatting and Saving ---
plt.suptitle('US Macroeconomic Dashboard (1948 - Present)', fontsize=18, fontweight='bold', y=0.98)
plt.tight_layout()

os.makedirs('01_fama_french_1993/output', exist_ok=True)
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"Dashboard successfully saved to {OUTPUT_PLOT}")