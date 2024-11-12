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
from streamlit_gsheets import GSheetsConnection

#configure the dashboard page
# st.set_page_config(page_title="Superstore!!!")
    
st.title(" :bar_chart: SG Employee Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

url = "https://docs.google.com/spreadsheets/d/18hn6TOgx2yRerr4tMvJgnFc0JdB0hAMK3ZT3a1azw4I/edit?pli=1&gid=0#gid=0"


conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)
st.dataframe(data)
#--------------
df = pd.DataFrame(data)
    
    # Specify the desired order for designations
desired_order = ['Analyst-Intern', 'Future Gears Analyst', 'Analyst', 'Associate Consultant', 'Consultant',
                     'Manager', 'Senior Manager', 'Director', 'Principal', 'Associate Partner', 'Partner']
    
    # Update the 'Designation' column to be a categorical type with the specified order
df['Designation'] = pd.Categorical(df['Designation'], categories=desired_order, ordered=True)

url2 = "https://docs.google.com/spreadsheets/d/18hn6TOgx2yRerr4tMvJgnFc0JdB0hAMK3ZT3a1azw4I/edit?pli=1&gid=1168015449#gid=1168015449"
conn = st.connection("gsheets", type=GSheetsConnection)
data2 = conn.read(spreadsheet=url2)
st.dataframe(data2)






