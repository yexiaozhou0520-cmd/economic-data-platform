"""
Economic Data Fetcher
Macroeconomic Data Collection Module for Financial Analysis
Author: Your Name
Date: 2025-05-01
"""

import pandas as pd
import numpy as np
import datetime
from pathlib import Path


def fetch_economic_data(start_date: str = "2010-01-01") -> pd.DataFrame:
    """
    Fetch macroeconomic indicators for economic analysis platform.
    Includes GDP growth, CPI, unemployment rate, policy rate and exchange rate.
    
    Args:
        start_date: Data start date
        
    Returns:
        pd.DataFrame: Structured macroeconomic time series data
    """
    # Generate monthly date range
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="M")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Simulate key economic indicators
    data = pd.DataFrame(index=dates)
    data["gdp_growth"] = np.random.normal(loc=2.5, scale=1.2, size=len(dates)).cumsum() / 10
    data["cpi_yoy"] = np.random.normal(loc=2.0, scale=0.8, size=len(dates)) + 1.0
    data["unemployment_rate"] = np.random.normal(loc=5.0, scale=0.5, size=len(dates))
    data["policy_rate"] = np.random.normal(loc=1.5, scale=0.7, size=len(dates))
    data["usd_exchange_rate"] = np.random.normal(loc=7.2, scale=0.15, size=len(dates))
    
    # Format output
    data = data.round(4)
    data.reset_index(inplace=True)
    data.rename(columns={"index": "date"}, inplace=True)
    
    return data


def save_data(df: pd.DataFrame, save_path: str = "./data/economic_data.csv"):
    """
    Save data to local CSV file.
    
    Args:
        df: Dataframe to save
        save_path: Target path
    """
    Path(save_path).parent.mkdir(exist_ok=True)
    df.to_csv(save_path, index=False, encoding="utf-8")
    print(f"Data saved to: {save_path}")


if __name__ == "__main__":
    df = fetch_economic_data()
    save_data(df)