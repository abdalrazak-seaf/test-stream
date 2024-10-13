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


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('centering-dock-357814-ddda7d72dfa6.json', scope)
client = gspread.authorize(creds)
    
#configure the dashboard page
st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")
    
st.title(" :bar_chart: SG Employee Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
    
    
sheet = client.open("dashboard").sheet1  # Replace with your sheet name
    
data = sheet.get_all_records()  # Gets all the records from the first sheet
    
    # st.read(data)  # Display the data in the app
    # Assuming 'data' is the list of dictionaries you got from the Google Sheet
df = pd.DataFrame(data)
    
    # Specify the desired order for designations
desired_order = ['Analyst-Intern', 'Future Gears Analyst', 'Analyst', 'Associate Consultant', 'Consultant',
                     'Manager', 'Senior Manager', 'Director', 'Principal', 'Associate Partner', 'Partner']
    
    # Update the 'Designation' column to be a categorical type with the specified order
df['Designation'] = pd.Categorical(df['Designation'], categories=desired_order, ordered=True)
    
    
    
    # Display the DataFrame in Streamlit
    # st.dataframe(df)
    
sheet2 = client.open("dashboard").get_worksheet(1)  # Replace with your sheet name
    
data2 = sheet2.get_all_records()  # Gets all the records from the first sheet
    
    # st.read(data)  # Display the data in the app
    # Assuming 'data' is the list of dictionaries you got from the Google Sheet
df_rate = pd.DataFrame(data2)
