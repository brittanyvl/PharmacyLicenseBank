import streamlit as st
from PharmacyBank import about, home, data_loader, layout, analysis
from pathlib import Path

def load_css():
    with open(Path(__file__).parent / "PharmacyBank" / "style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():

    # Set page title
    st.set_page_config(page_title="My Modular Streamlit App", layout="wide")

    # Load Stylesheet
    load_css()

    # Display header
    layout.display_header()

    # Sidebar menu
    menu = layout.display_sidebar()

    # Navigate to the right page based on menu selection
    if menu == "Home":
        home.home_page()
    elif menu == "About":
        about.about_page()

if __name__ == "__main__":
    main()
