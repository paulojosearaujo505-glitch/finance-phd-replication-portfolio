"""
Data Cleaning & Transformation: Macroeconomic Data
Author: Paulo Jose Araujo
Description: Loads raw macro data, resamples it to quarterly frequency,
             calculates year-over-year growth rates, and saves the clean dataset.
"""

import pandas as pd

# --- 1. Load Raw Data ---
INPUT_CSV = '01_fama_french_1993/data/macro_data.csv'
OUTPUT_CSV = '01_fama_french_1993/data/cleaned_macro_data.csv'

df = pd.read_csv(INPUT_CSV, index_col='Date', parse_dates=True)
print("Raw data loaded successfully. Shape:", df.shape)

# --- 2. Resample to Quarterly Frequency ---
# GDP is quarterly. UNRATE and CPI are monthly.
# We will convert everything to quarterly to match GDP.
# We use .mean() to average the monthly values within each quarter.
df_quarterly = df.resample('QE').mean()
print("Data resampled to quarterly frequency. Shape:", df_quarterly.shape)

# --- 3. Calculate Year-over-Year (YoY) Growth Rates ---
# Since the data is now quarterly, periods=4 calculates the change from the same quarter last year.
df_quarterly['GDP_Growth'] = df_quarterly['GDP'].pct_change(periods=4) * 100
df_quarterly['Inflation_Rate'] = df_quarterly['CPIAUCSL'].pct_change(periods=4) * 100

# Unemployment rate is already a percentage, so we don't need to calculate its growth rate.

# --- 4. Drop Missing Values (NaNs) ---
# The pct_change() function creates NaNs for the first 4 quarters.
# We also have NaNs from the early years where data didn't exist.
df_clean = df_quarterly.dropna()
print("NaNs dropped. Final clean shape:", df_clean.shape)

# --- 5. Save the Cleaned Data ---
df_clean.to_csv(OUTPUT_CSV)
print(f"Successfully saved cleaned data to {OUTPUT_CSV}")

# --- 6. Preview the Results ---
print("\nPreview of the cleaned data:")
print(df_clean.head())
print("\nLast 5 rows of the cleaned data:")
print(df_clean.tail())