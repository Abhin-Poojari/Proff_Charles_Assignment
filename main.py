# Imports required ---
import streamlit as st
import sqlite3 as sqlite
import pandas as pd

## Instructions:
# Go in Shell (on the right)
# write "pip install --upgrade streamlit"
# launch with "streamlit run main.py"


@st.cache_data
def get_data():
    con = sqlite.connect("Fake_sales_data.db")
    data = pd.read_sql_query("SELECT * from SalesA", con)
    return data


data = get_data()

st.title('Sales Dashboard')
st.write(f"We have {len(data)} datapoints")
choice = st.selectbox("Select a Compan", data["company"].unique(), index=0)

new_data = data[data["company"] == choice]
ppl = st.selectbox("Select a Category", new_data["cat"].unique(), index=0)
new_data = new_data[new_data["cat"] == ppl]
st.write(f"Sum of sales {choice}:")
sperweek = new_data.groupby("week")["price"].sum()
st.line_chart(sperweek, y="price")
