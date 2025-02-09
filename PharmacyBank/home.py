import streamlit as st
from PharmacyBank.data_loader import load_data  # Correct import

def home_page():
    # Load data
    data = load_data()

    # Store the data in session state (to make it available across interactions)
    st.session_state['data'] = data

    # Retrieve and display the data from session state
    if 'data' in st.session_state:
        #st.write("Here's some random data:")
        st.dataframe(st.session_state['data'])
    else:
        st.write("No data found!")
