import pandas as pd
import re

def clean_indicator_name(indicator):
    """Clean indicator name by removing unit"""
    return re.sub(r'\n.+$', '', indicator)

def extract_unit(indicator_list):
    """Extract unit from indicator names"""
    units = set()
    for ind in indicator_list:
        match = re.search(r'\n(.+)', ind)
        if match:
            units.add(match.group(1))
    return ', '.join(units) if units else ''

import re

def clean_indicator_name(ind):
    """Remove trailing units (e.g. '\n%' or '\nLần')"""
    return re.sub(r'\n.+$', '', ind)


def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

import pandas as pd
import numpy as np

def advanced_preprocess(df):
    df = df.copy()

    # Tìm cột ngày
    if 'Date' not in df.columns:
        possible = [col for col in df.columns if 'date' in col.lower() or 'ngày' in col.lower()]
        if possible:
            df.rename(columns={possible[0]: 'Date'}, inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y", errors="coerce")

    numeric_cols = [
        "Total Volume", "Total Value", "Market Cap",
        "Closing Price", "Price Change", "Matched Volume", "Matched Value"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "")
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=['Date', 'Closing Price'], inplace=True)
    df = df.sort_values("Date").reset_index(drop=True)

    return df


def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
