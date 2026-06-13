"""
MSE803 Assessment 1 - Avon River Data Analysis
Complete code for generating all figures required for the report
Run this script in the same directory as the Excel data file
"""

# ============================================
# IMPORT REQUIRED LIBRARIES
# ============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for professional figures
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.figsize'] = (10, 7)

print("=" * 60)
print("MSE803 Assessment 1 - Data Analysis")
print("Generating figures for Avon River conservation report")
print("=" * 60)

# ============================================
# LOAD AND CLEAN THE DATA
# ============================================
file_path = 'Data_Set_Assignmnet_1-V0.1_20426.xlsx'

# Read the combined sheet and split it into the two data tables
raw_sheet = pd.read_excel(file_path, sheet_name=0, header=1)

# First 5 columns: water quality data
water_quality = raw_sheet.iloc[:, :5].copy()
water_quality.columns = ['Site_ID', 'Date', 'Temperature', 'pH', 'DO']

# Last 5 columns: fish population data
fish_data = raw_sheet.iloc[:, 6:11].copy()
fish_data.columns = ['Site_ID', 'Date', 'Species', 'Count', 'Avg_Size']

# Convert dates
water_quality['Date'] = pd.to_datetime(water_quality['Date'])
fish_data['Date'] = pd.to_datetime(fish_data['Date'])

# Handle missing values
water_quality = water_quality.dropna(subset=['Temperature', 'pH', 'DO'])
fish_data['Species'] = fish_data['Species'].fillna('Unknown')
fish_data['Count'] = fish_data['Count'].fillna(0)

# Merge datasets
merged = pd.merge(water_quality, fish_data, on=['Site_ID', 'Date'], how='inner')

print(f"\nData loaded successfully!")
print(f"Water quality records: {len(water_quality)}")
print(f"Fish records: {len(fish_data)}")
print(f"Merged records: {len(merged)}")

# ============================================
# FIGURE 1: Temperature vs Dissolved Oxygen Scatter Plot
# INSERT THIS FIGURE in Task 1-B, after introducing Multiple Linear Regression
# ============================================
print("\nGenerating Figure 1...")

plt.figure(figsize=(10, 7))

# Create scatter with bubble sizes proportional to fish count
scatter = plt.scatter(merged['Temperature'], merged['DO'], 
                      s=merged['Count']*15 + 30, 
                      c=merged['Site_ID'].astype('category').cat.codes,
                      cmap='viridis', alpha=0.7, edgecolors='black', linewidth=0.5)

# Add threshold lines
plt.axhline(y=7, color='red', linestyle='--', linewidth=2, label='DO stress threshold (7 mg/L)')
plt.axvline(x=18, color='orange', linestyle='--', linewidth=2, label='Thermal stress threshold (18°C)')

# Labels and title
plt.xlabel('Temperature (°C)', fontsize=12, fontweight='bold')
plt.ylabel('Dissolved Oxygen (mg/L)', fontsize=12, fontweight='bold')
plt.title('Figure 1: Temperature-Dissolved Oxygen Relationship Across Sites\nBubble size represents fish count', fontsize=14, fontweight='bold')

# Legend
plt.legend(loc='upper right')

# Add site labels
for site in merged['Site_ID'].unique():
    subset = merged[merged['Site_ID'] == site]
    plt.annotate(site, (subset['Temperature'].mean(), subset['DO'].mean()), 
                fontsize=10, fontweight='bold', ha='center')

plt.tight_layout()
plt.savefig('Figure1_Temp_DO_Scatter.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: Figure1_Temp_DO_Scatter.png")

# ============================================
# FIGURE 2: Regression Diagnostics (4-panel)
# INSERT THIS FIGURE in Task 1-B, after presenting MLR coefficients
# ============================================
print("\nGenerating Figure 2...")

# Prepare data for MLR
X_do = merged[['Temperature', 'pH']].dropna()
y_do = merged.loc[X_do.index, 'DO']

# Fit model
mlr_do = LinearRegression()
mlr_do.fit(X_do, y_do)
y_pred_do = mlr_do.predict(X_do)
residuals = y_do - y_pred_do

# Create 4-panel figure
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Panel A: Residuals vs Fitted
axes[0,0].scatter(y_pred_do, residuals, alpha=0.6, edgecolors='black')
axes[0,0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0,0].set_xlabel('Fitted Values (mg/L)', fontsize=11)
axes[0,0].set_ylabel('Residuals (mg/L)', fontsize=11)
axes[0,0].set_title('Figure 2A: Residuals vs Fitted', fontsize=12, fontweight='bold')

# Panel B: Q-Q Plot
stats.probplot(residuals, dist="norm", plot=axes[0,1])
axes[0,1].set_title('Figure 2B: Normal Q-Q Plot', fontsize=12, fontweight='bold')
axes[0,1].get_lines()[0].set_marker('o')
axes[0,1].get_lines()[0].set_markersize(4)

# Panel C: Histogram of Residuals
axes[1,0].hist(residuals, bins=15, edgecolor='black', alpha=0.7, color='steelblue')
axes[1,0].set_xlabel('Residuals (mg/L)', fontsize=11)
axes[1,0].set_ylabel('Frequency', fontsize=11)
axes[1,0].set_title('Figure 2C: Distribution of Residuals', fontsize=12, fontweight='bold')

# Panel D: Residuals vs Temperature
axes[1,1].scatter(merged.loc[X_do.index, 'Temperature'], residuals, alpha=0.6, edgecolors='black')
axes[1,1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1,1].set_xlabel('Temperature (°C)', fontsize=11)
axes[1,1].set_ylabel('Residuals (mg/L)', fontsize=11)
axes[1,1].set_title('Figure 2D: Residuals vs Temperature', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('Figure2_Regression_Diagnostics.png', dpi=300, bbox_inches='tight')
plt.close()

# Print model results
print("  Saved: Figure2_Regression_Diagnostics.png")
print(f"\n  === Multiple Linear Regression Results ===")
print(f"  R-squared: {r2_score(y_do, y_pred_do):.3f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_do, y_pred_do)):.3f} mg/L")
print(f"  Temperature coefficient: {mlr_do.coef_[0]:.3f} mg/L per °C")
print(f"  pH coefficient: {mlr_do.coef_[1]:.3f} mg/L per pH unit")

# ============================================
# FIGURE 3: Principal Component Analysis
# INSERT THIS FIGURE in Task 1-C, when discussing PCA biplot visualisation
# ============================================
print("\nGenerating Figure 3...")

# Prepare water quality data for PCA
wq_pca_data = water_quality[['Temperature', 'pH', 'DO']].dropna()
scaler = StandardScaler()
wq_scaled = scaler.fit_transform(wq_pca_data)

# Perform PCA
pca = PCA()
pca_scores = pca.fit_transform(wq_scaled)
explained_variance = pca.explained_variance_ratio_

# Create figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel A: Scree Plot
axes[0].bar(range(1, len(explained_variance)+1), explained_variance, 
            alpha=0.7, color='steelblue', edgecolor='black', label='Individual')
axes[0].step(range(1, len(explained_variance)+1), np.cumsum(explained_variance), 
             where='mid', label='Cumulative', color='red', linewidth=2, marker='o')
axes[0].set_xlabel('Principal Component', fontsize=11)
axes[0].set_ylabel('Explained Variance Ratio', fontsize=11)
axes[0].set_title('Figure 3A: Scree Plot', fontsize=12, fontweight='bold')
axes[0].axhline(y=0.7, color='green', linestyle='--', linewidth=1.5, label='70% threshold')
axes[0].legend()

# Panel B: Biplot
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
axes[1].scatter(pca_scores[:,0], pca_scores[:,1], alpha=0.6, edgecolors='black', c='steelblue')

# Add variable vectors
variables = ['Temperature', 'pH', 'DO']
colors_vec = ['red', 'green', 'blue']
for i, var in enumerate(variables):
    axes[1].arrow(0, 0, loadings[i,0]*3, loadings[i,1]*3, 
                  color=colors_vec[i], alpha=0.8, width=0.02, head_width=0.1)
    axes[1].text(loadings[i,0]*3.3, loadings[i,1]*3.3, var, 
                 color=colors_vec[i], fontsize=12, fontweight='bold')

axes[1].set_xlabel(f'PC1 ({explained_variance[0]*100:.1f}%)', fontsize=11)
axes[1].set_ylabel(f'PC2 ({explained_variance[1]*100:.1f}%)', fontsize=11)
axes[1].set_title('Figure 3B: PCA Biplot', fontsize=12, fontweight='bold')
axes[1].axhline(y=0, color='grey', linestyle='-', alpha=0.3)
axes[1].axvline(x=0, color='grey', linestyle='-', alpha=0.3)
axes[1].grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('Figure3_PCA_Analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Saved: Figure3_PCA_Analysis.png")
print(f"\n  === PCA Results ===")
print(f"  PC1 explains {explained_variance[0]*100:.1f}% of variance")
print(f"  PC2 explains {explained_variance[1]*100:.1f}% of variance")
print(f"  First two components explain {(explained_variance[0]+explained_variance[1])*100:.1f}%")

# ============================================
# FIGURE 4: Species Distribution Heatmap
# INSERT THIS FIGURE in Task 1-C, after tool selection justification
# ============================================
print("\nGenerating Figure 4...")

# Create pivot table of species counts by site
species_by_site = pd.crosstab(fish_data['Species'], fish_data['Site_ID'], 
                               values=fish_data['Count'], aggfunc='sum').fillna(0)

# Filter to meaningful species (remove 'Unknown' if count is 0)
species_by_site = species_by_site[species_by_site.sum(axis=1) > 0]

plt.figure(figsize=(10, 7))
sns.heatmap(species_by_site, annot=True, fmt='.0f', cmap='YlOrRd', 
            cbar_kws={'label': 'Total Fish Count'}, linewidths=1, linecolor='white')
plt.xlabel('Site ID', fontsize=12, fontweight='bold')
plt.ylabel('Species', fontsize=12, fontweight='bold')
plt.title('Figure 4: Fish Species Distribution Across Sites\nNative vs Introduced Species Comparison', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('Figure4_Species_Heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Saved: Figure4_Species_Heatmap.png")
print(f"\n  === Species Distribution Summary ===")
print(f"  Sites with native Longfin Eel: {sum(species_by_site.loc['Longfin Eel'] > 0)}")
print(f"  Sites with native Inanga: {sum(species_by_site.loc['Inanga'] > 0)}")
print(f"  Sites with introduced Brown Trout: {sum(species_by_site.loc['Brown Trout'] > 0)}")
print(f"  Total native fish count: {species_by_site.loc[['Longfin Eel', 'Shortfin Eel', 'Inanga']].sum().sum():.0f}")
print(f"  Total introduced fish count: {species_by_site.loc['Brown Trout'].sum():.0f}")

# ============================================
# FIGURE 5: Time Series Analysis (3-panel)
# INSERT THIS FIGURE in Task 1-D, before providing recommendations
# ============================================
print("\nGenerating Figure 5...")

wq_sorted = water_quality.sort_values('Date')

fig, axes = plt.subplots(3, 1, figsize=(12, 12))

# Panel A: Temperature time series
for site in wq_sorted['Site_ID'].unique():
    site_data = wq_sorted[wq_sorted['Site_ID'] == site]
    axes[0].plot(site_data['Date'], site_data['Temperature'], 
                 marker='o', linewidth=2, markersize=6, label=f'Site {site}')
axes[0].axhline(y=18, color='red', linestyle='--', linewidth=2, label='Thermal stress threshold (18°C)')
axes[0].set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
axes[0].set_title('Figure 5A: Water Temperature Trends (October-December 2023)', fontsize=12, fontweight='bold')
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# Panel B: Dissolved Oxygen time series
for site in wq_sorted['Site_ID'].unique():
    site_data = wq_sorted[wq_sorted['Site_ID'] == site]
    axes[1].plot(site_data['Date'], site_data['DO'], 
                 marker='s', linewidth=2, markersize=6, label=f'Site {site}')
axes[1].axhline(y=7, color='red', linestyle='--', linewidth=2, label='Hypoxia threshold (7 mg/L)')
axes[1].set_ylabel('Dissolved Oxygen (mg/L)', fontsize=12, fontweight='bold')
axes[1].set_title('Figure 5B: Dissolved Oxygen Trends', fontsize=12, fontweight='bold')
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

# Panel C: pH time series
for site in wq_sorted['Site_ID'].unique():
    site_data = wq_sorted[wq_sorted['Site_ID'] == site]
    axes[2].plot(site_data['Date'], site_data['pH'], 
                 marker='^', linewidth=2, markersize=6, label=f'Site {site}')
axes[2].axhline(y=7.0, color='green', linestyle='--', linewidth=2, label='Neutral pH')
axes[2].set_ylabel('pH', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Date', fontsize=12, fontweight='bold')
axes[2].set_title('Figure 5C: pH Trends', fontsize=12, fontweight='bold')
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Figure5_Timeseries.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: Figure5_Timeseries.png")

# ============================================
# FIGURE 6: Correlation Matrix
# INSERT THIS FIGURE in Task 1-D, after providing recommendations
# ============================================
print("\nGenerating Figure 6...")

# Prepare correlation data
correlation_vars = merged[['Temperature', 'pH', 'DO', 'Count']].dropna()
corr_matrix = correlation_vars.corr()

plt.figure(figsize=(8, 7))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, fmt='.2f', linewidths=1, cbar_kws={'label': 'Correlation Coefficient'},
            mask=mask, vmin=-1, vmax=1)
plt.title('Figure 6: Correlation Matrix\nWater Quality Parameters and Fish Count', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('Figure6_Correlation_Matrix.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Saved: Figure6_Correlation_Matrix.png")
print(f"\n  === Correlation Analysis ===")
print(f"  Temperature-DO correlation: {corr_matrix.loc['Temperature', 'DO']:.3f}")
print(f"  Temperature-Count correlation: {corr_matrix.loc['Temperature', 'Count']:.3f}")
print(f"  DO-Count correlation: {corr_matrix.loc['DO', 'Count']:.3f}")
print(f"  pH-Count correlation: {corr_matrix.loc['pH', 'Count']:.3f}")

# ============================================
# SUPPLEMENTARY: Summary Statistics Table
# ============================================
print("\n" + "=" * 60)
print("SUMMARY STATISTICS FOR REPORT")
print("=" * 60)

print("\n--- Water Quality by Site ---")
for site in water_quality['Site_ID'].unique():
    subset = water_quality[water_quality['Site_ID'] == site]
    print(f"\nSite {site}:")
    print(f"  Temperature: {subset['Temperature'].mean():.1f}°C (range {subset['Temperature'].min():.1f}-{subset['Temperature'].max():.1f})")
    print(f"  DO: {subset['DO'].mean():.1f} mg/L (range {subset['DO'].min():.1f}-{subset['DO'].max():.1f})")
    print(f"  pH: {subset['pH'].mean():.2f} (range {subset['pH'].min():.2f}-{subset['pH'].max():.2f})")

print("\n--- Fish Populations by Site ---")
for site in fish_data['Site_ID'].unique():
    subset = fish_data[fish_data['Site_ID'] == site]
    total_fish = subset['Count'].sum()
    species_count = subset['Species'].nunique()
    print(f"Site {site}: {total_fish:.0f} total fish, {species_count} species observed")

print("\n" + "=" * 60)
print("All figures generated successfully!")
print("The following PNG files have been saved in the current directory:")
print("  1. Figure1_Temp_DO_Scatter.png")
print("  2. Figure2_Regression_Diagnostics.png")
print("  3. Figure3_PCA_Analysis.png")
print("  4. Figure4_Species_Heatmap.png")
print("  5. Figure5_Timeseries.png")
print("  6. Figure6_Correlation_Matrix.png")
print("\nRefer to the Graph Placement Guide in the report for where to insert each figure.")
print("=" * 60)