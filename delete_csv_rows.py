import pandas as pd
from appstate import AppState

state = AppState()

filtered_df = state.df[state.df["Date"] != state.yesterday_date]
filtered_df.to_csv("training.csv", index=False)
state.current_state["current_stocktake"] = state.current_state["buffer_stocktake"]
state.write_state()