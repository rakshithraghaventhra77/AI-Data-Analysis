"""
Data Loader Module
Handles loading and returning the Olist Orders dataset as a pandas DataFrame.
"""

import pandas as pd
from pathlib import Path


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the Olist Orders dataset from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing the dataset.
    
    Returns:
        pd.DataFrame: Loaded dataset with all records.
    
    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
        pd.errors.EmptyDataError: If the CSV file is empty.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
    
    df = pd.read_csv(file_path)
    
    return df


def get_basic_info(df: pd.DataFrame) -> dict:
    """
    Get basic information about the loaded dataset.
    
    Args:
        df (pd.DataFrame): The loaded dataset.
    
    Returns:
        dict: Dictionary containing shape, columns, and basic statistics.
    """
    info = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict()
    }
    
    return info
