import streamlit as st

def display_header():
    st.title("Active 503B Outsourcing Facilities")
    st.write("A data application by Brittany Campos")

def display_sidebar():
    menu = st.sidebar.selectbox("Select a Page", ["Home", "About"])
    return menu
