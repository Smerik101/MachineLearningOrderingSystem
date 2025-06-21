import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import tkinter as tk

#Ordering setup for twice a week deliveries.
#Setup for ordering Monday, and early delivery Tuesday.
#Setup for ordering Thursday and early delivery Friday.
#Modify parameters below to change.

def day_of_week():
    return datetime.now().weekday()-1


def check_day():
    today = day_of_week()
    if today == 0:  # Monday → Tues, Wed, Thurs
        return 3
    elif today == 3:  # Thursday → Fri, Sat, Sun, Mon
        return 4
    else:
        print("Ordering must be done on ordering day")
        sys.exit()


#Get user input for day projections and parameters.
def get_inputs():
    day_inputs = []
    for i in range(1, check_day() + 1):
        future_date = datetime.now() + timedelta(days=i)
        day_name = future_date.strftime("%A")  # e.g., 'Tuesday'

        sales = int(input(f"Projected sales for {day_name}? "))
        school_holiday = int(input(f"Is {day_name} a school holiday? (1=Yes, 0=No): "))
        public_holiday = int(input(f"Is {day_name} a public holiday? (1=Yes, 0=No): "))

        day_inputs.append({
            "date": future_date,
            "sales": sales,
            "school_holiday": school_holiday,
            "public_holiday": public_holiday
        })
    return day_inputs


#Setup Buffers for each product.
def custom_buffers(item):
    buffer_dict = {
        "BUN REGULAR": 100,
        "MUFFIN ENGLISH": 100,
        "BUN 4 INCH": 80,
        "BUN BIG MAC": 60,
        "BUN MCCRISPY": 30,
        "BUN GOURMET": 30,
    }
    return buffer_dict.get(item, 0)


def run_calculations(df, unique_products, imputer, scaler, encoder, model):
        # Predict usage
        order_window_predictions = {item: 0.0 for item in unique_products}
        for day in get_inputs():
            dow = day["date"].weekday()
            month = day["date"].month
            is_weekend = int(dow in [5, 6])

            for item in unique_products:
                categorical = encoder.transform(pd.DataFrame([[item]], columns=["Item Name"]))
                numeric = np.array([[day["sales"], dow, month, is_weekend,
                                         day["school_holiday"], day["public_holiday"]]])
                combined = np.hstack((numeric, categorical))
                combined_imputed = imputer.transform(combined)
                combined_scaled = scaler.transform(combined_imputed)
                usage_pred = max(0, model.predict(combined_scaled)[0])
                order_window_predictions[item] += usage_pred

        # Fetch leftover stock (last end stock from last count)
        latest_stock = {}
        for item in unique_products:
            product_data = df[df["Item Name"] == item]
            if not product_data.empty:
                last_row = product_data.sort_values("Date").iloc[-1]
                latest_stock[item] = last_row.get("End Stock", 0)
            else:
                latest_stock[item] = 0

        # Calculate order using buffers and leftover stock
        print(f"\nProposed Order Quantity")
        for item in unique_products:
            predicted_usage = order_window_predictions[item]
            current_stock = latest_stock[item]
            buffer = custom_buffers(item)
            order_qty = max(0, round(predicted_usage + buffer - current_stock))
            print(
                f"{item}: Order {order_qty} units (Predicted={round(predicted_usage, 2)}, Current={current_stock}, Buffer={buffer})")


def open_ordering(parent):
    df = pd.read_csv("TrainingSetNew.csv")
    df["Item Name"] = df["Item Name"].str.strip()
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
    unique_products = df["Item Name"].dropna().unique()

    with open("linear_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("imputer.pkl", "rb") as f:
        imputer = pickle.load(f)

    run_calculations(df, unique_products, imputer, scaler, encoder, model)