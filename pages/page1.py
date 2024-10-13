# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:38:39 2024

@author: AbdulrazaqAlden
"""
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

st.title("Chatbot")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Try to read the data from the Google Sheet
df = conn.read()

# Debugging - Check the type of the returned data
st.write("Type of returned data:", type(df))

# Debugging - Check the contents of the data
st.write("Raw Data:", df)

# If df is a dictionary or list, convert to a DataFrame
try:
    data = pd.DataFrame(df)
    st.write("Converted DataFrame:")
    st.dataframe(data)  # Display the DataFrame
except Exception as e:
    st.error(f"Error converting to DataFrame: {e}")


