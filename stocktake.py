import pandas as pd
import tkinter as tk
from setup import yesterday_date, yesterday_day, yesterday_public_holiday, yesterday_is_weekend
from modeltraining import model_training
from preprocessing import pre_processing

# Return to the menu


def close(frame, open_frame, window):
    open_frame.grid_forget()
    frame.grid(row=0, column=0, sticky="nsew")
    window.title("Ordering System")


def delete_stocktake(df, frame, frame1, window):
    filtered_df = df[df["Date"] != yesterday_date]
    filtered_df.to_csv("training.csv", index=False)
    close(frame, frame1, window)

# Checks to ensure stock count isn't being done twice in a day


def check_date(df):
    if yesterday_date in df["Date"].values:
        return True
    else:
        return False


def dataset():
    df = pd.read_csv("training.csv")
    df.to_csv("backup.csv", index=False)
    df["Date"].head()
    df = df[df["Date"].notnull()]
    return df

# Take User Input


def enter(button_pressed):
    button_pressed.set(True)


def exception(char):
    return char.isdigit()


def enter_input(frame2, item_name, frame, window):
    button_pressed = tk.BooleanVar(value=False)
    validation = frame2.register(exception)
    entry = tk.Entry(frame2, validate="key",
                     validatecommand=(validation, "%S"))
    entry.grid(row=2, column=1, padx=10, pady=10)
    label = tk.Label(frame2, text=item_name)
    label.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    button = tk.Button(frame2, text="Next",
                       command=lambda: enter(button_pressed))
    button.grid(row=2, column=2, padx=10,)
    button2 = tk.Button(frame2, text="Cancel",
                        command=lambda: close(frame, frame2, window))
    button2.grid(row=2, column=3, padx=10, )
    frame2.wait_variable(button_pressed)
    try:
        current_stock = int(entry.get())
    except ValueError:
        current_stock = 0
    return current_stock


def check_sales(df, sales_entry1, frame1, window, frame):
    try:
        sales_entry = int(sales_entry1.get())
        stocktake(df, sales_entry, frame1, window, frame)
    except ValueError:
        frame1.grid_forget()
        frame3 = tk.Frame(window)
        frame3.grid()
        label1 = tk.Label(frame3, text="Invalid Sales Entry.",
                          font=("Arial", 10))
        label1.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        button1 = tk.Button(frame3, text="Back", font=(
            "Arial", 10, "bold"), command=lambda: close(frame, frame3, window))
        button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

# Run stocktake


def stocktake(df, sales_entry, frame1, window, frame):
    # Initialize counting GUI
    frame1.grid_forget()
    frame2 = tk.Frame(window)
    frame2.grid()

    is_school_holiday = 0  # IMPLEMENT APK FOR AUTOFILL. 0 BY DEFAULT

    # Get unique product names
    unique_products = df["Item Name"].dropna().unique()
    product_mapping = {i: name for i, name in enumerate(unique_products)}
    item_amount = len(product_mapping)

    data_frame = pd.DataFrame(None, index=range(item_amount), columns=[
                              "Date", "Item Name", "Sales", "DayOfWeek", "IsWeekend", "IsPublicHoliday", "IsSchoolHoliday", "Usage", "End Stock"])
    data_frame['Date'] = yesterday_date
    data_frame["Sales"] = sales_entry
    data_frame["DayOfWeek"] = yesterday_day
    data_frame["IsWeekend"] = yesterday_is_weekend
    data_frame["IsPublicHoliday"] = yesterday_public_holiday
    data_frame["IsSchoolHoliday"] = is_school_holiday

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

        current_stock = enter_input(frame2, item_name, frame, window)
        usage = int(open_stock) - current_stock
        data_frame.loc[currentItem, "Item Name"] = str(item_name)
        data_frame.loc[currentItem, "Usage"] = usage
        data_frame.loc[currentItem, "End Stock"] = current_stock
        currentItem += 1

    data_frame.to_csv("training.csv", mode="a",
                      header=False, index=False)
    pre_processing()
    model_training()

    frame2.grid_forget()
    frame3 = tk.Frame(window)
    frame3.grid()
    label = tk.Label(frame3, text="Stock Count Complete")
    label.grid(row=1, column=1, padx=10, pady=10)
    button = tk.Button(frame3, text="Back",
                       command=lambda: close(frame, frame3, window))
    button.grid(row=2, column=1, padx=10, pady=10)

# Initiate GUI


def open_stocktake(window, frame):
    # Initiate Variables
    frame.grid_forget()
    df = dataset()
    repeated_date = check_date(df)

    # Initialize GUI
    window.title("Stocktake")
    frame1 = tk.Frame(window)
    frame1.grid()

    # Continue if stock count not completed for the day
    if repeated_date:
        label1 = tk.Label(
            frame1, text="Stocktake already completed today.", font=("Arial", 10))
        label1.grid(row=1, column=1, padx=10, pady=10,
                    sticky=tk.W, columnspan=2)
        button1 = tk.Button(frame1, text="Back", font=(
            "Arial", 10, "bold"), command=lambda: close(frame, frame1, window))
        button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        button2 = tk.Button(frame1, text="Delete Last Stocktake", font=(
            "Arial", 10, "bold"), command=lambda: delete_stocktake(df, frame, frame1, window))
        button2.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

    else:
        validation = frame1.register(exception)
        sales_entry1 = tk.Entry(frame1,  validate="key",
                                validatecommand=(validation, "%S"))
        label2 = tk.Label(frame1, text="Day Sales:",
                          font=("Ariel", 10, "bold"))
        button1 = tk.Button(frame1, text="Enter", command=lambda: check_sales(
            df, sales_entry1, frame1, window, frame))
        button2 = tk.Button(frame1, text="Cancel",
                            command=lambda: close(frame, frame1, window))
        sales_entry1.grid(row=2, column=1, padx=10, sticky=tk.W)
        label2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
        button2.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W)
