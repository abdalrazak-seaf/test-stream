# # -*- coding: utf-8 -*-
# """
# Created on Sun Dec 24 19:42:21 2023
import streamlit as st

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

# Main app script
st.title('My Multi-Page Streamlit App')

# Navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Select a Page', ['Page 1', 'Page 2'])

if page == 'Page 1':
    exec(open("pages/page1.py").read())
elif page == 'Page 2':
    exec(open("pages/page2.py").read())