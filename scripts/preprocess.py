import pandas as pd
import os

# Load dataset
df = pd.read_csv(
    "C:/Users/vishv/Downloads/python_learning.1st project/__MACOSX/python_learning/data/policedata.csv",
    low_memory=False
)

# Remove fully empty columns
df = df.dropna(axis=1, how="all")

# Handle missing values safely (only if column exists)
if 'driver_age' in df.columns:
    df['driver_age'] = df['driver_age'].fillna(df['driver_age'].median())

if 'driver_gender' in df.columns:
    df['driver_gender'] = df['driver_gender'].fillna("Unknown")

if 'violation' in df.columns:
    df['violation'] = df['violation'].fillna("Unknown")

if 'vehicle_number' in df.columns:
    df['vehicle_number'] = df['vehicle_number'].fillna("UNKNOWN")

# Convert date and time safely
if 'stop_date' in df.columns:
    df['stop_date'] = pd.to_datetime(df['stop_date'], errors='coerce')

if 'stop_time' in df.columns:
    df['stop_time'] = pd.to_datetime(df['stop_time'], format='%H:%M', errors='coerce').dt.time

# Keep only the columns that exist in both DataFrame and MySQL table
columns_to_keep = [
    "stop_date", "stop_time", "country_name", "driver_gender",
    "driver_age", "driver_race", "violation", "search_conducted",
    "search_type", "stop_outcome", "is_arrested", "stop_duration",
    "drugs_related_stop", "vehicle_number"
]
df = df[[col for col in columns_to_keep if col in df.columns]]

# Ensure output folder exists
output_path = "C:/Users/vishv/Downloads/python_learning.1st project/__MACOSX/python_learning/data/clean_stops.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save cleaned file
df.to_csv(output_path, index=False)
print(f"✅ Cleaned dataset saved to: {output_path}\nReady for MySQL insertion.")
