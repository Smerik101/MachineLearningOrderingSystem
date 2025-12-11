import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


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

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    for item in df["Item Name"].unique():

        newdf = pd.DataFrame()
        newdf = df[df["Item Name"].isin([item])]

        # Don't attempt to predict for items with under 2 weeks of entries
        if newdf.shape[0] < 14:
            continue

        # One-hot encode the item name
        product_encoded = encoder.fit_transform(newdf[["Item Name"]])

        # Combine features
        X_numeric = newdf[numeric_features].values
        X_combined = np.hstack((X_numeric, product_encoded))

        # Define target
        y = newdf["Usage"].values

        # Save outputs
        np.savez(f"preprocessed/{item}.npz", X=X_combined, y=y)
    
    with open("encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)


