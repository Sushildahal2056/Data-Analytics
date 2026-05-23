from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd

# Load iris dataset
iris = datasets.load_iris()

# Create dataframe
iris_df = pd.DataFrame(iris.data)

# Add target column
iris_df['class'] = iris.target

# Rename columns
iris_df.columns = [
    'sepal_len',
    'sepal_wid',
    'petal_len',
    'petal_wid',
    'class'
]

# View dataset
print(iris_df.head())

# Missing values
print("\nMissing Values:")
print(iris_df.isnull().sum())

# Mean values
print("\nMean Values:")
print(iris_df.mean())

# Remove empty rows
iris_df.dropna(how="all", inplace=True)

# Features
X = iris_df.iloc[:, 0:4]

# Target
y = iris_df['class']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create SVM model
model = SVC(kernel='linear')

# Train model
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)


