# W6 Data Cleaning

This script loads the Iris dataset from `sklearn.datasets` and creates a `pandas` DataFrame.

Steps performed:
- Load the Iris dataset and convert it to a DataFrame.
- Add the target labels as a `class` column.
- Count missing values per column with `iris_df.isnull().sum()`.
- Calculate the proportion of missing data per column with `iris_df.isnull().mean()`.
- Drop rows that are completely empty with `iris_df.dropna(how="all", inplace=True)`.
- Print the first 5 rows of numeric feature columns.
- Calculate feature correlations with `iris_df.iloc[:, :4].corr()`.

The correlation matrix shows how each numeric feature relates to the others using Pearson correlation. Higher positive values mean a stronger direct relationship, and lower negative values mean a stronger inverse relationship.