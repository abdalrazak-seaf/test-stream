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

# Read the entire sheet.
df = conn.read()

# Convert the data to a pandas DataFrame
data = pd.DataFrame(df)

# Print results to the app.
st.write("Google Sheet Data")
st.dataframe(data)



