import pandas as pd

# === CONFIG ===
csv_file = "TrainingSetNew.csv"
date_column = "Date"

# === INPUT ===
target_date = input("Enter the date to delete (dd/mm/yyyy): ")

# === LOAD CSV ===
df = pd.read_csv(csv_file)

# === FILTER OUT THE TARGET DATE ===
filtered_df = df[df[date_column] != target_date]

# === SAVE CLEANED CSV ===
filtered_df.to_csv(csv_file, index=False)

print(f"Rows with date {target_date} have been removed.")