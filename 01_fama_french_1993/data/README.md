# Project 01: Fama & French (1993) - Common Risk Factors

## Project Overview
This project replicates the foundational asset pricing models of Fama & French (1993). Before diving into stock returns, this initial phase builds a macroeconomic data pipeline to understand the broader economic environment.

## Data Pipeline Structure
1. **`code/macro_data_pipeline.py`**: Fetches raw GDP, Unemployment Rate, and CPI data from the Federal Reserve Economic Data (FRED) API.
2. **`code/01_data_cleaning.py`**: Resamples the raw data to a uniform quarterly frequency, calculates Year-over-Year (YoY) growth rates, and removes missing values.
3. **`code/02_data_visualization.py`**: Generates a multi-panel dashboard of the cleaned data.

## Key Transformations
- **Resampling:** Monthly data (UNRATE, CPI) is averaged to match the quarterly frequency of GDP.
- **Growth Rates:** GDP and CPI are converted to YoY percentage changes to ensure stationarity and comparability.
- **Missing Data:** Rows with insufficient historical data are dropped.

## Results
![Macro Dashboard](output/macro_dashboard.png)

## How to Run
1. Set your FRED API key as an environment variable.
2. Run `python 01_fama_french_1993/code/macro_data_pipeline.py` to fetch the raw data.
3. Run `python 01_fama_french_1993/code/01_data_cleaning.py` to generate the cleaned dataset.
4. Run `python 01_fama_french_1993/code/02_data_visualization.py` to generate the dashboard.

# Data Directory

This directory is intentionally left empty of CSV files due to GitHub's file size limits and best practices for reproducible research.

To generate the data for this project, run the following script from the repository root:
`python 01_fama_french_1993/code/03_fetch_ff_data.py`

This script will automatically download and clean the Fama-French 3-Factor and 25 Size/Book-to-Market portfolio data from Kenneth French's Dartmouth Library.