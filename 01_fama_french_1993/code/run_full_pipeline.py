"""
Master Pipeline: Macroeconomic Data
Author: Paulo Jose Araujo
Description: A unified, refactored pipeline that fetches, cleans, 
             and visualizes macroeconomic data in a single run.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from fredapi import Fred

# --- Configuration ---
SERIES_IDS = {
    'GDP': 'GDP',
    'UNRATE': 'UNRATE',
    'CPIAUCSL': 'CPIAUCSL'
}
RAW_DATA_PATH = '01_fama_french_1993/data/macro_data.csv'
CLEAN_DATA_PATH = '01_fama_french_1993/data/cleaned_macro_data.csv'
PLOT_PATH = '01_fama_french_1993/output/macro_dashboard.png'


def fetch_fred_data(api_key, series_ids, output_path):
    """Fetches data from FRED API and saves it as a raw CSV."""
    print("Step 1: Fetching data from FRED...")
    fred = Fred(api_key=api_key)
    data_frames = []
    
    for name, series_id in series_ids.items():
        series_data = fred.get_series(series_id)
        df = pd.DataFrame(series_data, columns=[name])
        data_frames.append(df)
        
    merged_df = pd.concat(data_frames, axis=1, join='outer', sort=False)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged_df.index.name = 'Date'
    merged_df.to_csv(output_path)
    print(f"Raw data saved to {output_path}")
    return merged_df


def clean_macro_data(input_path, output_path):
    """Loads raw data, resamples to quarterly, calculates growth rates, and saves."""
    print("\nStep 2: Cleaning and transforming data...")
    df = pd.read_csv(input_path, index_col='Date', parse_dates=True)
    
    # Resample to quarterly
    df_q = df.resample('QE').mean()
    
    # Calculate YoY growth rates
    df_q['GDP_Growth'] = df_q['GDP'].pct_change(periods=4) * 100
    df_q['Inflation_Rate'] = df_q['CPIAUCSL'].pct_change(periods=4) * 100
    
    # Drop NaNs
    df_clean = df_q.dropna()
    df_clean.to_csv(output_path)
    print(f"Cleaned data saved to {output_path}")
    return df_clean


def plot_macro_dashboard(df, output_path):
    """Generates a multi-panel dashboard of the macroeconomic data."""
    print("\nStep 3: Generating visualization...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14, 12), sharex=True)

    axes[0].plot(df.index, df['GDP_Growth'], color='#1f77b4', linewidth=2)
    axes[0].axhline(0, color='black', linestyle='--', linewidth=1)
    axes[0].set_title('US GDP Year-over-Year Growth', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Percent Change (%)', fontsize=12)

    axes[1].plot(df.index, df['UNRATE'], color='#d62728', linewidth=2)
    axes[1].set_title('US Unemployment Rate', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Percent (%)', fontsize=12)

    axes[2].plot(df.index, df['Inflation_Rate'], color='#2ca02c', linewidth=2)
    axes[2].axhline(0, color='black', linestyle='--', linewidth=1)
    axes[2].set_title('US Inflation Rate (CPI YoY)', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('Percent Change (%)', fontsize=12)
    axes[2].set_xlabel('Year', fontsize=12)

    plt.suptitle('US Macroeconomic Dashboard (1948 - Present)', fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    print(f"Dashboard saved to {output_path}")


if __name__ == "__main__":
    # Retrieve API Key
    api_key = os.environ.get('FRED_API_KEY')
    if not api_key:
        raise ValueError("FRED_API_KEY environment variable not set.")
        
    # Execute the pipeline
    raw_df = fetch_fred_data(api_key, SERIES_IDS, RAW_DATA_PATH)
    clean_df = clean_macro_data(RAW_DATA_PATH, CLEAN_DATA_PATH)
    plot_macro_dashboard(clean_df, PLOT_PATH)
    
    print("\nPipeline executed successfully!")