import pandas as pd
from modeltraining import model_training
from preprocessing import pre_processing


# Delete last stocktake
def delete_stocktake(state):
    filtered_df = state.df[state.df["Date"] != state.yesterday_date]
    filtered_df.to_csv("training.csv", index=False)


# Checks to ensure stock count isn't being done twice in a day
def check_date(state):
    if state.yesterday_date in state.df["Date"].values:
        return True
    else:
        return False


# Take User Input
def enter_input(item_name):
    while True:
        try:
            current_stock = int(input(f"Enter stock for {item_name}:"))
            return current_stock
        except ValueError:
            print("Invalid Entry. Try again")


# Checks users sales input
def check_sales():
    while True:
        try:
            sales = int(input(f"Enter day sales:"))
            return sales
        except ValueError:
            print("Invalid Entry. Try again")


# Run stocktake
def stocktake(state, sales):

    is_school_holiday = 0  # IMPLEMENT APK FOR AUTOFILL. 0 BY DEFAULT

    # Get unique product names
    product_mapping = {i: name for i, name in enumerate(state.unique_products)}
    item_amount = len(product_mapping)

    data_frame = pd.DataFrame(None, index=range(item_amount), columns=[
                              "Date", "Item Name", "Sales", "DayOfWeek", "IsWeekend", "IsPublicHoliday", "IsSchoolHoliday", "Usage", "End Stock"])
    data_frame['Date'] = state.yesterday_date
    data_frame["Sales"] = sales
    data_frame["DayOfWeek"] = state.yesterday_day
    data_frame["IsWeekend"] = state.yesterday_is_weekend
    data_frame["IsPublicHoliday"] = state.yesterday_is_public_holiday
    data_frame["IsSchoolHoliday"] = is_school_holiday

    # Iterate through items
    currentItem = 0
    while currentItem < item_amount:
        item_name = product_mapping[currentItem]
        product_rows = state.df[state.df["Item Name"] == item_name]

        # Get last known End Stock as openStock
        if not product_rows.empty:
            last_row = product_rows.iloc[-1]
            open_stock = last_row["End Stock"]
        else:
            open_stock = 0

        current_stock = enter_input(item_name)
        usage = int(open_stock) - current_stock
        data_frame.loc[currentItem, "Item Name"] = str(item_name)
        data_frame.loc[currentItem, "Usage"] = usage
        data_frame.loc[currentItem, "End Stock"] = current_stock
        currentItem += 1


    state.backup_csv()
    data_frame.to_csv("training.csv", mode="a",
                      header=False, index=False)

    state.df = state.get_dataset()
    pre_processing(state)
    state.get_encoders()
    state.get_preprocessed_data()
    model_training(state)
    state.get_model()


def open_stocktake(state):
    repeated_date = check_date(state)

    # Continue if stock count not completed for the day
    if repeated_date:
        print("Stocktake already completed today.")
    else:
        sales = check_sales()
        stocktake(state, sales)
