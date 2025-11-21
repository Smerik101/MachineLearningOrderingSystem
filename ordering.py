import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from setup import order_days, delivery_days, order_for_days, today_day, au_holidays, model, encoder, scaler, imputer


def close_order_screen(frame, open_frame, open_frame2, window):
    open_frame.pack_forget()
    open_frame2.pack_forget()
    frame.grid(row=0, column=0, sticky="nsew")
    window.geometry('400x300')
    window.title("Ordering System")


def close(frame, open_frame):
    open_frame.grid_forget()
    frame.grid(row=0, column=0, sticky="nsew")


def weekday_from_int(x):  # Convert int to day of week
    base_date = datetime(2024, 1, 1)
    return base_date + timedelta(days=x)


def check_day():
    index = order_days.index(today_day)
    start_day = delivery_days[index]
    order_days_amount = order_for_days[index]
    return start_day, order_days_amount

# Take User Input


def enter(button_pressed, entry):
    value = entry.get().strip()
    if not value:
        messagebox.showinfo(
            "Missing Input", "Please enter a value before continuing!")
    else:
        button_pressed.set(True)


def exception(char):
    return char.isdigit()


def enter_input(frame, day_name, frame2):
    button_pressed = tk.BooleanVar(value=False)
    validation = frame2.register(exception)
    entry = tk.Entry(frame2, validate="key",
                     validatecommand=(validation, "%S"))
    entry.grid(row=2, column=1, padx=10, pady=10)
    label = tk.Label(frame2, text="Enter projected sales for:")
    label.grid(row=1, column=1, columnspan=2, pady=10)
    label2 = tk.Label(frame2, text=day_name)
    label2.grid(row=1, column=2, columnspan=2, pady=10)
    button = tk.Button(frame2, text="Next",
                       command=lambda: enter(button_pressed, entry))
    button.grid(row=2, column=2, padx=10, )
    button2 = tk.Button(frame2, text="Cancel",
                        command=lambda: close(frame, frame2))
    button2.grid(row=2, column=3, padx=10, )
    frame2.wait_variable(button_pressed)
    projected_sales = int(entry.get())
    return projected_sales

# Get user input for day projections and parameters.


def get_inputs(window, frame, frame1):
    start_day, order_days_amount = check_day()
    day_inputs = []
    frame1.grid_forget()
    frame2 = tk.Frame(window)
    frame2.grid()

    for i in range(0, order_days_amount):
        public_holiday = 0
        school_holiday = 0
        future_date = weekday_from_int(start_day) + timedelta(days=i)
        day_name = future_date.strftime("%A")
        sales = enter_input(frame, day_name, frame2)
        if future_date in au_holidays:
            public_holiday = 1

        day_inputs.append({
            "date": future_date,
            "sales": sales,
            "school_holiday": school_holiday,
            "public_holiday": public_holiday
        })
    frame2.grid_forget()
    return day_inputs


def run_calculations(df, unique_products, frame, window, frame1):
    # Predict usage
    with open("buffer.txt", "r") as f:
        buffer_dict = json.load(f)
    order_window_predictions = {item: 0.0 for item in unique_products}
    for day in get_inputs(window, frame, frame1):
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

    top_frame = tk.Frame(window)
    top_frame.pack(side="top", fill="both", expand=True)
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(side="top", fill="x")

    columns = list(order.columns)
    tree = ttk.Treeview(top_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    # Insert rows from DataFrame
    for _, row in order.iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.pack(padx=10, fill="both", expand=True)

    button2 = tk.Button(bottom_frame, text="Close", command=lambda: close_order_screen(
        frame, top_frame, bottom_frame, window))
    button2.pack(side="bottom", padx=10, pady=10)
    button3 = tk.Button(bottom_frame, text="Submit")
    button3.pack(side="bottom", padx=10, pady=10)
    window.update_idletasks()
    window.geometry("")


def open_ordering(window, frame):
    frame.grid_forget()
    df = pd.read_csv("TrainingSetNew.csv")
    df["Item Name"] = df["Item Name"].str.strip()
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
    unique_products = df["Item Name"].dropna().unique()
    window.title("Propose Order")
    frame1 = tk.Frame(window)
    frame1.grid()

    if today_day in order_days:
        Label1 = tk.Label(frame1, text="Propose Order",
                          font=("Ariel", 10, "bold"))
        Label1.grid(row=1, column=1, padx=10, pady=10,
                    columnspan=2, sticky=tk.W)
        Button1 = tk.Button(frame1, text="Calculate Order", command=lambda: run_calculations(
            df, unique_products, frame, window, frame1))
        Button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        Button2 = tk.Button(frame1, text="Cancel",
                            command=lambda: close(frame, frame1))
        Button2.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
    else:
        label1 = tk.Label(
            frame1, text="Ordering must be completed on ordering days", font=("Arial", 10))
        label1.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        button1 = tk.Button(frame1, text="Back", font=(
            "Arial", 10, "bold"), command=lambda: close(frame, frame1))
        button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
