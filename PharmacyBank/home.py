import streamlit as st

def home_page():
    st.header("Home Page")
    st.write("This is the home page of the app. You can add content here.")
    # Add any interactive widgets, charts, or data here
    st.write("Here's some random data:", st.session_state.get("data"))
