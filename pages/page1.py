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
# st.dataframe(data)
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

    # Second row of columns
col4, col5 = st.columns(2)
    
    # Gender Distribution by Designation
with col4:
    st.subheader('Gender Distribution by Designation')
    gender_designation = df.groupby(['Gender', 'Designation']).size().reset_index(name='count')
    fig = px.bar(gender_designation, x='Gender', y='count', color='Designation', barmode='group', text='count',
                     color_discrete_map=designation_color_map)  # Apply the custom color map
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis_title="Gender", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)
    
    # Branch Distribution by Designation
with col5:
    st.subheader('Branch Distribution by Designation')
    branch_designation = df.groupby(['Branch', 'Designation']).size().reset_index(name='count')
    fig = px.bar(branch_designation, x='Branch', y='count', color='Designation', barmode='group', text='count',
                     color_discrete_map=designation_color_map)  # Apply the custom color map
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis_title="Branch", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    #-----------------------------------
    # Assuming df is your DataFrame
    # Replace these column names with the actual names of the skill columns in your dataset
skill_columns = ['rate yourself in Operational and Organizational Excellence'
                     , 'rate yourself in Digital', 'rate yourself in Strategy', 
                     'rate yourself in Marketing']
    # Convert skill columns to numeric, non-numeric entries will become NaN
for col in skill_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Now check the data types again to confirm the conversion
data_types_after_conversion = df[skill_columns].dtypes
    # Calculate average ratings for each skill area by Designation
avg_skill_ratings = df.groupby('Designation')[skill_columns].mean()
    
    # Dictionary mapping old column names to new names
rename_dict = {'rate yourself in Operational and Organizational Excellence': 'Operational and Organizational Excellence',
                   'rate yourself in Digital': 'Digital',
                   'rate yourself in Strategy': 'Strategy',
                   'rate yourself in Marketing': 'Marketing'}
    
    # Renaming the columns
avg_skill_ratings.rename(columns=rename_dict, inplace=True)
    
    # List of designations to exclude, because they did not fill the survey
designations_to_exclude = ['Partner', 'Principal', 'SME']
    
    # Drop the specified designations from the DataFrame
avg_skill_ratings = avg_skill_ratings.drop(designations_to_exclude, errors='ignore')
    
    
    # Identifying Skill Gaps
    # You might set a threshold to identify gaps, for example, ratings below a certain value
skill_gap_threshold = 3  # Example threshold
skill_gaps = avg_skill_ratings < skill_gap_threshold
    
    
    
    # Skillset Analysis section
st.header('Skillset Analysis')
    # Second row of columns
col6, col7 = st.columns(2)
    
    # Gender Distribution by Designation
with col6:
    # Displaying Average Skill Ratings
    st.subheader('Average Skill Ratings by Designation')
    # st.table(avg_skill_ratings)
    
    # Visualization (optional)
    # You can use a heatmap or bar chart to visualize these ratings
    fig = px.imshow(avg_skill_ratings, aspect='auto')#, color_continuous_scale='Picnic')
    st.plotly_chart(fig)
    
with col7:
    # Displaying Skill Gaps
    st.subheader('Identified Skill Gaps (Ratings Below Threshold)')
    # st.table(skill_gaps)
    
    # Convert boolean values to numeric (1 for True, 0 for False)
    numeric_skill_gaps = skill_gaps.astype(int)
    
    # Define a custom color scale: 0 -> green, 1 -> red
    custom_color_scale = [[0, '#005587'], [1, '#64C8E1']]
    
    # Create a heatmap using Plotly
    fig = px.imshow(numeric_skill_gaps, aspect='auto', color_continuous_scale=custom_color_scale)
    
    # Display the heatmap in Streamlit
    st.plotly_chart(fig)
    #--------------------------------------------------------------------
    
    # Create two columns for the new analysis
col8, col9 = st.columns(2)
    
    # 1. Average Number of Projects Handled by Employees in Different Roles
with col8:
    st.subheader("Average Number of Projects by Role for Each Service Line")
    
        # Calculating the average number of projects per role for each service line
    service_lines = ['Digital', 'Marketing', 'Operation', 'Strategy']
    avg_projects_by_role_service_line = df.groupby('Designation')[service_lines].mean().reset_index()
    
        # Melting the DataFrame for suitable format for Plotly heatmap
    melted_data = avg_projects_by_role_service_line.melt(id_vars='Designation', var_name='Service Line', value_name='Average Projects')
    
        # Plotting the heatmap with Plotly
    fig = px.density_heatmap(melted_data, x='Service Line', y='Designation', z='Average Projects') 
                                 #color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. Correlation Between the Number of Projects and Average Ratings
with col9:
    st.subheader("Correlation: Number of Projects and Average Ratings")
    
        # Ensure that the 'Total Projects' and 'average rating' columns are numeric
    df['Total Projects'] = pd.to_numeric(df['Total Projects'], errors='coerce')
    df['average rating'] = pd.to_numeric(df['average rating'], errors='coerce')
    
        # Drop NaN values for a clean correlation calculation
    correlation_df = df[['Total Projects', 'average rating']].dropna()
    
        # Calculate correlation
    correlation = correlation_df.corr()
    
        # Display the correlation value
    st.write("Correlation coefficient:", correlation.iloc[0, 1])
    
        # Plotting the correlation
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    sns.scatterplot(data=correlation_df, x='Total Projects', y='average rating', ax=ax)
    st.pyplot(fig)



