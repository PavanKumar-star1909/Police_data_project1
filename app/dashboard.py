import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# -----------------------------
# MySQL Connection
# -----------------------------
MYSQL_USER = "pavankumar"
MYSQL_PASSWORD = "PAva19@#"
MYSQL_DB = "police_db"
MYSQL_HOST = "localhost"

# Encode password for special characters (@, #, etc.)
encoded_password = quote_plus(MYSQL_PASSWORD)

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}/{MYSQL_DB}"
)

st.set_page_config(page_title="Police Check Post Dashboard", layout="wide")

st.title("🚓 Police Check Post Dashboard")

# ==========================
# Helper: Get distinct values for dropdowns
# ==========================
def get_distinct_values(column_name):
    try:
        query = f"SELECT DISTINCT {column_name} FROM police_stops WHERE {column_name} IS NOT NULL"
        values = pd.read_sql(query, engine)[column_name].dropna().tolist()
        return values
    except:
        return []

# Fetch options for dropdowns
country_options = get_distinct_values("country_name")
race_options = get_distinct_values("driver_race")
violation_options = get_distinct_values("violation")

# ==========================
# Tabs
# ==========================
tab1, tab2, tab3 = st.tabs(["📝 Add New Log", "🔍 Insights", "📊 Reports"])

# ==========================
# TAB 1: Add New Police Log
# ==========================
with tab1:
    st.subheader("Add New Police Log")

    with st.form(key='new_log_form'):
        stop_date = st.date_input("Stop Date")
        stop_time = st.time_input("Stop Time")
        country_name = st.selectbox("Country Name", [""] + country_options)
        driver_gender = st.selectbox("Driver Gender", ["male", "female", "other"])
        driver_age = st.number_input("Driver Age", min_value=0, max_value=120, step=1)
        driver_race = st.selectbox("Driver Race", [""] + race_options)
        violation = st.selectbox("Violation", [""] + violation_options)
        search_conducted = st.selectbox("Was a Search Conducted?", [0, 1])
        search_type = st.text_input("Search Type")
        is_arrested = st.selectbox("Was Driver Arrested?", [0, 1])
        drugs_related_stop = st.selectbox("Was it Drug Related?", [0, 1])
        stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "15-30 Min", "30-60 Min", ">60 Min"])
        vehicle_number = st.text_input("Vehicle Number")

        submit_button = st.form_submit_button("Submit Log")

    if submit_button:
        # Create a DataFrame from form input
        new_log = pd.DataFrame({
            'stop_date': [stop_date],
            'stop_time': [stop_time],
            'country_name': [country_name],
            'driver_gender': [driver_gender],
            'driver_age': [driver_age],
            'driver_race': [driver_race],
            'violation': [violation],
            'search_conducted': [search_conducted],
            'search_type': [search_type],
            'is_arrested': [is_arrested],
            'drugs_related_stop': [drugs_related_stop],
            'stop_duration': [stop_duration],
            'vehicle_number': [vehicle_number]
        })

        try:
            new_log.to_sql("police_stops", engine, if_exists="append", index=False)
            st.success("✅ New log submitted successfully!")
            st.dataframe(new_log)
        except Exception as e:
            st.error(f"❌ Error inserting log: {e}")

# ==========================
# TAB 2: Insights
# ==========================
with tab2:
    st.subheader("Advanced Insights")

    queries = {
        "Top 10 Vehicles Involved in Drug-Related Stops": 
            "SELECT vehicle_number, COUNT(*) AS drug_stop_count "
            "FROM police_stops WHERE drugs_related_stop=1 "
            "GROUP BY vehicle_number ORDER BY drug_stop_count DESC LIMIT 10",

        "Vehicles Most Frequently Searched": 
            "SELECT vehicle_number, COUNT(*) AS search_count "
            "FROM police_stops WHERE search_conducted=1 "
            "GROUP BY vehicle_number ORDER BY search_count DESC LIMIT 10",

        "Driver Age Group with Highest Arrest Rate": 
            "SELECT driver_age, SUM(is_arrested) AS arrests "
            "FROM police_stops GROUP BY driver_age ORDER BY arrests DESC LIMIT 10",

        "Gender Distribution by Country": 
            "SELECT country_name, driver_gender, COUNT(*) AS stop_count "
            "FROM police_stops GROUP BY country_name, driver_gender",

        "Race & Gender Combination with Highest Search Rate": 
            "SELECT driver_race, driver_gender, COUNT(*) AS search_count "
            "FROM police_stops WHERE search_conducted=1 "
            "GROUP BY driver_race, driver_gender ORDER BY search_count DESC LIMIT 10",

        "Most Common Violations Among Drivers <25": 
            "SELECT violation, COUNT(*) AS violation_count "
            "FROM police_stops WHERE driver_age < 25 GROUP BY violation ORDER BY violation_count DESC",

        "Countries with Highest Drug-Related Stops": 
            "SELECT country_name, COUNT(*) AS drug_stops "
            "FROM police_stops WHERE drugs_related_stop=1 GROUP BY country_name ORDER BY drug_stops DESC",

        "Yearly Breakdown of Stops and Arrests by Country": 
            "SELECT country_name, YEAR(stop_date) AS year, "
            "COUNT(*) AS total_stops, SUM(is_arrested) AS total_arrests "
            "FROM police_stops GROUP BY country_name, YEAR(stop_date) "
            "ORDER BY year, total_arrests DESC",

        "Driver Violation Trends Based on Age and Race": 
            "SELECT driver_age, driver_race, violation, COUNT(*) AS count "
            "FROM police_stops GROUP BY driver_age, driver_race, violation "
            "ORDER BY count DESC LIMIT 20",

        "Time Period Analysis of Stops (Year, Month, Hour)": 
            "SELECT YEAR(stop_date) AS year, MONTH(stop_date) AS month, "
            "HOUR(stop_time) AS hour, COUNT(*) AS stop_count "
            "FROM police_stops GROUP BY year, month, hour ORDER BY year, month, hour",

        "Violations with High Search and Arrest Rates": 
            "SELECT violation, "
            "SUM(search_conducted) AS searches, "
            "SUM(is_arrested) AS arrests, COUNT(*) AS total, "
            "(SUM(search_conducted)/COUNT(*))*100 AS search_rate, "
            "(SUM(is_arrested)/COUNT(*))*100 AS arrest_rate "
            "FROM police_stops GROUP BY violation "
            "ORDER BY arrest_rate DESC LIMIT 10",

        "Driver Demographics by Country": 
            "SELECT country_name, driver_gender, driver_race, AVG(driver_age) AS avg_age, COUNT(*) AS total "
            "FROM police_stops GROUP BY country_name, driver_gender, driver_race "
            "ORDER BY total DESC",

        "Top 5 Violations with Highest Arrest Rates": 
            "SELECT violation, SUM(is_arrested) AS arrests, COUNT(*) AS total, "
            "(SUM(is_arrested)/COUNT(*))*100 AS arrest_rate "
            "FROM police_stops GROUP BY violation "
            "ORDER BY arrest_rate DESC LIMIT 5"
    }

    selected_query_name = st.selectbox("Select a Query to Run:", list(queries.keys()))

    if st.button("Run Query"):
        query = queries[selected_query_name]
        try:
            result_df = pd.read_sql(query, engine)
            st.success(f"✅ Query executed: {selected_query_name}")
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"❌ Error executing query: {e}")

# ==========================
# TAB 3: Reports
# ==========================
import plotly.express as px
with tab3:
    st.subheader("📊 Automated Reports")

    report_query = """
        SELECT country_name, violation, COUNT(*) AS violation_count, 
               SUM(is_arrested) AS total_arrests, 
               SUM(drugs_related_stop) AS drug_cases
        FROM police_stops 
        GROUP BY country_name, violation
        ORDER BY violation_count DESC
    """

    try:
        report_df = pd.read_sql(report_query, engine)
        st.write("### Summary Report by Country & Violation")
        st.dataframe(report_df)

        # ==============================
        # Charts / Visualizations
        # ==============================
        st.write("### 📈 Visual Insights")

        # 1. Total Violations by Country (Pie Chart)
        country_summary = report_df.groupby("country_name")["violation_count"].sum().reset_index()
        fig1 = px.pie(country_summary, names="country_name", values="violation_count",
                      title="🚦 Violations Share by Country", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Top 10 Violations Overall (Horizontal Bar)
        top_violations = report_df.groupby("violation")["violation_count"].sum().reset_index().sort_values(by="violation_count", ascending=False).head(10)
        fig2 = px.bar(top_violations, x="violation_count", y="violation", orientation="h",
                      title="🔥 Top 10 Violations", color="violation_count", color_continuous_scale="Viridis")
        st.plotly_chart(fig2, use_container_width=True)

        # 3. Arrests vs Violations (Bubble Chart)
        arrest_chart = report_df.groupby("violation")[["violation_count", "total_arrests"]].sum().reset_index()
        fig3 = px.scatter(arrest_chart, x="violation_count", y="total_arrests",
                          size="total_arrests", color="violation",
                          title="👮 Arrests vs Violations (Bubble Chart)",
                          size_max=60)
        st.plotly_chart(fig3, use_container_width=True)

        # 4. Drug Related Cases by Country (Line Chart)
        drug_chart = report_df.groupby("country_name")["drug_cases"].sum().reset_index()
        fig4 = px.line(drug_chart, x="country_name", y="drug_cases", markers=True,
                       title="💊 Drug Related Stops by Country", color="country_name")
        st.plotly_chart(fig4, use_container_width=True)

        # ==============================
        # Download Option
        # ==============================
        st.download_button("⬇️ Download Report (CSV)", 
                           report_df.to_csv(index=False), 
                           "police_report.csv", 
                           "text/csv")

    except Exception as e:
        st.error(f"❌ Error generating report: {e}")
