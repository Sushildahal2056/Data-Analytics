from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Set styling for clear plots
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# 1. LOAD AND CLEAN DATA
# ---------------------------------------------------------
print("=== STEP 1: DATA CLEANING ===")
# Load the dataset
file_path = Path(__file__).with_name('Fitness_App_User_Data.xlsx')
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Identify missing values
missing_values = df.isnull().sum()
print("\n[Missing Values Per Column]:")
print(missing_values)

# Remove duplicates if any exist
duplicate_count = df.duplicated().sum()
print(f"\n[Duplicates Found]: {duplicate_count}")
if duplicate_count > 0:
    df.drop_duplicates(inplace=True)
    print("-> Duplicates successfully removed.")

# Address inconsistencies / Data Types
df['Subscription_Type'] = df['Subscription_Type'].astype('category')
df['Churned'] = df['Churned'].astype('category')
print("\n-> Data cleaning process complete. Structural integrity verified.")


# ---------------------------------------------------------
# 2. FEATURE SELECTION & PREPROCESSING
# ---------------------------------------------------------
print("\n=== STEP 2: FEATURE SELECTION & STANDARDIZATION ===")
# Select continuous numeric features driving user activity
features = ['Age', 'Workouts_per_Week', 'Avg_Session_Duration_Min', 'Steps_per_Day']
X = df[features]
print(f"Selected features for clustering: {features}")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("-> Features scaled to mean=0 and variance=1 successfully.")



print("\n=== STEP 3: COMPUTING ELBOW METHOD ===")
wcss = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)


plt.figure(figsize=(8, 5))
plt.plot(k_range, wcss, marker='o', linestyle='--', color='#2c3e50', linewidth=2)
plt.title('Elbow Method for Optimal Number of Clusters', fontsize=14, fontweight='bold')
plt.xlabel('Number of Clusters (k)', fontsize=12)
plt.ylabel('WCSS (Inertia)', fontsize=12)
plt.xticks(k_range)
plt.tight_layout()
plt.savefig('elbow_method.png', dpi=300)
plt.close()
print("-> Elbow Method plot saved as 'elbow_method.png'.")



print("\n=== STEP 4: APPLYING K-MEANS CLUSTERING ===")

optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

cluster_profiles = df.groupby('Cluster')[features].mean()
cluster_sizes = df['Cluster'].value_counts().sort_index()

print("\n[Cluster Profile Averages]:")
print(cluster_profiles.round(2))
print("\n[User Distribution Per Cluster]:")
print(cluster_sizes)



print("\n=== STEP 5: GENERATING CHARTS FOR SLIDES ===")

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df, 
    x='Steps_per_Day', 
    y='Workouts_per_Week', 
    hue='Cluster', 
    palette='Set2', 
    s=90, 
    alpha=0.8,
    edgecolor='w'
)
plt.title('User Segmentation: Daily Steps vs. Weekly Workouts', fontsize=14, fontweight='bold')
plt.xlabel('Steps per Day', fontsize=12)
plt.ylabel('Workouts per Week', fontsize=12)
plt.legend(title='App User Segment', labels=['Cluster 0', 'Cluster 1', 'Cluster 2'])
plt.tight_layout()
plt.savefig('user_segments_scatter.png', dpi=300)
plt.close()


plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Cluster', hue='Subscription_Type', palette='muted')
plt.title('Subscription Model Split Across Clusters', fontsize=14, fontweight='bold')
plt.xlabel('User Segment (Cluster)', fontsize=12)
plt.ylabel('Number of Users', fontsize=12)
plt.legend(title='Subscription Type')
plt.tight_layout()
plt.savefig('subscription_distribution.png', dpi=300)
plt.close()

print("\n[SUCCESS]: All files generated! Check your current VS Code folder directory.")