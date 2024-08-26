# # -*- coding: utf-8 -*-
# """
# Created on Sun Dec 24 19:42:21 2023
import streamlit as st
# import page1
# import page2



st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")
# Main app script
st.title('My Multi-Page Streamlit App')

# Navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Select a Page', ['Page 1', 'Page 2'])

if page == 'Page 1':
    exec(open("page1.py").read())
# elif page == 'Page 2':
#     exec(open("page2.py").read())
