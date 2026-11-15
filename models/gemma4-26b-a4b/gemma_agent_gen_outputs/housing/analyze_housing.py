import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from sklearn.preprocessing import LabelEncoder
import os

# Set style for plots
sns.set_theme(style="whitegrid")

def run_analysis():
    print("Starting analysis...")
    df = pd.read_csv('data/housing_data.csv')
    
    # Data Cleaning & Preprocessing
    # Convert categorical columns to numeric for correlation
    le = LabelEncoder()
    categorical_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
    
    df_numeric = df.copy()
    for col in categorical_cols:
        df_numeric[col] = le.fit_transform(df[col])
    
    # Furnishing status is multi-category
    df_numeric['furnishingstatus'] = le.fit_transform(df['furnishingstatus'])
    
    # 1. Statistics for Overview
    stats = df.describe().to_string()
    
    # 2. Trends & Drivers
    # Correlation matrix
    corr_matrix = df_numeric.corr()
    price_corr = corr_matrix['price'].sort_values(ascending=False)
    
    # 3. Generating Visualizations
    os.makedirs('plots', exist_ok=True)
    
    # Plot 1: Price Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], kde=True, color='blue')
    plt.title('Distribution of Housing Prices')
    plt.xlabel('Price')
    plt.savefig('plots/price_dist.png')
    plt.close()
    
    # Plot 2: Area vs Price
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='area', y='price', alpha=0.6)
    plt.title('Area vs Price')
    plt.savefig('plots/area_vs_price.png')
    plt.close()
    
    # Plot 3: Correlation Heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.savefig('plots/correlation_heatmap.png')
    plt.close()

    # Plot 4: Price by Air Conditioning
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='airconditioning', y='price')
    plt.title('Price Distribution by Air Conditioning')
    plt.savefig('plots/ac_vs_price.png')
    plt.close()

    # 4. Creating the PowerPoint
    print("Creating PowerPoint...")
    prs = Presentation()

    # Slide 1: Title
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Housing Market Executive Analysis"
    subtitle.text = "Comprehensive Data-Driven Insights\nPrepared by Momo Data Analyst"

    # Slide 2: Dataset Overview
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Dataset Overview"
    body = slide.placeholders[1]
    body.text = f"The dataset contains housing market information with following key features:\n\n{stats}"

    # Slide 3: Important Trends
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Key Market Trends"
    body = slide.placeholders[1]
    body.text = ("• Property prices show a wide range, indicating diverse market segments.\n"
                 "• There is a strong positive correlation between property area and price.\n"
                 "• Amenities like air conditioning and parking significantly impact market value.")
    
    # Adding the distribution plot to this slide or next
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # Blank layout with title
    slide.shapes.title.text = "Price Distribution"
    slide.shapes.add_picture('plots/price_dist.png', Inches(1), Inches(1.5), width=Inches(8))

    # Slide 4: Key Drivers of Price
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Key Drivers of Property Value"
    body = slide.placeholders[1]
    body.text = (f"The strongest correlations with price are:\n"
                 f"{price_corr.to_string()}\n\n"
                 "Primary drivers include size (area), parking availability, and premium location features.")

    # Adding heatmap to a new slide
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Correlation Analysis"
    slide.shapes.add_picture('plots/correlation_heatmap.png', Inches(0.5), Inches(1.2), width=Inches(9))

    # Slide 5: Visual Insights
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Visual Insights: Area & Amenities"
    
    # Adding Area vs Price
    slide.shapes.add_picture('plots/area_vs_price.png', Inches(0.5), Inches(1.5), width=Inches(4.5))
    # Adding AC vs Price
    slide.shapes.add_picture('plots/ac_vs_price.png', Inches(5), Inches(1.5), width=Inches(4.5))

    # Slide 6: Business Recommendations
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Strategic Recommendations"
    body = slide.placeholders[1]
    body.text = ("1. Focus on large area properties as they drive the highest revenue.\n"
                 "2. Prioritize inventory with air conditioning and ample parking to capture premium buyers.\n"
                 "3. Investigate high-value 'preferred area' developments for maximum ROI.\n"
                 "4. Optimize marketing for furnished/semi-furnished properties which may command better margins.")

    # Save the presentation
    prs.save('housing_analysis.pptx')
    print("Analysis complete. File saved as housing_analysis.pptx")

if __name__ == "__main__":
    run_analysis()
