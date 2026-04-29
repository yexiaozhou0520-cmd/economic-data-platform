"""
Economic Data Processor
Data Cleaning and Preprocessing Module
Author: Your Name
Date: 2025-05-01
"""

import pandas as pd

def clean_economic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize raw economic data.
    
    Args:
        df: Raw economic dataframe
        
    Returns:
        pd.DataFrame: Cleaned and sorted dataframe
    """
    df_clean = df.copy()
    
    # Convert date format
    df_clean["date"] = pd.to_datetime(df_clean["date"])
    
    # Remove missing values
    df_clean = df_clean.dropna()
    
    # Sort by time
    df_clean = df_clean.sort_values("date").reset_index(drop=True)
    
    return df_clean

def load_and_clean_data(file_path: str = "./data/economic_data.csv") -> pd.DataFrame:
    """
    Load data from CSV and apply cleaning pipeline.
    
    Args:
        file_path: Path to data file
        
    Returns:
        pd.DataFrame: Final cleaned dataframe
    """
    df = pd.read_csv(file_path)
    return clean_economic_data(df)