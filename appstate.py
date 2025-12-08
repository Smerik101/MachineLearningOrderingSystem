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
        self.df = self.get_dataset()
        self.today_date = date.today()
        self.today_day = self.today_date.weekday()
        self.is_weekend = self._is_weekend()
        self.is_public_holiday = self._is_public_holiday()
        self.yesterday_date = self.today_date - timedelta(days=1)
        self.yesterday_day = self.yesterday_date.weekday()
        self.yesterday_is_weekend = self._yesterday_is_weekend()
        self.yesterday_is_public_holiday = self._yesterday_is_public_holiday()

        self.order_days = (1, 5)  # Days ordering is completed
        self.delivery_delay = 3  # Time for order to arrive

        self.delivery_days = self._delivery_days()
        self.order_for_days = self._order_for_days()

        self.yesterday_date = self.yesterday_date.strftime("%d/%m/%Y")
        self.today_date = self.today_date.strftime("%d/%m/%Y")

    def get_buffer(self):
        with open("buffer.txt", "r") as f:
            self.buffer_dict = json.load(f)

    def get_model(self):
        with open("linear_model.joblib", "rb") as f:
            self.model = joblib.load(f)

    def get_encoders(self):
        with open("encoder.pkl", "rb") as f:
            self.encoder = pickle.load(f)
        with open("scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)
        with open("imputer.pkl", "rb") as f:
            self.imputer = pickle.load(f)

    def get_preprocessed_data(self):
        self.model_data = np.load('preprocessed_data.npz')

    def get_dataset(self):
        df = pd.read_csv("training.csv")
        df.to_csv("backup.csv", index=False)
        df = df[df["Date"].notnull()]
        df["Item Name"] = df["Item Name"].str.strip()
        return df

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
