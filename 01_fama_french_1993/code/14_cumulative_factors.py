"""
Cumulative Factor Returns: SMB and HML Across Sub-Periods
Author: Paulo Jose Araujo
Description: Plots the cumulative returns of the SMB and HML factors
             from 1926 to 2025, with shaded regions for the three sub-periods.
             This is the capstone visualization for the extension project.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. Load the Data ---
factors_df = pd.read_csv('01_fama_french_1993/data/ff_factors.csv', index_col='Date', parse_dates=True)
factors_df = factors_df.sort_index()

# --- 2. Calculate Cumulative Returns ---
# Compound the monthly returns: (1 + r).cumprod() - 1
cumulative = (1 + factors_df[['SMB', 'HML']]).cumprod() - 1

# --- 3. Define Sub-Periods for Shading ---
periods = {
    'Original (1963-1991)': ('1963-07-01', '1991-12-31'),
    'Post-Pub (1992-2007)': ('1992-01-01', '2007-12-31'),
    'Modern (2008-2025)': ('2008-01-01', '2025-12-31')
}

# --- 4. Create the Visualization ---
fig, ax = plt.subplots(figsize=(16, 9))

# Plot the cumulative returns
ax.plot(cumulative.index, cumulative['SMB'] * 100, label='SMB (Size Premium)', color='#d62728', linewidth=2)
ax.plot(cumulative.index, cumulative['HML'] * 100, label='HML (Value Premium)', color='#2ca02c', linewidth=2)

# Add shaded regions for sub-periods
colors = ['#e6f3ff', '#fff5e6', '#ffe6e6']  # Light blue, light orange, light red
for i, (period_name, (start, end)) in enumerate(periods.items()):
    ax.axvspan(pd.to_datetime(start), pd.to_datetime(end), alpha=0.5, color=colors[i], label=period_name)

# Add a vertical dashed line at the end of 1991
ax.axvline(pd.to_datetime('1991-12-31'), color='black', linestyle='--', linewidth=1.5)
ax.text(pd.to_datetime('1992-06-01'), ax.get_ylim()[0] + 5, 'Post-Publication', fontsize=10, fontweight='bold')

# Formatting
ax.set_title('Cumulative Returns of SMB and HML Factors (1926-2025)', fontsize=18, fontweight='bold')
ax.set_ylabel('Cumulative Return (%)', fontsize=14)
ax.set_xlabel('Year', fontsize=14)
ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)

# Format x-axis to show decades
ax.xaxis.set_major_locator(mdates.YearLocator(10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
OUTPUT_PLOT = '01_fama_french_1993/output/cumulative_factors.png'
os.makedirs('01_fama_french_1993/output', exist_ok=True)
plt.savefig(OUTPUT_PLOT, dpi=300)
print(f"Cumulative factor plot saved to {OUTPUT_PLOT}")

# --- 5. Print Summary Statistics ---
print("\n--- Cumulative Returns by Sub-Period ---")
for period_name, (start, end) in periods.items():
    period_data = cumulative.loc[start:end]
    smb_start = period_data['SMB'].iloc[0] if len(period_data) > 0 else 0
    smb_end = period_data['SMB'].iloc[-1] if len(period_data) > 0 else 0
    hml_start = period_data['HML'].iloc[0] if len(period_data) > 0 else 0
    hml_end = period_data['HML'].iloc[-1] if len(period_data) > 0 else 0
    
    print(f"\n{period_name}:")
    print(f"  SMB Cumulative Return: {(smb_end - smb_start)*100:.2f}%")
    print(f"  HML Cumulative Return: {(hml_end - hml_start)*100:.2f}%")