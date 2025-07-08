import pickle
from datetime import timedelta, date
import holidays
import tkinter as tk
from tkinter import messagebox
import json

##Initialize Date Data
au_holidays = holidays.country_holidays('AU', subdiv='ACT', years=2025)

#Initialize Todays Date
today_date = date.today()#Change day for troubleshooting
today_day = today_date.weekday()

if today_date.weekday() == 6 or today_date.weekday() == 5:
    is_weekend = 1
else:
    is_weekend = 0

if today_date in au_holidays:
    public_holiday = 1
else:
    public_holiday = 0

#Initialize Yesterdays Date
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

## Buffer Setup
with open("data.txt", "r") as f:
    buffer_dict = json.load(f)

## Order Delivery Setup
order_days = (1, 5 ) #Days ordering is completed
delivery_delay = 3 #Time for order to arrive

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

with open("linear_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("imputer.pkl", "rb") as f:
    imputer = pickle.load(f)
#with open("data.txt", "w") as f: ##FOR MODIFYING BUFFERS
#    json.dump(buffer_dict, f)

def close(frame, open_frame):
    open_frame.grid_forget()
    frame.grid(row=0, column=0, sticky="nsew")

def setup(frame1, frame, window):
    frame1.grid_forget()
    frame2 = tk.Frame(window)
    frame2.grid()
    Label1 = tk.Label(frame2, text="Setup", font=("Ariel", 10, "bold"))
    Label1.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)
    Button1 = tk.Button(frame2, text="Item Setup")
    Button1.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
    Button2 = tk.Button(frame2, text="Order Timing Setup")
    Button2.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
    Button3 = tk.Button(frame2, text="Cancel", command=lambda: close(frame, frame2))
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
    button1 = tk.Button(frame1, text="Enter", command = lambda:enter(frame1, frame, window, password_entry))
    button2 = tk.Button(frame1, text="Cancel", command=lambda:close(frame, frame1))
    password_entry.grid(row=2, column=1, padx=10, sticky=tk.W)
    label2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
    button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
    button2.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W)

    """buffer_dict = {
        "BUN REGULAR": 100,
        "MUFFIN ENGLISH": 100,
        "BUN 4 INCH": 80,
        "BUN BIG MAC": 60,
        "BUN MCCRISPY": 30,
        "BUN GOURMET": 30,
    }"""