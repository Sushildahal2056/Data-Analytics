import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Create folders
if not os.path.exists('charts'): os.makedirs('charts')

# 1. Load Data
df = pd.read_csv('messy_dataset_Mukesh.csv')

# 2. Cleaning: Handle "thirty-eight" and Duplicates
df.drop_duplicates(inplace=True)
word_map = {'thirty-eight': 38}
df['Age'] = df['Age'].replace(word_map)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
df.fillna(df.median(numeric_only=True), inplace=True)

# --- GENERATE THE 5 CHARTS ---

# Chart 1: Missing Data
plt.figure(figsize=(6,4))
sns.heatmap(df.isnull(), cbar=False).set_title("Missing Data Map")
plt.savefig('charts/chart1_missing.png')

# Chart 2: Scatter Plot (Age vs Salary)
plt.figure(figsize=(6,4))
sns.regplot(x='Age', y='Salary', data=df)
plt.savefig('charts/chart2_scatter.png')

# Chart 3: Heatmap (Pearson)
plt.figure(figsize=(6,4))
sns.heatmap(df.corr(method='pearson', numeric_only=True), annot=True, cmap='RdYlGn')
plt.savefig('charts/chart3_heatmap.png')
plt.savefig('image.png') # Main image for README

# Chart 4: Boxplots
plt.figure(figsize=(6,4))
sns.boxplot(data=df[['Age', 'Salary']])
plt.savefig('charts/chart4_boxplots.png')

# Chart 5: Z-Score/Distribution
plt.figure(figsize=(6,4))
sns.histplot(df['Salary'], kde=True)
plt.savefig('charts/chart5_country_zscore.png')

print("All 5 charts generated successfully.")