import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import tkinter as tk
from Initialize import buffer_dict, order_days, delivery_days, order_for_days, today_day, au_holidays, df

def close(stock_window, parent):
    stock_window.destroy()
    parent.deiconify()

def day_of_week():
    return datetime.now().weekday()

def weekday_from_int(x): #Convert int to day of week
    base_date = datetime(2024, 1, 1)
    return base_date + timedelta(days=x)

def check_day():
    if today_day in order_days:
        index = order_days.index(today_day)
        start_day = delivery_days[index]
        order_days_amount = order_for_days[index]
        return start_day, order_days_amount

    else:
        print("Ordering must be done on ordering day")
        sys.exit()

#Get user input for day projections and parameters.
def get_inputs():
    start_day, order_days_amount = check_day()
    day_inputs = []
    for i in range(0, order_days_amount):
        future_date = weekday_from_int(start_day) + timedelta(days=i)
        day_name = future_date.strftime("%A")

        sales = int(input(f"Projected sales for {day_name}? "))
        school_holiday = int(input(f"Is {day_name} a school holiday? (1=Yes, 0=No): "))
        public_holiday = 0
        if future_date in au_holidays:
            public_holiday = 1

        day_inputs.append({
            "date": future_date,
            "sales": sales,
            "school_holiday": school_holiday,
            "public_holiday": public_holiday
        })
    return day_inputs

def run_calculations(unique_products, imputer, scaler, encoder, model):
        # Predict usage
        order_window_predictions = {item: 0.0 for item in unique_products}
        for day in get_inputs():
            dow = day["date"].weekday()
            month = day["date"].month
            is_weekend = int(dow in [5, 6])

            for item in unique_products:
                categorical = encoder.transform(pd.DataFrame([[item]], columns=["Item Name"]))
                numeric = np.array([[day["sales"], dow, month, is_weekend, day["school_holiday"], day["public_holiday"]]])
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
            buffer = buffer_dict.get(item, 0)
            order_qty = max(0, round(predicted_usage + buffer - current_stock))
            print(
                f"{item}: Order {order_qty} units (Predicted={round(predicted_usage, 2)}, Current={current_stock}, Buffer={buffer})")

def open_ordering(parent):
    unique_products = df["Item Name"].dropna().unique()

    with open("linear_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("imputer.pkl", "rb") as f:
        imputer = pickle.load(f)

    order_window = tk.Toplevel()
    order_window.title("Propose Order")
    order_window.geometry('400x300')
    order_window.resizable(width=False, height=False)
    frame1 = tk.Frame(order_window)
    frame1.grid()
    Label1 = tk.Label(frame1, text="Propose Order", font=("Ariel", 10, "bold"))
    Label1.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)
    Button1 = tk.Button(frame1, text="Calculate Order", command=lambda:run_calculations(unique_products, imputer, scaler, encoder, model))
    Button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
    Button2 = tk.Button(frame1, text="Cancel", command=lambda: close(order_window, parent))
    Button2.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

