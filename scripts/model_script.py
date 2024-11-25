
# Model Script for Regression Analysis
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
diabetes_df = pd.read_csv('data/diabetes_dataset.csv')

# Train-test split
X = diabetes_df[['bmi']]
y = diabetes_df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)