import pickle
from datetime import timedelta, date
import holidays
import json
import joblib
import pandas as pd
import numpy as np


au_holidays = holidays.Australia(state='ACT', years=2025)


class AppState:

    def __init__(self):
        self.df = self.get_dataset() #Get and store dataset
        self.today_date = date.today() + timedelta(days=1)#Get and store todays date
        self.today_day = self.today_date.weekday() #Get and store todays weekday (int)
        self.is_weekend = self._is_weekend() #Get and store weekend (bool)
        self.is_public_holiday = self._is_public_holiday() #Get and store public holiday (bool)
        self.yesterday_date = self.today_date - timedelta(days=1) #Get and store yesterdays date
        self.yesterday_day = self.yesterday_date.weekday() #Get and store yesterdays weekday (int)
        self.yesterday_is_weekend = self._yesterday_is_weekend() #Get and store yesterday weekend (bool)
        self.yesterday_is_public_holiday = self._yesterday_is_public_holiday() #Get and store yesterday public holiday (bool)
        self.get_config()

    #Read config file
    def get_config(self):
        with open("config.json", "r") as f:
            config_dict = json.load(f)
            self.buffer_dict = config_dict["unique_items"]
            self.order_days = tuple(config_dict["order_days"])
            self.delivery_delay = config_dict["delivery_delay"]
            self.unique_products = []
            for key in config_dict["unique_items"]:
                self.unique_products.append(key)
            self.unique_products = sorted(
                self.unique_products, key=lambda x: x[0])


        self.delivery_days = self._delivery_days() #Calculate delivery days
        self.order_for_days = self._order_for_days() #Calculate days within ordering period
        self.yesterday_date = self.yesterday_date.strftime("%d/%m/%Y") #Convert date format
        self.today_date = self.today_date.strftime("%d/%m/%Y") #Convert date format

    #Read/update ML model
    def get_model(self):
        with open("linear_model.joblib", "rb") as f:
            self.model = joblib.load(f)

    #Read/update encoders from preprocessing
    def get_encoders(self):
        with open("encoder.pkl", "rb") as f:
            self.encoder = pickle.load(f)
        with open("scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)
        with open("imputer.pkl", "rb") as f:
            self.imputer = pickle.load(f)

    #Read/update preprocessed data
    def get_preprocessed_data(self):
        self.model_data = np.load('preprocessed_data.npz')

    #Read/update dataset
    def get_dataset(self):
        df = pd.read_csv("training.csv")
        df = df[df["Date"].notnull()]
        df["Item Name"] = df["Item Name"].str.strip()
        return df
    
    def backup_csv(self):
        self.df.to_csv("backup.csv", index=False)
        print("CSV copy updated")

    def _is_weekend(self):
        if self.today_day == 6 or self.today_day == 5:
            return 1
        else:
            return 0

    def _is_public_holiday(self):
        if self.today_date in au_holidays:
            return 1
        else:
            return 0

    def _yesterday_is_weekend(self):
        if self.yesterday_date.weekday() == 6 or self.yesterday_date.weekday() == 5:
            return 1
        else:
            return 0

    def _yesterday_is_public_holiday(self):
        if self.yesterday_date in au_holidays:
            return 1
        else:
            return 0

    def _delivery_days(self):
        delivery_days = []
        for i in range(len(self.order_days)):
            x = self.order_days[i] + self.delivery_delay
            if x > 6:
                x = x-7
            delivery_days.append(x)
        return delivery_days

    def _order_for_days(self):
        order_for_days = []
        for i in range(len(self.delivery_days)):
            x = self.delivery_days[i]
            x = x+1
            y = 1
            while x not in self.delivery_days:
                y = y+1
                x = x+1
                if x > 6:
                    x = x-7
            order_for_days.append(y)
        return order_for_days
