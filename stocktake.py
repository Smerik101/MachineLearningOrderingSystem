from datetime import timedelta
import sys
import pandas as pd
import datetime

#Load dataset
df = pd.read_csv("TrainingSetNew.csv")
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
df = df[df["Date"].notnull()]  # remove rows with bad dates
yesterday = datetime.datetime.now() - timedelta(days=1)
isWeekend = 0
if yesterday.weekday() == 5 or yesterday.weekday() == 6:
    isWeekend = 1
date = pd.to_datetime(datetime.date.today() - timedelta(days=1))
if (df["Date"].dt.date == date.date()).any():
    print(f"Stocktake data for date {date.date()} already exists.")
    sys.exit()

# Get unique product names
unique_products = df["Item Name"].dropna().unique()
product_mapping = {i: name for i, name in enumerate(unique_products)}
itemAmount = len(product_mapping)

#Take user inputs
sales = int(input("Day Sales: "))
isPublicHoliday = int(input("Was it public holiday? (1=Yes, 0=No)"))
isSchoolHoliday = int(input("Was it school holiday? (1=Yes, 0=No)"))

#Iterate through items
for currentItem in range(itemAmount):
    item_name = product_mapping[currentItem]
    product_rows = df[df["Item Name"].str.contains(item_name, na=False)]

    #Get last known End Stock as openStock
    if not product_rows.empty:
        last_row = product_rows.iloc[-1]
        openStock = last_row["End Stock"]
    else:
        openStock = 0

    print(f"\n{item_name}")
    currentStock = int(input("Stock Count: "))

    new_data = pd.DataFrame([{
        "Date": date,
        "Item Name": item_name,
        "Sales": sales,
        "DayOfWeek": yesterday.weekday(),
        "IsWeekend": isWeekend,
        "IsPublicHoliday": isPublicHoliday,
        "IsSchoolHoliday": isSchoolHoliday,
        "Usage": openStock - currentStock,
        "End Stock": currentStock
    }])

    new_data.to_csv("TrainingSetNew.csv", mode="a", header=False, index=False)