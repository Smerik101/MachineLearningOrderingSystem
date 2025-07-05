import pickle
from datetime import timedelta, date
import holidays
import pandas as pd

##Initialize Date Data
au_holidays = holidays.country_holidays('AU', subdiv='ACT', years=2025)

#Initialize Todays Date
today_date = date.today() - timedelta(days=1)#Change day for troubleshooting
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
buffer_dict = {
    "BUN REGULAR": 100,
    "MUFFIN ENGLISH": 100,
    "BUN 4 INCH": 80,
    "BUN BIG MAC": 60,
    "BUN MCCRISPY": 30,
    "BUN GOURMET": 30,
}

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

