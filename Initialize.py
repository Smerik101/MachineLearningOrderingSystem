from datetime import timedelta, date
import holidays
import pandas as pd

##Initialize Date Data
au_holidays = holidays.country_holidays('AU', subdiv='ACT', years=2025)

#Initialize Todays Date
today_date = date.today()
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

df = pd.read_csv("TrainingSetNew.csv")
df["Item Name"] = df["Item Name"].str.strip()
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
df.to_csv("backup.csv", index=False)
df["Date"].head()
df = df[df["Date"].notnull()]