9# -*- coding: utf-8 -*-
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

st.title("Chatbot_Abdalrazak")

# example/st_app.py


from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/18hn6TOgx2yRerr4tMvJgnFc0JdB0hAMK3ZT3a1azw4I/edit?pli=1&gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)
st.dataframe(data)

# # Create a connection object.
# conn = st.connection("gsheets", type=GSheetsConnection)

# df = conn.read()

# # Streamlit app
# st.title("Google Sheets Data in Streamlit")

# # # Load and display the data
# # df = load_gsheet_data()
# # st.write(df)



