import pandas as pd
import numpy as mp 
import streamlit as st
import preprosser
df = pd.read_csv("C:\\Users\\hp\Desktop\\Sales_Analytics\\Sales_Data_Analysis\\data.csv")
#print(df)



#creating time features
df = preprosser.fetch_time_features(df)

#Sidebar 
st.sidebar.title("Filters")

#Year Filter
st.sidebar.multiselect("Year Filter",[1,2,3])


# Filters
selected_year = preprosser.multiselect("Select Year", df["Financial_Year"].unique())
selected_retailer = preprosser.multiselect("Select Retailer", df["Retailer"].unique())
selected_company = preprosser.multiselect("Select Company", df["Company"].unique())
selected_month = preprosser.multiselect("Select Month", df["Financial_Month"].unique())

# Global filtering
filtered_df = df[(df["Financial_Year"].isin(selected_year)) & (df["Retailer"].isin(selected_retailer)) & (df["Company"].isin(selected_company)) & (df["Financial_Month"].isin(selected_month))]

# Title for dashbaord
st.title("Sales Analytics Dashboard")


# Creating columns for Indicators or KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label = "Total sales", value = int(filtered_df["Amount"].sum()))
with col2:
    st.metric(label = "Total margin", value = int(filtered_df["Margin"].sum()))
with col3:
    st.metric(label = "Total transactions", value = len(filtered_df["Margin"]))
with col4:
    st.metric(label = "Margin percentage (in %)", value = int(filtered_df["Margin"].sum()*100/filtered_df["Amount"].sum()))

# Month on month sales
yearly_sales = filtered_df[["Financial_Year", "Financial_Month", "Amount"]].groupby(["Financial_Year", "Financial_Month"]).sum().reset_index().pivot(index = "Financial_Month", columns = "Financial_Year", values = "Amount")
st.line_chart(yearly_sales, x_label = "Financial Month", y_label = "Total sales")

col5, col6 = st.columns(2)
# Retailer Revenue
with col5:
    st.title("Retailers count by revenue %")
    retailer_count = preprosser.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(retailer_count, x_label = "percentage revenue",y_label = "retailer_count")

with col6:
    st.title("Companies count by revenue %")
    company_count = preprosser.fetch_top_revenue_companies(filtered_df)
    company_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(company_count, x_label = "percentage revenue",y_label = "company_count")






