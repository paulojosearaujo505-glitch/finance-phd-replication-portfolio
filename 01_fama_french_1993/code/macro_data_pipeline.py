"""
Macroeconomic Data Pipeline: FRED API
Author: Paulo Jose Araujo
Description: Fetches GDP, Unemployment Rate, and CPI from FRED,
             merges them into a single DataFrame, and saves to CSV.
"""

import os
import pandas as pd
from fredapi import Fred

# --- 1. Configuration ---
SERIES_IDS = {
    'GDP': 'GDP',               # Gross Domestic Product (Quarterly)
    'UNRATE': 'UNRATE',         # Civilian Unemployment Rate (Monthly)
    'CPIAUCSL': 'CPIAUCSL'      # Consumer Price Index (Monthly)
}
OUTPUT_CSV = '01_fama_french_1993/data/macro_data.csv'

# --- 2. Retrieve API Key ---
api_key = os.environ.get('FRED_API_KEY')
if not api_key:
    raise ValueError("FRED_API_KEY environment variable not set.")

fred = Fred(api_key=api_key)

# --- 3. Fetch Data ---
print("Fetching macroeconomic data from FRED...")
data_frames = []

for series_name, series_id in SERIES_IDS.items():
    print(f"Fetching {series_name} ({series_id})...")
    series_data = fred.get_series(series_id)
    df = pd.DataFrame(series_data, columns=[series_name])
    data_frames.append(df)

# --- 4. Merge Data ---
merged_df = pd.concat(data_frames, axis=1, join='outer', sort=False)

# --- 5. Save to CSV ---
os.makedirs('01_fama_french_1993/data', exist_ok=True)
merged_df.index.name = 'Date'
merged_df.to_csv(OUTPUT_CSV)
print(f"Successfully saved merged macro data to {OUTPUT_CSV}")

print("\nPreview of the data:")
print(merged_df.head())