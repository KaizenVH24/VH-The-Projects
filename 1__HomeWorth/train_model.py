import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("data/housing_data.csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)
print(df.head())

# -------------------------------
# Define Features & Target
# -------------------------------
X = df.drop("price", axis=1)
y = df["price"]

# -------------------------------
# Identify Column Types
# -------------------------------
categorical_cols = ["city", "location_type", "furnishing"]

numerical_cols = [
    "area_sqft",
    "bhk",
    "bathrooms",
    "parking",
    "property_age"
]

# -------------------------------
# Preprocessing
# -------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ],
    remainder="passthrough"
)

# -------------------------------
# Create Pipeline
# -------------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])

# -------------------------------
# Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# -------------------------------
# Train Model
# -------------------------------
print("\nTraining model...")
model.fit(X_train, y_train)

# -------------------------------
# Evaluate Model
# -------------------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Performance:")
print("Mean Absolute Error:", round(mae, 2))
print("R2 Score:", round(r2, 4))

# -------------------------------
# Save Model
# -------------------------------
joblib.dump(model, "models/house_price_model.pkl")

print("\nModel saved in models/house_price_model.pkl")