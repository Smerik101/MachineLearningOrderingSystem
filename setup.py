import pickle
from datetime import timedelta, date
import holidays
import tkinter as tk
from tkinter import messagebox, ttk
import json
import joblib

#### DATA TO BE INITIALIZED UPON PROGRAM OPEN####

# Initialize Date Data
au_holidays = au = holidays.Australia(state='ACT', years=2025)

# Initialize Todays Date
today_date = date.today()
# today_date -= timedelta(days=1) #LINE FOR TROUBLESHOOTING
today_day = today_date.weekday()

if today_date.weekday() == 6 or today_date.weekday() == 5:
    is_weekend = 1
else:
    is_weekend = 0

if today_date in au_holidays:
    public_holiday = 1
else:
    public_holiday = 0

# Initialize Yesterdays Date
yesterday_date = today_date - timedelta(days=1)
yesterday_day = yesterday_date.weekday()

if yesterday_date.weekday() == 6 or yesterday_date.weekday() == 5:
    yesterday_is_weekend = 1
else:
    yesterday_is_weekend = 0

if yesterday_date in au_holidays:
    yesterday_public_holiday = 1
else:
    yesterday_public_holiday = 0

yesterday_date = yesterday_date.strftime("%d/%m/%Y")
today_date = today_date.strftime("%d/%m/%Y")

# Order Delivery Setup
order_days = (1, 5)  # Days ordering is completed
delivery_delay = 3  # Time for order to arrive

delivery_days = []
for i in range(len(order_days)):
    x = order_days[i] + delivery_delay
    if x > 6:
        x = x-7
    delivery_days.append(x)

order_for_days = []
for i in range(len(delivery_days)):
    x = delivery_days[i]
    x = x+1
    y = 1
    while x not in delivery_days:
        y = y+1
        x = x+1
        if x > 6:
            x = x-7
    order_for_days.append(y)

with open("linear_model.joblib", "rb") as f:
    model = joblib.load(f)
with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("imputer.pkl", "rb") as f:
    imputer = pickle.load(f)
with open("buffer.txt", "r") as f:
    buffer_dict = json.load(f)

#### DATA TO BE INITIALIZED UPON PROGRAM OPEN####


def close(frame, open_frame, window):
    open_frame.grid_forget()
    frame.grid(row=0, column=0, sticky="nsew")
    window.geometry('400x300')
    window.title("Ordering System")


def modify_buffer(frame, frame2, window):
    frame2.grid_forget()
    top_frame = tk.Frame(window)
    top_frame.grid()

    def refresh_tree():
        for item in tree.get_children():
            tree.delete(item)
        for key, value in buffer_dict.items():
            tree.insert("", "end", values=(key, value))

    def add_or_update():
        key = label_text.get()
        value = int(value_entry.get())
        if key:
            buffer_dict[key] = value
            refresh_tree()
            with open("buffer.txt", "w") as f:
                json.dump(buffer_dict, f)

    def on_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            key = item['values'][0]
            value = item['values'][1]
            label_text.set(key)
            value_entry.delete(0, tk.END)
            value_entry.insert(0, value)

    label_text = tk.StringVar()
    tree = ttk.Treeview(top_frame, columns=("Key", "Value"), show="headings")
    tree.heading("Key", text="Key")
    tree.heading("Value", text="Value")
    tree.grid(row=0, column=0, columnspan=3)

    tk.Label(top_frame, text="Key:").grid(row=1, column=0)
    key_entry = tk.Label(top_frame, textvariable=label_text)
    key_entry.grid(row=1, column=1)

    tk.Label(top_frame, text="Value:").grid(row=2, column=0)
    value_entry = tk.Entry(top_frame)
    value_entry.grid(row=2, column=1)

    # Buttons
    tk.Button(top_frame, text="Update",
              command=add_or_update).grid(row=1, column=2)
    tk.Button(top_frame, text="Done", command=lambda: close(
        frame, top_frame, window)).grid(row=2, column=2)
    window.geometry("")
    tree.bind("<<TreeviewSelect>>", on_select)
    refresh_tree()


def setup(frame1, frame, window):
    frame1.grid_forget()
    frame2 = tk.Frame(window)
    frame2.grid()
    Label1 = tk.Label(frame2, text="Setup", font=("Ariel", 10, "bold"))
    Label1.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)
    Button1 = tk.Button(frame2, text="Modify Buffers",
                        command=lambda: modify_buffer(frame, frame2, window))
    Button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
    Button2 = tk.Button(frame2, text="Order Timing Setup")
    Button2.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
    Button3 = tk.Button(frame2, text="Cancel",
                        command=lambda: close(frame, frame2, window))
    Button3.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W)


def enter(frame1, frame, window, password_entry):
    password = "1234"
    entered_password = password_entry.get()

    if entered_password == password:
        setup(frame1, frame, window)
    else:
        messagebox.showinfo("Password Entry", "Incorrect Password")


def open_setup(window, frame):
    frame.grid_forget()
    window.title("Setup")
    frame1 = tk.Frame(window)
    frame1.grid()

    password_entry = tk.Entry(frame1, validate="key", show="*")
    label2 = tk.Label(frame1, text="Password:", font=("Ariel", 10, "bold"))
    button1 = tk.Button(frame1, text="Enter", command=lambda: enter(
        frame1, frame, window, password_entry))
    button2 = tk.Button(frame1, text="Cancel",
                        command=lambda: close(frame, frame1, window))
    password_entry.grid(row=2, column=1, padx=10, sticky=tk.W)
    label2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
    button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
    button2.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W)
