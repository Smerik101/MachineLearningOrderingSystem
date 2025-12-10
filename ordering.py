import pickle
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from appstate import au_holidays


# Convert int to day of week
def weekday_from_int(x):
    base_date = datetime(2024, 1, 1)
    return base_date + timedelta(days=x)


# Check if current day is ordering day
def check_day(state):
    index = state.order_days.index(state.today_day)
    start_day = state.delivery_days[index]
    order_days_amount = state.order_for_days[index]
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
def get_inputs(state):
    start_day, order_days_amount = check_day(state)
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


def get_data():
    with open("linear_model.joblib", "rb") as f:
        model = joblib.load(f)
    with open("encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("imputer.pkl", "rb") as f:
        imputer = pickle.load(f)
    return model, encoder, scaler, imputer


def get_array(state, day, dow, month, is_weekend):

    numeric = np.array([[day["sales"], dow, month]])
    if state.feature_pref["use_weekend"] == True:
        numeric = np.concatenate((numeric, [[is_weekend]]), axis=1)
    if state.feature_pref["use_school_holiday"] == True:
        numeric =  np.concatenate((numeric, [[day["school_holiday"]]]), axis=1)
    if state.feature_pref["use_public_holiday"] == True:
        numeric = np.concatenate((numeric, [[day["public_holiday"]]]), axis=1)
    return numeric


# Predict usage
def run_calculations(state, df):
    order_window_predictions = {item: 0.0 for item in state.unique_products}
    for day in get_inputs(state):
        dow = day["date"].weekday()
        month = day["date"].month
        is_weekend = int(dow in [5, 6])
        model, encoder, scaler, imputer = get_data()

        for item in state.unique_products:
            categorical = encoder.transform(
                pd.DataFrame([[item]], columns=["Item Name"]))
            numeric = get_array(state, day, dow, month, is_weekend)
            combined = np.hstack((numeric, categorical))
            combined_imputed = imputer.transform(combined)
            combined_scaled = scaler.transform(combined_imputed)
            usage_pred = max(0, model.predict(combined_scaled)[0])
            order_window_predictions[item] += usage_pred

    # Fetch leftover stock (last end stock from last count)
    latest_stock = {}
    for item in state.unique_products:
        product_data = df[df["Item Name"] == item]
        if not product_data.empty:
            last_row = product_data.sort_values("Date").iloc[-1]
            latest_stock[item] = last_row.get("End Stock", 0)
        else:
            latest_stock[item] = 0

    order = pd.DataFrame(
        columns=["Item", "Buffer", "Current Qty", "Projected Usage", "Proposed Order Qty"])

    # Calculate order using buffers and leftover stock
    for item in state.unique_products:
        predicted_usage = order_window_predictions[item]
        current_stock = latest_stock[item]
        buffer = state.buffer_dict.get(item, 0)
        order_qty = max(0, round(predicted_usage + buffer - current_stock))
        new_row = {"Item": item, "Buffer": buffer, "Current Qty": current_stock,
                   "Projected Usage": round(predicted_usage), "Proposed Order Qty": order_qty}
        order = pd.concat([order, pd.DataFrame([new_row])], ignore_index=True)

    print(order)


def open_ordering(state):
    df = state.df
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")

    if state.today_day in state.order_days:
        run_calculations(state, df)
    else:
        print("Ordering must be done on ordering days")
