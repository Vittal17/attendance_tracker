import streamlit as st
import pandas as pd

st.title("attendance vibes")

# load the CSV, handle empty case
try:
    df = pd.read_csv("attendance_log.csv")
    st.write("who showed up n when", df)
    st.write("total check-ins:", len(df))
    if not df.empty:
        st.write("unique peeps:", df["name"].nunique())
except FileNotFoundError:
    st.write("no attendance log yet, run attendance.py first")
except KeyError:
    st.write("oops, CSV missing 'name' column, check the data")