from datetime import date
from pathlib import Path
import sqlite3
import sys

import pandas as pd
import streamlit as st

MODEL_DIR = Path(__file__).resolve().parents[1] / "model.py"
sys.path.insert(0, str(MODEL_DIR))

from model import predict_health


DB_PATH = Path(__file__).with_name("patient.db")


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def create_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


conn = get_connection()
create_table(conn)

st.title("Sneha health app")

name = st.text_input("Full Name")
email = st.text_input("Email")
dob = st.date_input("Date of Birth", max_value=date.today())

glucose = st.number_input("Glucose", min_value=0.0, max_value=500.0, step=1.0)
haemoglobin = st.number_input("Haemoglobin", min_value=0.0, max_value=25.0, step=0.1)
cholesterol = st.number_input("Cholesterol", min_value=0.0, max_value=500.0, step=1.0)

if st.button("Predict and Save"):
    if not name.strip():
        st.error("Please enter the patient's full name.")
    elif not email.strip() or "@" not in email:
        st.error("Please enter a valid email address.")
    else:
        remarks = predict_health(glucose, haemoglobin, cholesterol)

        conn.execute(
            """
            INSERT INTO patients
            (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                dob.isoformat(),
                email.strip(),
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
            ),
        )
        conn.commit()

        st.success("Patient saved")
        st.write("Prediction:", remarks)

if st.button("Show Patients"):
    df = pd.read_sql_query(
        "SELECT * FROM patients ORDER BY created_at DESC",
        conn,
    )

    if df.empty:
        st.info("No patients saved yet.")
    else:
        st.dataframe(df, use_container_width=True)
