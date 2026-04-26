import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV file
df = pd.read_csv("age_networth.csv")

# Preview data
print(df.head())

# Calculate correlation
correlation = df["Age"].corr(df["Net Worth"])
print("Correlation:", correlation)

# Scatter plot
plt.figure()
plt.scatter(df["Age"], df["Net Worth"])
plt.xlabel("Age")
plt.ylabel("Net Worth")
plt.title("Age vs Net Worth")

# Add regression line
x = df["Age"]
y = df["Net Worth"]

m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)

plt.show()