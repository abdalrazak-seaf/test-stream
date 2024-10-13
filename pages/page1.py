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

st.title("Chatbot_Abdalrazak")

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# Function to load Google Sheets data
def load_gsheet_data():
    # Define the scope for accessing Google Sheets and Google Drive
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load credentials from Streamlit secrets
    creds_dict = json.loads(st.secrets["connections.gsheets"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet by name
    sheet = client.open("Your Google Sheet Name").sheet1  # Replace with your Google Sheet name

    # Get all records from the sheet
    data = sheet.get_all_records()

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)

    return df

# Streamlit app
st.title("Google Sheets Data in Streamlit")

# Load and display the data
df = load_gsheet_data()
st.write(df)



