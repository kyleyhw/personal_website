import streamlit as st

# --- LOAD INTER FONT ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    </style>
    """,
    unsafe_allow_html=True,
)

# --- PRESENTATIONS PAGE CONTENT ---
st.title("presentations")

st.markdown("""
- **Impact of Variable Cosmology on the 21-cm Cosmic Dawn Signal**
  - *Master's Project Presentation, University of Cambridge (2025)*
- **Interim Progress Presentation**
  - *Cambridge Cosmic Dawn Group (2024)*
- **Estimating Neutron Star Tidal Deformability**
  - *CITA Undergraduate Research Showcase (2023)*
- **PHY478 Physics Project Final Presentation**
  - *University of Toronto (2023)*
- **Two Presentations on Neutron Star Physics**
  - *CITA Compact Objects Group (2023)*
""")
