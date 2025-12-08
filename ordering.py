import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from setup import order_days, delivery_days, order_for_days, today_day, au_holidays, model, encoder, scaler, imputer


# Convert int to day of week
def weekday_from_int(x):
    base_date = datetime(2024, 1, 1)
    return base_date + timedelta(days=x)


# Check if current day is ordering day
def check_day():
    index = order_days.index(today_day)
    start_day = delivery_days[index]
    order_days_amount = order_for_days[index]
    return start_day, order_days_amount


# Take User Input
def enter_input(day_name):
    while True:
        try:
            projected_sales = int(
                input(f"Enter projected sales for {day_name}:"))
            return projected_sales
        except ValueError:
            print("Invalid Entry. Try again")


# Get user input for day projections and parameters.
def get_inputs():
    start_day, order_days_amount = check_day()
    day_inputs = []

    for i in range(0, order_days_amount):
        public_holiday = 0
        school_holiday = 0
        future_date = weekday_from_int(start_day) + timedelta(days=i)
        day_name = future_date.strftime("%A")
        sales = enter_input(day_name)
        if future_date in au_holidays:
            public_holiday = 1

        day_inputs.append({
            "date": future_date,
            "sales": sales,
            "school_holiday": school_holiday,
            "public_holiday": public_holiday
        })
    return day_inputs


def run_calculations(df, unique_products):
    # Predict usage
    with open("buffer.txt", "r") as f:
        buffer_dict = json.load(f)
    order_window_predictions = {item: 0.0 for item in unique_products}
    for day in get_inputs():
        dow = day["date"].weekday()
        month = day["date"].month
        is_weekend = int(dow in [5, 6])

        for item in unique_products:
            categorical = encoder.transform(
                pd.DataFrame([[item]], columns=["Item Name"]))
            numeric = np.array(
                [[day["sales"], dow, month, is_weekend, day["school_holiday"], day["public_holiday"]]])
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

    order = pd.DataFrame(
        columns=["Item", "Buffer", "Current Qty", "Projected Usage", "Proposed Order Qty"])

    # Calculate order using buffers and leftover stock
    for item in unique_products:
        predicted_usage = order_window_predictions[item]
        current_stock = latest_stock[item]
        buffer = buffer_dict.get(item, 0)
        order_qty = max(0, round(predicted_usage + buffer - current_stock))
        new_row = {"Item": item, "Buffer": buffer, "Current Qty": current_stock,
                   "Projected Usage": round(predicted_usage), "Proposed Order Qty": order_qty}
        order = pd.concat([order, pd.DataFrame([new_row])], ignore_index=True)

    print(order)


def open_ordering():
    df = pd.read_csv("training.csv")
    df["Item Name"] = df["Item Name"].str.strip()
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
    unique_products = df["Item Name"].dropna().unique()

    if today_day in order_days:
        run_calculations(df, unique_products)
    else:
        print("Ordering must be done on ordering days")


open_ordering()
