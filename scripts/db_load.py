import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# === File Path Handling ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path to scripts/
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "clean_stops.csv")

# Load cleaned CSV
df = pd.read_csv(DATA_PATH, low_memory=False)

# === MySQL Credentials ===
MYSQL_USER = "pavankumar"
MYSQL_PASSWORD = "PAva19@#"   # original password
MYSQL_DB = "police_db"
MYSQL_HOST = "localhost"

# === Test MySQL connection (mysql-connector-python) ===
import mysql.connector
try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    print("✅ MySQL connection successful")
    conn.close()
except mysql.connector.Error as e:
    print("❌ Error connecting to MySQL:", e)
    exit(1)

# === SQLAlchemy Engine (uses mysql+mysqlconnector) ===
encoded_password = quote_plus(MYSQL_PASSWORD)
engine = create_engine(
    f"mysql+mysqlconnector://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}/{MYSQL_DB}"
)

# === Insert data into MySQL table ===
try:
    df.to_sql("police_stops", engine, if_exists="append", index=False)
    print("✅ Data loaded into SQL database successfully")
except Exception as e:
    print("❌ Error loading data into SQL:", e)
