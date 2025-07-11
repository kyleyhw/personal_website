import streamlit as st

def load_font():
    # --- LOAD INTER FONT ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
        </style>
        """,
        unsafe_allow_html=True,
    )