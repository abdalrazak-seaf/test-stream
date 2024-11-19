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
import random
from sklearn.preprocessing import MinMaxScaler
from streamlit_gsheets import GSheetsConnection

#configure the dashboard page
# st.set_page_config(page_title="Superstore!!!")
    
st.title('''

         :bar_chart: Resources Matching''')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


url = "https://docs.google.com/spreadsheets/d/18hn6TOgx2yRerr4tMvJgnFc0JdB0hAMK3ZT3a1azw4I/edit?pli=1&gid=0#gid=0"


conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, worksheet = 'Sheet1')
# st.dataframe(data)
df = pd.DataFrame(data)

data2 = conn.read(spreadsheet=url, worksheet = 'Sheet3')
# st.dataframe(data2)
df_proj = pd.DataFrame(data2)

#-------------
# Sidebar Filters
st.sidebar.title("Filters")

# Define mappings between service lines and corresponding sub-service lines
sub_service_line_mapping = {
    "Digital": ['Digital Strategy', 'Digital Transformation Support', 'Business Intelligence Solutions',
                'Data Management', 'Data Solutions at Scale', 'Data Analytics'],
    "Marketing": ['Brand Equity & Development', 'Marketing Strategy', 'Communication Strategy',
                  'Pricing Strategy', 'Marketing Support'],
    "Operation": ['Governance', 'Operating Model Design', 'Project Management', 'Performance Management', 
                  'Organizational Design', 'Policies and Procedures', 'Change Management', 
                  'Culture Transformation', 'Capability Building', 'Business Process Management'],
    "Strategy": ['Strategy Development', 'Strategy Implementation', 'Market Research & Economical Studies']
}

# Filter 1: Service Line (multi-select)
service_lines = ["Digital", "Marketing", "Operation", "Strategy"]
selected_service_lines = st.sidebar.multiselect('Select Service Line(s)', service_lines)

# Filter 2: Sub-Service Line (multi-select)
# Update sub-service line options based on selected service lines
sub_service_line_options = []
for sl in selected_service_lines:
    sub_service_line_options.extend(sub_service_line_mapping.get(sl, []))

selected_sub_service_lines = st.sidebar.multiselect('Select Sub-Service Line(s)', list(set(sub_service_line_options)))

# Project filter (single select)
project_options = df_proj['Project Code'].unique()
selected_project = st.sidebar.selectbox('Select a Project', ['None'] + list(project_options))

# Display the selected filters
st.write("Selected Project:", selected_project)
st.write(f"Selected Service Line(s): {', '.join(selected_service_lines) if selected_service_lines else 'None'}")
st.write(f"Selected Sub-Service Line(s): {', '.join(selected_sub_service_lines) if selected_sub_service_lines else 'None'}")

# Designation filter (multiselect) - Add this below the project filter
designation_options = df_proj['Designation'].unique()
selected_designations = st.sidebar.multiselect('Select Designation(s)', designation_options)


#-----------------
    # Select specific columns to display
columns_to_display = ['Employee ID', 'Employee Name', 'Designation', 
                          'From Date', 'To Date', 'Ratio (%)', 
                          'Project Code', 'Project Partner Name', 'Service Line', 
                          'Gender', 'Nationality', 'Branch', 'Grade', 'Status', 
                          'Months since Joining']
if selected_project != 'None':
    filtered_df = df_proj[df_proj['Project Code'] == selected_project]
    # Display the DataFrame as a table
    st.dataframe(filtered_df[columns_to_display])
elif selected_designations:
    filtered_df = df_proj[df_proj['Designation'].isin(selected_designations)]

    # # Select specific columns to display
    # columns_to_display = ['Employee ID', 'Employee Name', 'Designation', 
    #                       'From Date', 'To Date', 'Ratio (%)', 
    #                       'Project Code', 'Project Partner Name', 'Service Line', 
    #                       'Gender', 'Nationality', 'Branch', 'Grade', 'Status', 
    #                       'Months since Joining']

    # Display the DataFrame as a table
    st.dataframe(filtered_df[columns_to_display])
else:
    st.write("Please select a project to view details.")

#---------------------------------------------------------------------------------------
# Define weights
tenure_weight = 0.2
sl_weight = 0.25
eval_weight = 0.2
rate_weight = 0.1
total_proj_weight = 0.25


# Assuming df is your DataFrame
# Replace 'column1', 'column2', etc., with your actual column names
columns_to_convert = ['Months since Joining', 'Strategy2', 'Strategy Development', 'Strategy Implementation',
       'Market Research & Economical Studies', 'Digital2', 'Digital Strategy',
       'Digital Transformation Support', 'Business Intelligence Solutions',
       'Data Management', 'Data Solutions at Scale', 'Data Analytics',
       'Operational and Organizational Excellence2', 'Governance',
       'Operating Model Design', 'Project Management',
       'Performance Management', 'Organizational Design',
       'Policies and Procedures', 'Change Management',
       'Culture Transformation', 'Capability Building',
       'Business Process Management', 'Marketing2',
       'Brand Equity & Development', 'Marketing Strategy',
       'Communication Strategy', 'Pricing Strategy', 'Marketing Support', 'Digital', 'Marketing', 'Operation',
       'Strategy', 'july 2023', 'jan 2023', 'Digital_Norm', 'Marketing_Norm',
       'Operation_Norm', 'Strategy_Norm', 'Total Projects',
       'rate yourself in Operational and Organizational Excellence',
       'rate yourself in Digital', 'rate yourself in Strategy',
       'rate yourself in Marketing', 'average rating', 'avg_rating_Norm']

for column in columns_to_convert:
    # Replace np.nan with 0 and then convert to numeric
    df_proj[column] = pd.to_numeric(df_proj[column].fillna(0), errors='coerce')


#------------------------

#----------------------------------
    
# Initialize the MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

# Function to calculate match rate
def calculate_match_rate(df, service_line, sub_service_line, suffix):
    # Make sure to replace spaces and special characters in sub_service_line
    sub_service_line_component = sub_service_line  # Example replacement
    service_line_component = service_line + '_Norm'

    df[f'service_line_value_{suffix}'] = df[service_line_component]
    df[f'sub_service_line_value_{suffix}'] = df[sub_service_line_component]

    df[f'average_evaluation_{suffix}'] = (df['july 2023'] + df['jan 2023']) / 2

    df[f'match_rate_{suffix}'] = (df['Months since Joining'] * tenure_weight + 
                                  df[f'service_line_value_{suffix}'] * sl_weight + 
                                  df[f'average_evaluation_{suffix}'] * eval_weight + 
                                  df[f'sub_service_line_value_{suffix}'] * rate_weight + 
                                  df['Total Projects'] * total_proj_weight)

# Function to normalize match rate for a specific sub-service line
def calculate_and_normalize_match_rate(df, service_line, sub_service_line, suffix):
    calculate_match_rate(df, service_line, sub_service_line, suffix)

    # Group by 'Designation' and normalize within each group for the specific sub-service line
    grouped = df.groupby('Designation')[f'match_rate_{suffix}']

    # Apply normalization within each group
    df[f'match_rate_Norm_{suffix}'] = grouped.transform(lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten())

# Check if at least one service line and one sub-service line are selected
if selected_service_lines and selected_sub_service_lines:
    # Copy the DataFrame for independent calculations
    df_copy = df_proj.copy()
    


    # Perform match rate calculations for each sub-service line independently
    for i, ssl in enumerate(selected_sub_service_lines):
        service_line = selected_service_lines[min(i, len(selected_service_lines) - 1)]
        suffix = ssl.replace(' ', '_').replace('&', 'and')  # Consistent with calculate_match_rate
        calculate_and_normalize_match_rate(df_copy, service_line, ssl, suffix)

    # Filter DataFrame based on selected project or designation
    if selected_project != 'None':
        filtered_df = df_copy[df_copy['Project Code'] == selected_project]
    elif selected_designations:
        filtered_df = df_copy[df_copy['Designation'].isin(selected_designations)]
    else:
        filtered_df = df_copy
    # Create a layout based on the number of sub-service lines selected
    cols = st.columns(len(selected_sub_service_lines))

    # Display match rate tables for each sub-service line
    for i, ssl in enumerate(selected_sub_service_lines):
        with cols[i]:
            suffix = ssl.replace(' ', '_').replace('&', 'and')
            ssl_columns = ['Employee ID', 'Employee Name', 'Designation', 
                            f'match_rate_Norm_{suffix}']#f'match_rate_{suffix}',
            # Check if required columns exist
            if all(col in filtered_df for col in ssl_columns):
                st.write(f"Match Rate Analysis for {ssl}:")
                st.dataframe(filtered_df[ssl_columns])
            else:
                st.error(f"Error: Required columns for {ssl} are missing.")
    # Save the DataFrame to an Excel file
    output_filename = "match_rate_analysis.xlsx"
    # filtered_df.to_excel(output_filename, index=False)
    
    test_df = filtered_df.copy()

    # Create a download button for the Excel file
    # with open(output_filename, "rb") as file:
    #     btn = st.download_button(
    #         label="Download Match Rate Analysis as Excel",
    #         data=file,
    #         file_name=output_filename,
    #         mime="application/vnd.ms-excel"
    #     )
else:
    st.write("Please select a service line and a sub-service line to view the match rate analysis.")
    
#-------------------------------------
# Function to calculate average normalized match rate for a specific sub-service line
def calculate_average_match_rate_norm(df, sub_service_line):
    column_name = f"match_rate_Norm_{sub_service_line.replace(' ', '_')}"  # Adjust column name formatting if needed
    if column_name in df.columns:
        average = df[column_name].mean()
        return round(average, 2)  # Round to two decimal places
    else:
        return "Column not found"

# Check if at least one service line and one sub-service line are selected
if selected_service_lines and selected_sub_service_lines:
    # Copy the DataFrame for independent calculations
    df_copy = df_proj.copy()

    # Perform match rate calculations for each sub-service line independently
    for i, ssl in enumerate(selected_sub_service_lines):
        service_line = selected_service_lines[min(i, len(selected_service_lines) - 1)]
        suffix = ssl.replace(' ', '_')#.replace('&', 'and')  # Consistent with calculate_match_rate
        calculate_and_normalize_match_rate(df_copy, service_line, ssl, suffix)

    # Filter DataFrame based on selected project or designation
    if selected_project != 'None':
        filtered_df = df_copy[df_copy['Project Code'] == selected_project]
    elif selected_designations:
        filtered_df = df_copy[df_copy['Designation'].isin(selected_designations)]
    else:
        filtered_df = df_copy
    # Create a layout based on the number of sub-service lines selected
    cols = st.columns(len(selected_sub_service_lines))

    # Display match rate tables and average normalized match rates for each sub-service line
    for i, ssl in enumerate(selected_sub_service_lines):
        with cols[i]:
            suffix = ssl.replace(' ', '_')
            ssl_columns = ['Employee ID', 'Employee Name', 'Designation', 
                           f'match_rate_{suffix}', f'match_rate_Norm_{suffix}']
            st.write(f"Match Rate Analysis for {ssl}:")

            # Filter DataFrame for each project if selected
        if selected_project != 'None':
            project_filtered_df = df_copy[df_copy['Project Code'] == selected_project]
            # st.dataframe(project_filtered_df[ssl_columns])

            # Calculate and display the average normalized match rate for the project
            project_avg_match_rate_norm = calculate_average_match_rate_norm(project_filtered_df, ssl)
            st.metric(label=f"Average Norm. Rate ({ssl})", value=project_avg_match_rate_norm)
        elif selected_designations:
            designation_filtered_df = df_copy[df_copy['Designation'].isin(selected_designations)]
            # st.dataframe(designation_filtered_df[ssl_columns])

            # Calculate and display the average normalized match rate for the selected designations
            designation_avg_match_rate_norm = calculate_average_match_rate_norm(designation_filtered_df, ssl)
            st.metric(label=f"Average Norm. Rate ({ssl})", value=designation_avg_match_rate_norm)
        else:
            # st.dataframe(df_copy[ssl_columns])

            # Calculate and display the overall average normalized match rate
            overall_avg_match_rate_norm = calculate_average_match_rate_norm(df_copy, ssl)
            st.metric(label=f"Overall Avg. Norm. Rate ({ssl})", value=overall_avg_match_rate_norm)
else:
    st.write("Please select a service line and a sub-service line to view the match rate analysis.")
    
    
#----------------------------------------------------------------------
# what if analysis    

# ... [existing Streamlit app code, including current match rate calculations and displays] ...

# Function to simulate adding an employee to the selected project
def simulate_employee_addition_to_project(df, employee_ids, project_code):
    df_simulated = df.copy()
    df_simulated.loc[df_simulated['Employee Name'].isin(employee_ids), 'Project Code'] = project_code
    return df_simulated

# Function to recalculate match rates
def recalculate_match_rates(df, service_lines, sub_service_lines):
    # Assume calculate_and_normalize_match_rate function is already defined
    for ssl in sub_service_lines:
        service_line = service_lines[min(i, len(service_lines) - 1)]
        suffix = ssl.replace(' ', '_').replace('&', 'and')
        calculate_and_normalize_match_rate(df, service_line, ssl, suffix)
        
# Debug version of calculate_average_match_rate_norm
def calculate_average_match_rate_norm_debug(df, sub_service_line):
    column_name = f"match_rate_Norm_{sub_service_line.replace(' ', '_')}"
    if column_name in df.columns:
        # Debug: Print values being averaged
        # st.write(f"Values for {column_name}: ", df)  # Show first few values
        average = df[column_name].mean()
        return round(average, 2)  # Round to two decimal places
    else:
        return "Column not found"


# Function to simulate project team changes
def simulate_project_team_change(df, employees_to_add, employees_to_remove, project_code):
    df_simulated = df.copy()
    # Adding employees to the project
    df_simulated.loc[df_simulated['Employee Name'].isin(employees_to_add), 'Project Code'] = project_code
    # Removing employees from the project
    df_simulated.loc[df_simulated['Employee Name'].isin(employees_to_remove), 'Project Code'] = None  # Or another appropriate value
    return df_simulated

# Streamlit UI for "What-If" Analysis with Employee Addition and Removal
st.sidebar.header("What-If Analysis: Modifying Project Team")
employees_to_add = st.sidebar.multiselect("Select Employee(s) to Add", df_proj['Employee Name'].unique(), key="add")
employees_to_remove = st.sidebar.multiselect("Select Employee(s) to Remove", df_proj[df_proj['Project Code'] == selected_project]['Employee Name'].unique(), key="remove")

# Button to perform the what-if analysis
if st.sidebar.button("Perform What-If Analysis"):
    st.subheader("What-If Analysis Results")

    # Simulate changes to the project team
    df_simulated = simulate_project_team_change(df_proj, employees_to_add, employees_to_remove, selected_project)

    # Recalculate match rates for the simulated DataFrame
    recalculate_match_rates(df_simulated, selected_service_lines, selected_sub_service_lines)

    # Display the recalculated match rates for comparison
    st.write("Match Rates After Modifying Project Team:")
    for ssl in selected_sub_service_lines:
        suffix = ssl.replace(' ', '_').replace('&', 'and')
        ssl_columns = ['Employee Name', 'Designation', f'match_rate_{suffix}', f'match_rate_Norm_{suffix}']
        st.write(f"Match Rate Analysis for {ssl} (Simulated):")
        st.dataframe(df_simulated[df_simulated['Project Code'] == selected_project][ssl_columns])
        
        # Calculate and display the average normalized match rate
        avg_norm_rate = calculate_average_match_rate_norm(df_simulated[df_simulated['Project Code'] == selected_project][ssl_columns], ssl)
        st.metric(label=f"Average Norm. Rate for {ssl} (Simulated)", value=avg_norm_rate)

#----------------------------------------------------------------
# planning a new project

st.sidebar.header("Project Planning for Upcoming Projects")

# Define the order of designations
ordered_designations = ['Analyst-Intern', 'Future Gears Analyst', 'Analyst', 'Associate Consultant', 
                        'Consultant', 'Manager', 'Senior Manager', 'Director', 'Principal', 
                        'Associate Partner', 'Partner']

# Step 1: Role Selection in specified order
st.sidebar.subheader("Needed Roles for the Project")
designation_counts = {designation: st.sidebar.number_input(f"Number of {designation}", min_value=0, max_value=10, step=1) 
                      for designation in ordered_designations if designation in df_proj['Designation'].unique()}



    # Add a numeric input in the sidebar for the match rate norm threshold
match_rate_norm_threshold = st.sidebar.number_input('Minimum Match Rate Norm Threshold', min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    
    
    # In the Streamlit sidebar, allow the user to specify the project start date
project_start_date = st.sidebar.date_input("Project Start Date", value=pd.to_datetime("today"))
    # Convert project_start_date to pandas Timestamp if it's not already
project_start_date = pd.to_datetime(project_start_date)


#---------------------------
def generate_suggested_team(df, designation_counts, suffix, consider_availability=False, project_start_date=None, random_state=None):
    suggested_team = pd.DataFrame()
    project_start_date = pd.to_datetime(project_start_date)  # Ensure this is in datetime format
    
    # First, transform 'To Date' to ensure it's in datetime format across the DataFrame
    df['To Date'] = pd.to_datetime(df['To Date'])

    # If considering availability, create a series with the latest 'To Date' for each employee
    if consider_availability and project_start_date is not None:
        latest_to_date_per_employee = df.groupby('Employee Name')['To Date'].max()
        df = df.join(latest_to_date_per_employee, on='Employee Name', rsuffix='_latest')
        
    for designation, count in designation_counts.items():
        if count > 0:
            eligible_candidates = df[(df['Designation'] == designation) & (df[f'match_rate_Norm_{suffix}'] > match_rate_norm_threshold)]
            
            if consider_availability and project_start_date is not None:
                two_weeks_before_start = project_start_date - pd.Timedelta(weeks=2)
                # Filter based on the latest 'To Date'
                eligible_candidates = eligible_candidates[
                    (eligible_candidates['To Date_latest'] >= two_weeks_before_start) &
                    (eligible_candidates['To Date_latest'] <= project_start_date + pd.Timedelta(weeks=4))
                ]
            
            selected_candidates = eligible_candidates.sample(min(count, len(eligible_candidates)), random_state=random_state)
            suggested_team = pd.concat([suggested_team, selected_candidates])
            
    
            
    return suggested_team


#-------------

# Option to consider employee availability
consider_availability = st.sidebar.checkbox("Consider Employee Availability")

# Button to generate teams
if st.sidebar.button("Generate Suggested Teams"):
    st.subheader("Suggested Teams and Match Rate Analysis")

    team_cols = st.columns(3)  # Create three columns for the teams
    
    for i in range(3):
        with team_cols[i]:
            st.markdown(f"**Team {i + 1}**")
            random_seed = random.randint(1, 10000)  # Ensure different teams
            suggested_team = generate_suggested_team(
                test_df, 
                designation_counts, 
                suffix, 
                consider_availability=consider_availability, 
                project_start_date=project_start_date, 
                random_state=random_seed
            )
            
            # Display the suggested team
            st.write(suggested_team[['Employee Name', 'Designation', f'match_rate_Norm_{suffix}', 'To Date']])
            
            # Calculate and display match rate for this team
            avg_norm_rate = calculate_average_match_rate_norm(suggested_team, ssl)
            # Implement display of match rate for the team     # Display match rates and average normalized match rates (Assuming these functions are already implemented)
            st.metric(label=f"Average Norm. Rate for {ssl} (Team {i + 1})", value=avg_norm_rate)





