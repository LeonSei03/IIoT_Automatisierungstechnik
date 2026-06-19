import streamlit as st
import sqlite3
import pandas as pd
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

st.set_page_config(page_title="Learning Factory Dashboard", layout="wide")
st.title("Learning Factory – Live Dashboard")

def load_data():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM flaschen ORDER BY time_scale", con)
    con.close()
    return df

try:
    df = load_data()
    n = len(df)
    cracked = int(df["is_cracked"].sum())

    # Kennzahlen 
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Flaschen gesamt", n)
    col2.metric("Gesprungen", cracked)
    col3.metric("In Ordnung", n - cracked)
    col4.metric("Ausschussrate", f"{cracked/n*100:.1f}%" if n > 0 else "–")

    st.divider()

    # Zeitreihe
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Zeitreihe")
        spalte = st.selectbox("Spalte wählen", [
            "final_weight",
            "vibration_index_red", "vibration_index_blue", "vibration_index_green",
            "temperature_C_red", "temperature_C_blue", "temperature_C_green",
            "fill_level_grams_red", "fill_level_grams_blue", "fill_level_grams_green",
        ])
        st.line_chart(df.set_index("bottle")[spalte])

    with col_right:
        st.subheader("Endgewicht vs. Vibrationsindex (Rot)")
        st.scatter_chart(df, x="vibration_index_red", y="final_weight", color="is_cracked")

    st.divider()

    # Tabelle
    st.subheader("Rohdaten (letzte 20 Flaschen)")
    st.dataframe(
        df.tail(20)[[
            "bottle", "recipe", "final_weight", "is_cracked",
            "temperature_C_red", "temperature_C_blue", "temperature_C_green",
            "vibration_index_red", "vibration_index_blue", "vibration_index_green",
        ]],
        use_container_width=True
    )

except Exception as e:
    st.warning(f"Warte auf Daten... ({e})")

# Auto-Refresh alle 5 Sekunden
time.sleep(5)
st.rerun()