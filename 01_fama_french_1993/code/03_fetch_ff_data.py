"""
Fama-French Data Downloader (Robust Version)
Author: Paulo Jose Araujo
Description: Downloads Fama-French data and extracts ONLY the first 
             (monthly value-weighted) section, stopping at the first blank line.
"""

import os
import urllib.request
import zipfile
import io
import pandas as pd

# --- Configuration ---
FF_FACTORS_URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'
FF_PORTFOLIOS_URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip'

OUTPUT_FACTORS = '01_fama_french_1993/data/ff_factors.csv'
OUTPUT_PORTFOLIOS = '01_fama_french_1993/data/ff_25_portfolios.csv'


def download_first_section(url, skiprows):
    """Download FF zip, unzip it, and extract ONLY the first monthly data section."""
    # 1. Download the raw zip bytes
    with urllib.request.urlopen(url) as response:
        zip_bytes = response.read()
    
    # 2. Extract the CSV text from the zip
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        csv_name = z.namelist()[0]
        csv_content = z.read(csv_name).decode('utf-8', errors='ignore')
    
    # 3. Split into lines and find the header row
    lines = csv_content.split('\n')
    header_line = lines[skiprows]
    
    # 4. Collect ONLY data rows until the first blank line
    #    This stops us from capturing the annual/equal-weighted sections below.
    data_lines = [header_line]
    for line in lines[skiprows + 1:]:
        if line.strip() == '':
            break
        data_lines.append(line)
    
    # 5. Parse into a DataFrame
    df = pd.read_csv(io.StringIO('\n'.join(data_lines)), index_col=0)
    
    # 6. Clean the index: keep only valid 6-digit YYYYMM rows
    df.index = df.index.astype(str).str.strip()
    df = df[df.index.str.match(r'^\d{6}$')]
    
    # 7. Convert index to datetime and returns to decimals
    df.index = pd.to_datetime(df.index, format='%Y%m')
    df.index.name = 'Date'
    df = df.astype(float) / 100
    
    return df


# --- Download and Process 3-Factor Data ---
print("Downloading Fama-French 3-Factor Data...")
factors_df = download_first_section(FF_FACTORS_URL, skiprows=3)
os.makedirs('01_fama_french_1993/data', exist_ok=True)
factors_df.to_csv(OUTPUT_FACTORS)
print(f"Factors saved. Shape: {factors_df.shape}")
print(f"Date range: {factors_df.index[0]} to {factors_df.index[-1]}")
print(factors_df.head())

# --- Download and Process 25 Portfolios Data ---
print("\nDownloading 25 Portfolios Data...")
portfolios_df = download_first_section(FF_PORTFOLIOS_URL, skiprows=15)
portfolios_df.to_csv(OUTPUT_PORTFOLIOS)
print(f"Portfolios saved. Shape: {portfolios_df.shape}")
print(f"Date range: {portfolios_df.index[0]} to {portfolios_df.index[-1]}")
print(portfolios_df.head())

print("\nData acquisition complete!")