````markdown
# Police Dashboard Project

A Python-based project that visualizes and analyzes police stop data. It combines data preprocessing, database management, and a web dashboard interface for insightful analysis.

---

## 1. Project Overview
The **Police Dashboard** project tracks and analyzes vehicle stops conducted by the police. It provides insights into:

- Stop dates and times
- Driver demographics (age, gender, race)
- Violation types
- Searches and arrests
- Drugs-related stops
- Stop durations  

This helps understand trends and patterns in traffic enforcement.

---

## 2. Setup and Installation

### 2.1 Python Environment
1. Ensure Python is installed (Python 3.9+ recommended).  
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
````

### 2.2 Required Python Modules

Install the necessary Python packages using `pip`:

```bash
pip install pandas numpy sqlalchemy pymysql streamlit
```

* **pandas**: For data manipulation
* **numpy**: For numerical operations
* **sqlalchemy**: For database connection and ORM
* **pymysql**: MySQL database connector
* **streamlit**: For building interactive web dashboards

---

## 3. Data

### 3.1 Input Data

The project uses CSV files:

* `policedata.csv` – Original raw police stop data
* `clean_stops.csv` – Preprocessed and cleaned data

### 3.2 Preprocessing Steps

Performed in `scripts/preprocess.py`:

1. Remove missing or null values.
2. Standardize column names.
3. Format dates and times correctly (`stop_date`, `stop_time`).
4. Encode categorical values if needed (e.g., `driver_gender`, `driver_race`).
5. Save the cleaned data as `clean_stops.csv`.

---

## 4. Database Connection

### 4.1 Database Setup

1. Use MySQL to create a database:

```sql
CREATE DATABASE police_db;
```

2. Create a table for police stops:

```sql
CREATE TABLE police_stops (
    stop_date DATE,
    stop_time TIME,
    country_name VARCHAR(50),
    driver_gender VARCHAR(10),
    driver_age INT,
    driver_race VARCHAR(20),
    violation VARCHAR(50),
    search_conducted BOOLEAN,
    search_type VARCHAR(50),
    is_arrested BOOLEAN,
    drugs_related_stop BOOLEAN,
    stop_duration VARCHAR(20),
    vehicle_number VARCHAR(20)
);
```

### 4.2 Loading Data into Database

Use SQLAlchemy and PyMySQL in `scripts/db_load.py` to load the preprocessed CSV into MySQL:

```python
import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv('../data/clean_stops.csv')

# Connect to MySQL
engine = create_engine("mysql+pymysql://username:password@localhost/police_db")

# Load data into table
df.to_sql('police_stops', con=engine, if_exists='replace', index=False)
```

---

## 5. Dashboard using Streamlit

### 5.1 Streamlit Setup

* Streamlit allows creating interactive web apps for data analysis.
* Install with:

```bash
pip install streamlit
```

### 5.2 Running the Dashboard

In `app/dashboard.py`, you:

1. Connect to the database.
2. Load data into a Pandas DataFrame.
3. Create visualizations (bar charts, pie charts, tables) for:

   * Violations per race/gender
   * Stop durations
   * Searches and arrests

Run the dashboard:

```bash
streamlit run app/dashboard.py
```

---

## 6. Project Structure

```
Police-Dashboard/
│
├─ app/               # Streamlit dashboard scripts
│   └─ dashboard.py
├─ data/              # CSV datasets
│   ├─ policedata.csv
│   └─ clean_stops.csv
├─ scripts/           # Data preprocessing and database scripts
│   ├─ preprocess.py
│   └─ db_load.py
├─ sql/               # SQL schema files
├─ README.md
└─ requirements.txt   # Python dependencies
```

---

## 7. GitHub Integration

1. Initialize Git:

```bash
git init
git add .
git commit -m "Initial commit - Police Dashboard project"
```

2. Add remote repository:

```bash
git remote add origin https://github.com/PavanKumar-star1909/Police-Dashboard.git
```

3. Push to GitHub:

```bash
git push -u origin main
```

---

## 8. Author

**Pavan Kumar J**
GitHub: [PavanKumar-star1909](https://github.com/PavanKumar-star1909)

---

## 9. Summary

This project demonstrates the **end-to-end workflow**:

1. Data collection from CSV files
2. Data preprocessing and cleaning
3. Storing data in MySQL database
4. Visualization and analysis through a **Streamlit web dashboard**

```

---


```
