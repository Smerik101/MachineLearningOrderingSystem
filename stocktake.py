import pandas as pd
import tkinter as tk
from Initialize import yesterday_date, yesterday_day, yesterday_public_holiday, yesterday_is_weekend, df

# Return to the menu
def close(stock_window, parent):
    stock_window.destroy()
    parent.deiconify()

# Checks to ensure stock count isn't being done twice in a day
def check_date():
    if yesterday_date in df["Date"].values:
        return True
    else:
        return False

# Take User Input
def enter(button_pressed):
    button_pressed.set(True)

def enter_input(frame2, item_name):
    button_pressed = tk.BooleanVar(value=False)
    validation = frame2.register(exception)
    entry = tk.Entry(frame2, validate="key", validatecommand=(validation, "%S"))
    entry.grid(row=2, column=1, padx=10, pady=10)
    label = tk.Label(frame2, text=item_name)
    label.grid(row=1, column=1, columnspan=2, padx= 10, pady=10)
    button = tk.Button(frame2, text="Next", command=lambda:enter(button_pressed))
    button.grid(row=2, column=2, padx=10,)
    button2 = tk.Button(frame2, text="Back")
    button2.grid(row=2, column=3, padx=10, pady=10)
    frame2.wait_variable(button_pressed)
    current_stock = int(entry.get())
    return current_stock

def exception(char):
    return char.isdigit()

# Run stocktake
def stocktake(sales_entry1, frame1, stock_window, parent):
    #Initialize counting GUI
    frame1.grid_forget()
    frame2 = tk.Frame(stock_window)
    frame2.grid()

    data_frame = pd.DataFrame()
    is_school_holiday = 0  # IMPLEMENT APK FOR AUTOFILL. 0 BY DEFAULT

    # Get unique product names
    unique_products = df["Item Name"].dropna().unique()
    product_mapping = {i: name for i, name in enumerate(unique_products)}
    item_amount = len(product_mapping)

    # Iterate through items
    currentItem = 0
    while currentItem < item_amount:
        item_name = product_mapping[currentItem]
        product_rows = df[df["Item Name"] == item_name]

        # Get last known End Stock as openStock
        if not product_rows.empty:
            last_row = product_rows.iloc[-1]
            open_stock = last_row["End Stock"]
        else:
            open_stock = 0

        current_stock = enter_input(frame2, item_name)

        new_data = pd.DataFrame([{
            "Date": yesterday_date,
            "Item Name": item_name,
            "Sales": int(sales_entry1.get()),
            "DayOfWeek": yesterday_day,
            "IsWeekend": yesterday_is_weekend,
            "IsPublicHoliday": yesterday_public_holiday,
            "IsSchoolHoliday": is_school_holiday,
            "Usage": open_stock - current_stock,
            "End Stock": current_stock
        }])

        data_frame = data_frame._append(new_data, ignore_index=True)
        currentItem = currentItem+1

    data_frame.to_csv("TrainingSetNew.csv", mode="a", header=False, index=False)

    frame2.grid_forget()
    frame3 = tk.Frame(stock_window)
    frame3.grid()
    label = tk.Label(frame3, text="Stock Count Complete")
    label.grid(row=1, column=1, padx=10, pady=10)
    button = tk.Button(frame3, text="Back", command=lambda: close(stock_window, parent))
    button.grid(row=2, column=1, padx=10, pady=10)

# Initiate GUI
def open_stocktake(parent):
    #Initiate Variables
    #df = dataset()
    repeated_date = check_date()

    #Initialize GUI
    stock_window = tk.Toplevel()
    stock_window.resizable(width=False, height=False)
    stock_window.title("Stocktake")
    stock_window.geometry('400x300')
    frame1 = tk.Frame(stock_window)
    frame1.grid()

    # Continue if stock count not completed for the day
    if repeated_date:
        label1 = tk.Label(frame1, text="Stocktake already completed today.", font=("Arial", 10))
        label1.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        button1 = tk.Button(frame1, text="Back", font=("Arial", 10, "bold"), command=lambda: close(stock_window, parent))
        button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    else:
        validation = frame1.register(exception)
        sales_entry1 = tk.Entry(frame1,  validate="key", validatecommand=(validation, "%S"))
        label2 = tk.Label(frame1, text="Day Sales:", font=("Ariel", 10, "bold"))
        button1 = tk.Button(frame1, text="Enter", command=lambda:stocktake(sales_entry1, frame1, stock_window, parent))
        sales_entry1.grid(row=2, column=1, padx=10, sticky=tk.W)
        label2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)



