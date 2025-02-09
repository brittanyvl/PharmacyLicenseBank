import streamlit as st

def display_header():
    st.title("Welcome to My Modular Streamlit App")
    st.write("This is an example of a well-structured Streamlit app.")

def display_sidebar():
    menu = st.sidebar.selectbox("Select a Page", ["Home", "About"])
    return menu
