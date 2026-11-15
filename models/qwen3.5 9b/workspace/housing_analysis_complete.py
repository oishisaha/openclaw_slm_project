#!/usr/bin/env python3
"""
HOUSING MARKET ANALYSIS - Comprehensive Executive Report Generator

This script analyzes housing market data and generates insights for an executive presentation.
It produces:
1. Statistical analysis with visualizations (for PPT)
2. Key trends and price drivers
3. Business recommendations
4. PowerPoint slide deck structure (slide content in markdown format)

Author: Kiwi - Data Analyst Agent
Date: """ + datetime.now().strftime("%Y-%m-%d") + """
"""

import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime


def load_data(filepath):
    """Load and validate the housing dataset."""
    
    print("=" * 70)
    print(" " * 20, "="*58)
    print(f"HOUSING MARKET DATA ANALYSIS")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}, UTC+8 (SGT)")
    print("=" * 70)
    
    try:
        df = pd.read_csv(filepath)
        
        # Data validation summary
        missing_cols = df.columns[df.isnull().any()] if df.empty else []
        
        print(f"\n✓ Dataset loaded successfully from {filepath}")
        print(f"  • Total properties analyzed: {len(df):,}\")
        
        numeric_cols = ['price', 'area']
        categorical_cols = [c for c in df.columns 
                          if not any(x.startswith(c) or x.endswith(str(len([x for x in df.columns if isinstance(getattr(type(df), '__dict__', {}).__getitem__(len(numeric_cols))))]) and len(col)))]
