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
    #---------------------------------
    # First row of columns
col1, col2, col3 = st.columns(3)
    # Define brand colors (adjust these colors as per your brand)
brand_colors = {
        'Gender': '#B6AD77',  # Example blue
        'Nationality': '#00A5CD',  # Example darker blue
        'Branch': '#005587'  # Example even darker blue
    }
    
    # Start creating Streamlit layout
    # st.title('Distribution Metrics')
    
    # Gender Distribution
with col1:
    st.subheader('Gender Distribution')
    gender_count = df['Gender'].value_counts()
    fig = px.bar(gender_count, text=gender_count, color_discrete_sequence=[brand_colors['Gender']])
    fig.update_layout(xaxis_title="Gender", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)
    
    # Nationality Distribution
with col2:
    st.subheader('Nationality Distribution')
    nationality_count = df['Nationality'].value_counts()
    fig = px.bar(nationality_count, text=nationality_count, color_discrete_sequence=[brand_colors['Nationality']])
    fig.update_layout(xaxis_title="Nationality", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)
    
    # Branch Distribution
with col3:
    st.subheader('Branch Distribution')
    branch_count = df['Branch'].value_counts()
    fig = px.bar(branch_count, text=branch_count, color_discrete_sequence=[brand_colors['Branch']])
    fig.update_layout(xaxis_title="Branch", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)
        
   # Brand colors (repeating or selecting as necessary, ensure you have at least as many colors as designations)
brand_colors = ['#64C8E1', '#00A5CD', '#005587', '#23282D', '#787878', 
                    '#B6AD77', '#7AADA4', '#59BFDA', '#C8C5C6', '#787878', '#7AADA4']
    
    # List of designations
designations = ['Analyst-Intern', 'Future Gears Analyst', 'Analyst', 'Associate Consultant', 'Consultant',
                    'Manager', 'Senior Manager', 'Director', 'Principal', 'Associate Partner', 'Partner']
    
    # Map designations to colors
designation_color_map = {designation: brand_colors[i] for i, designation in enumerate(designations)}





