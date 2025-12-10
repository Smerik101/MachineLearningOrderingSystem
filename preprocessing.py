import pickle
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def pre_processing(state):
    
    # Load dataset
    df = state.df
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')

    # Remove rows with invalid or missing date
    df = df[df["Date"].notnull()]
    # Remove negative or missing usage values
    df = df[df["Usage"].notnull() & (df["Usage"] >= 0)]

    # Feature engineering
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Month"] = df["Date"].dt.month
    df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)
    df["isSchoolHoliday"] = df["isSchoolHoliday"].fillna(0).astype(int)
    df["isPublicHoliday"] = df["isPublicHoliday"].fillna(0).astype(int)
    df = df.sort_values(by=["Item Name", "Date"])

    # Define numeric features
    numeric_features = ["Sales", "DayOfWeek", "Month",
                        "IsWeekend", "isSchoolHoliday", "isPublicHoliday"]
    
    if state.feature_pref["use_weekend"] == False:
        numeric_features.remove("IsWeekend")
    if state.feature_pref["use_public_holiday"] == False:
        numeric_features.remove("isPublicHoliday")
    if state.feature_pref["use_school_holiday"] == False:
        numeric_features.remove("isSchoolHoliday")

    # One-hot encode the item name
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    product_encoded = encoder.fit_transform(df[["Item Name"]])

    # Combine features
    X_numeric = df[numeric_features].values
    X_combined = np.hstack((X_numeric, product_encoded))

    # Define target
    y = df["Usage"].values

    # Impute and scale
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()
    X_imputed = imputer.fit_transform(X_combined)
    X_scaled = scaler.fit_transform(X_imputed)

    # Save outputs
    np.savez("preprocessed_data.npz", X=X_scaled, y=y)
    with open("encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    with open("imputer.pkl", "wb") as f:
        pickle.dump(imputer, f)

