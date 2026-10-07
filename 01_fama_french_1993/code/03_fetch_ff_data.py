"""
Fama-French Data Downloader
Author: Paulo Jose Araujo
Description: Downloads the Fama-French 3-Factor data and the 25 Size/Book-to-Market
             portfolios directly from Kenneth French's Dartmouth library.
             Cleans the messy headers and saves them as CSV files.
"""

import os
import pandas as pd
import numpy as np

# --- 1. Configuration ---
# URLs for the zipped CSV files from Kenneth French's website
FF_FACTORS_URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'
FF_PORTFOLIOS_URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip'

OUTPUT_FACTORS = '01_fama_french_1993/data/ff_factors.csv'
OUTPUT_PORTFOLIOS = '01_fama_french_1993/data/ff_25_portfolios.csv'

# --- 2. Function to Clean FF Data ---
def clean_ff_data(df):
    """Helper function to drop annual rows and convert to decimal returns."""
    # Convert index to string and remove any leading/trailing spaces
    df.index = df.index.astype(str).str.strip()
    
    # Keep ONLY rows where the index has 6 digits (YYYYMM monthly data)
    # This automatically drops the 4-digit annual data at the bottom of the file
    df = df[df.index.str.len() == 6]
    
    # Convert the index (YYYYMM) to a proper datetime object
    df.index = pd.to_datetime(df.index, format='%Y%m')
    df.index.name = 'Date'
    
    # Divide by 100 to convert percentage returns to decimals
    df = df.astype(float) / 100
    
    return df

# --- 3. Download and Process 3-Factor Data ---
print("Downloading Fama-French 3-Factor Data...")
# skiprows=3 is specific to the format of this file
factors_df = pd.read_csv(FF_FACTORS_URL, skiprows=3, index_col=0)
factors_df = clean_ff_data(factors_df)

os.makedirs('01_fama_french_1993/data', exist_ok=True)
factors_df.to_csv(OUTPUT_FACTORS)
print(f"Factors data saved to {OUTPUT_FACTORS}")
print("\nFactors Preview:")
print(factors_df.head())

# --- 4. Download and Process 25 Portfolios Data ---
print("\nDownloading 25 Portfolios Data...")
# skiprows=6 is specific to the format of this file
# NEW CLEAN CODE
portfolios_df = pd.read_csv(FF_PORTFOLIOS_URL, skiprows=15, index_col=0)
portfolios_df = clean_ff_data(portfolios_df)

portfolios_df.to_csv(OUTPUT_PORTFOLIOS)
print(f"Portfolios data saved to {OUTPUT_PORTFOLIOS}")
print("\nPortfolios Preview:")
print(portfolios_df.head())

print("\nData acquisition complete!")