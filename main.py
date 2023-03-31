# Imports required ---
import streamlit as st
import sqlite3 as sqlite
import pandas as pd
import plotly.express as px

## Instructions:
# Go in Shell (on the right)
# write "pip install --upgrade streamlit"
# launch with "streamlit run main.py"
# https://abhin-poojari-proff-charles-assignment-main-zgozri.streamlit.app/


@st.cache_data
# Fetching data function
def get_data(table_name):
  con = sqlite.connect("Fake_sales_data.db")
  data = pd.read_sql_query(f"SELECT * from {table_name}", con)
  return data


# data['company'] = data['company'].astype('string')
# data['cat'] = data['cat'].astype ('string')

st.set_page_config('Sales Dashboard', ":bar_chart:", layout="wide")

#--------------SIDE BAR -------------------
st.sidebar.header("Filter the data here:")

data_set = st.sidebar.selectbox("Select Dataset:", ["SalesA", "SalesB"],
                                index=0)
# Fetching data
data = get_data(data_set)

# Company selection
company = st.sidebar.selectbox("Select a Company:",
                               data["company"].unique(),
                               index=0)

# Category selection
category_options = data[data["company"] == company]["cat"].unique()

select_all = st.sidebar.checkbox('Select all category')

if(select_all):
  category = category_options
else:
  category = st.sidebar.multiselect("Select any Category",
                                  category_options,
                                  default=category_options[0],
                                  disabled=select_all)

# Data filtering
data_selection = data.query("company == @company & cat in @category")

#--------------MAIN PAGE -------------------
st.title(f":bar_chart: Sales Dashboard - {company}")

# ------------Collecting KPIs------------------------------------------------
total_revenue = int(data_selection["price"].sum())
avg_revenue = round(data_selection["price"].mean(), 1)
total_volume = data_selection["price"].count()

# ------------Displaying KPIs------------------------------------------------
first_column, second_column, third_column = st.columns(3)

with first_column:
  st.subheader("Total Sales:")
  st.subheader(f"**:blue[{total_revenue}]**")

with second_column:
  st.subheader("Average Sales:")
  st.subheader(f"**:blue[{avg_revenue}]**")

with third_column:
  st.subheader("Total Volume:")
  st.subheader(f"**:blue[{total_volume}]**")

# -----------------------------------------------------------------------
st.subheader("Category Analysis:")
first_column, second_column = st.columns(2)

with first_column:
  #Chart for Products Sold
  no_prod_sold = data_selection[['cat', 'price']].value_counts().reset_index()
  
  no_prod_sold.columns = [*no_prod_sold.columns[:-1], 'Volume of Product']
  
  plot_bar = px.bar(no_prod_sold,
                    x='price',
                    y='Volume of Product',
                    color='cat',
                    width=450,
                    labels={"cat": "Category", "price":"Price"},
                    title=f'Different products sold in {company}')
  
  st.plotly_chart(plot_bar)

with second_column:
  market_share = data.groupby(["company","cat"])["price"].sum().reset_index()
  market_share = market_share.loc[market_share["cat"].isin(category)]
  market_share['Percentage'] = 100 * market_share['price'] / market_share.groupby('cat')['price'].transform('sum')
  
  plot_bar = px.bar(market_share,
                      x='cat',
                      y='Percentage',
                      color='company',
                      width=450,
                      labels={"Percentage": "Market Share (%)", "cat": "Category"},
                      title='Market Share based on Category')
    
  st.plotly_chart(plot_bar)

# --------------------------------------------------------------------------
# Volume of sales per week
volume_per_week = data_selection.groupby(["week"])["price"].count().reset_index()

# The revenues per week
revenue_per_week = data_selection.groupby(["week"])["price"].sum().reset_index()

data = data.loc[data["cat"].isin(category)]

# The volumes of other company per week
market_volume_per_week = data.groupby(["company","week"])["price"].count().reset_index()
# st.table(market_volume_per_week)
# The revenues of other company per week
market_revenue_per_week = data.groupby(["company","week"])["price"].sum().reset_index()

# --------------------------------------------------------------------------
# Displaying Chart
st.subheader("Volume and Revenue Analysis:")
first_column, second_column = st.columns(2)

with first_column:
  # plot volume & revenue through time
  tab1, tab2 = st.tabs(["Volume", "Revenue"])

  with tab1:
    chart_volume = px.line(volume_per_week,
                           x="week",
                           y="price",
                           width=450,
                           labels={"price": "Volume of Products"},
                           title='Volume produced per week')
    st.plotly_chart(chart_volume)

  with tab2:
    chart_revenue = px.line(revenue_per_week,
                            x="week",
                            y="price",
                            width=450,                            
                            labels={"price":"Price"},
                            title='Revenue generated per Week')
    st.plotly_chart(chart_revenue)

with second_column:
  # plot volume & revenue through time
  tab1, tab2 = st.tabs(["Volume", "Revenue"])

  with tab1:
    chart_volume = px.line(market_volume_per_week,
                           x="week",
                           y="price",
                           line_group="company",
                           color="company",
                           width=550,
                           labels={"price": "Volume of Products"},
                           title='Market Analysis - Volume / Time')
    st.plotly_chart(chart_volume)

  with tab2:
    chart_revenue = px.line(market_revenue_per_week,
                            x="week",
                            y="price",
                            line_group="company",
                            color="company",
                            width=550,
                            labels={"price":"Price"},
                            title='Market Analysis - Revenue / Time')
    st.plotly_chart(chart_revenue)
