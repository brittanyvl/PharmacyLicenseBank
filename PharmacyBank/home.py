import streamlit as st
from PharmacyBank.data_loader import load_data
from PharmacyBank.analysis import *

def home_page():
    # Load data
    data = load_data()

    # Store the data in session state (to make it available across interactions)
    st.session_state['data'] = data

    # Retrieve and display the data from session state
    if 'data' in st.session_state:
        # Create 5 columns for metrics to be displayed horizontally
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Open 503Bs", metric_total_pharmacies)

        with col2:
            st.metric("% Compounding Sterile", f"{metric_percent_intend_sterile}%")  # Adding '%' sign

        with col3:
            st.metric("% Uninspected by FDA", f"{metric_percent_fda_uninspected}%")  # Adding '%' sign

        with col4:
            st.metric("% with FDA Recalls", f"{metric_percent_recalls_conducted}%")  # Adding '%' sign

        with col5:
            st.metric("% with 483s Issued", f"{metric_percent_483s_issued}%")  # Adding '%' sign

        # Optionally display the DataFrame below the metrics
        st.dataframe(st.session_state['data'])

        # Optionally display the DataFrame below the metrics
        st.dataframe(st.session_state['data'])

    else:
        st.write("No data found!")
