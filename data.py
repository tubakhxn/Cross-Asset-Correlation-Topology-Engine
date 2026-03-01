"""
data.py
Handles data ingestion, preprocessing, and log return calculation for the Cross-Asset Correlation Topology Engine.
"""
import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Optional

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load historical price data from a CSV file.
    Expects columns as asset tickers and rows as dates.
    Returns a DataFrame indexed by date.
    """
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return df

def download_yfinance(tickers: List[str], start: str, end: str) -> pd.DataFrame:
    """
    Download historical price data from Yahoo Finance for given tickers and date range.
    Returns a DataFrame of adjusted close prices indexed by date.
    """
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    return data

def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute log returns for each asset using vectorized numpy operations.
    Returns a DataFrame of log returns indexed by date.
    """
    log_returns = np.log(prices / prices.shift(1))
    return log_returns.dropna()

def compute_rolling_correlation(log_returns: pd.DataFrame, window: int = 60) -> List[pd.DataFrame]:
    """
    Compute rolling correlation matrices over a specified window size.
    Returns a list of correlation matrices (DataFrames).
    Uses vectorized pandas operations for efficiency.
    """
    rolling_corrs = [log_returns.iloc[i:i+window].corr() for i in range(len(log_returns) - window + 1)]
    return rolling_corrs
