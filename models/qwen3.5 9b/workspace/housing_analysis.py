#!/usr/bin/env python3
"""
Housing Market Analysis Script
Comprehensive analysis of housing market data with executive slide deck generation.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def load_and_analyze_data(filepath):
    """Load dataset and perform comprehensive statistical analysis."""
    
    print("=" * 60)
    print("HOUSING MARKET DATA ANALYSIS")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(filepath, dtype={
        'mainroad': str, 
        'guestroom': str, 
        'basement': str, 
        'hotwaterheating': str,
        'airconditioning': str,
        'parking': int,  # Already numeric from CSV parsing context
        'prefarea': str,
        'furnishingstatus': str
    })
    
    print(f"\nDataset loaded: {len(df)} properties")
    print(f"Columns: {list(df.columns)}\n")
    
    # Basic statistics for price analysis (in millions)
    df['price_million'] = df['price'] / 1_000_000
    
    print("=" * 60)
    print("SECTION 1: DATASET OVERVIEW")
    print("=" * 60)
    
    # Descriptive statistics for price (in millions)
    price_stats = {
        'Metric': ['Total Properties', 
                    f"Price Range",
                    "Median Price ($M)",
                    "Mean Price ($M)",
                    "Mode: Most Common Class"],
        
        'Value': [len(df),
                   f"${df['price'].min()/1_000_000:.2f} - ${df['price'].max()/1_000_000:.2f}",
                   round(float(np.percentile(df['price'], 50))/1_000_000, 3),
                   round(float(np.mean(df['price']))/1_000_000, 3),
                   'Low: $4.6M - Mid: $7.8M - High: $29.5M']
    }
    
    print("\nPRICE DISTRIBUTION")
    for metric, value in zip(price_stats['Metric'], price_stats['Value']):
        if isinstance(value, float) or 'Range' not in str(value):
            print(f"  • {metric}: ${value:.2f}M")
        
    # Price class distribution (in millions: Low <$15M, Mid $15-30M, High>$30M)
    price_bins = pd.cut(df['price'], 
                        bins=[4_600_000, 15_000_000, 29_700_000, float('inf')],
                        labels=['Low', 'Mid', 'High'])
    print(f"\nPRICE CLASS DISTRIBUTION")
    for class_name in ['Low (<$15M)', 
                       f"Medium ($15-30M)",
                       "High (> $29.7M)"]:
        count = len(price_bins[price_bins == class_name.replace(' ', '').split()[0] if '$' not in class_name else class_name.split('(')[1].rstrip(')').replace('<', ' ').strip('$')])  # Complex parsing - use simple approach below
        
    print("\nPRICE CLASS BREAKDOWN:")
    
    low_count = len(df[df['price'] <= 15_000_000])
    mid_count = len((df > 7.8M and df < 30) & df) 
    
