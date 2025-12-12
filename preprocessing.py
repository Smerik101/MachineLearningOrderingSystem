import numpy as np
import pandas as pd


def pre_processing(state):
    
    # Load dataset
    df = state.df

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')
    df = df[df["Date"].notnull()]     # Remove rows with invalid or missing date
    df = df[df["Usage"].notnull() & (df["Usage"] >= 0)]     # Remove negative or missing usage values

    # Feature engineering
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Month"] = df["Date"].dt.month
    df = df.sort_values(by=["Item Name", "Date"])

    # Define numeric features
    numeric_features = ["Sales", "DayOfWeek", "Month",
                        "IsWeekend", "isSchoolHoliday", "isPublicHoliday"]
    
    if not state.feature_pref["use_weekend"]:
        numeric_features.remove("IsWeekend")
    if not state.feature_pref["use_public_holiday"]:
        numeric_features.remove("isPublicHoliday")
    if not state.feature_pref["use_school_holiday"]:
        numeric_features.remove("isSchoolHoliday")

    for item in df["Item Name"].unique():

        newdf = pd.DataFrame()
        newdf = df[df["Item Name"].isin([item])]

        # Don't attempt to predict for items with under 2 weeks of entries
        if newdf.shape[0] < 14:
            continue


        # Combine features
        X_numeric = newdf[numeric_features].values
        X=X_numeric

        # Define target
        y = newdf["Usage"].values

        # Save outputs
        np.savez(f"preprocessed/{item}.npz", X=X, y=y)



