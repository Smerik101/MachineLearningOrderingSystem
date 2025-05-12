import pickle
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load data
df = pd.read_csv("TrainingSet.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")

# Clean data
df = df[df["Usage"].notnull() & (df["Usage"] >= 0)]

# Feature engineering
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["Month"] = df["Date"].dt.month
df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)
df["Sales*Temp"] = df["Sales"] * df["Max Temp"]

# One-hot encode the "Product Name" column
encoder = OneHotEncoder(handle_unknown="ignore")
product_encoded = encoder.fit_transform(df[["Item Name"]]).toarray()

# Select numeric features
X_numeric = df[["Sales", "Max Temp", "DayOfWeek", "Month", "IsWeekend", "Sales*Temp"]].values

# Combine numerical and encoded categorical features
X_combined = np.hstack((X_numeric, product_encoded))

# Target
y = df["Usage"].values

# Impute missing values (if any) and scale numeric features
imputer = SimpleImputer(strategy="mean")
scaler = StandardScaler()

X_imputed = imputer.fit_transform(X_combined)
X_scaled = scaler.fit_transform(X_imputed)

# Save to npz
np.savez("preprocessed_data.npz", X=X_scaled, y=y)
with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("imputer.pkl", "wb") as f:
    pickle.dump(imputer, f)