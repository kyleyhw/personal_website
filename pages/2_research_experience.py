import streamlit as st

from load_style import *
load_font()

# --- RESEARCH & SKILLS PAGE CONTENT ---
st.title("Research & Skills")

st.header("Research Experience")

st.subheader("Master's of Advanced Study Research Project")
st.write("*Institute of Astronomy, University of Cambridge (Oct 2024 - Present)*")
with st.expander("Details"):
    st.markdown("""
    - **Topic:** Implementation and statistical testing of variable initial conditions and resolution in the 21cmSPACE code package for simulating hydrogen gas clouds in the early universe.
    - **Goal:** To enable efficient forecasting for future radio astronomy experiments, particularly the Square Kilometre Array (SKA).
    - **Skills:** Simulation, MATLAB, High-Performance Computing, Linux, Data Visualization, Cosmology.
    """)

st.subheader("Canadian Institute for Theoretical Astrophysics (CITA) Summer Fellowship")
st.write("*University of Toronto (May 2023 - Dec 2023)*")
with st.expander("Details"):
    st.markdown("""
    - **Topic:** Probing neutron star tidal deformability from gravitational wave signals using Markov Chain Monte Carlo (MCMC) parameter estimation.
    - **Goal:** Incorporating new models for neutron star equation of state correlations into the LIGO Scientific Collaboration's analysis pipeline.
    - **Skills:** Simulation, MCMC, Machine Learning, Bayesian Inference, High-Performance Computing, Linux.
    """)

st.subheader("McGill Space Institute Summer Research Award")
st.write("*McGill University (May 2022 - Apr 2023)*")
with st.expander("Details"):
    st.markdown("""
    - **Topic:** Incorporating statistical priors into the power spectrum data estimator for the Hydrogen Epoch of Reionization Array (HERA) collaboration.
    - **Goal:** To improve the analysis of radio astronomy data from HERA's cosmic dawn experiment.
    - **Skills:** Simulation, Fourier Transform, Radio Astronomy, Python.
    """)

st.write("---")

st.header("Technical Skills")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Programming")
    st.markdown("""
    - Python
    - MATLAB
    - Java
    - *Emphasis on design, vectorization, and best practices.*
    """)

with col2:
    st.subheader("Data Analysis & Simulation")
    st.markdown("""
    - Fast Fourier Transform (FFT)
    - Numerical Methods (differentiation, integration, root finding)
    - Monte Carlo Methods
    - Bayesian Inference
    """)

st.subheader("Key Libraries & Software")
st.markdown("""
- **Bilby:** Extensive use for parameter estimation.
- **21cmSPACE:** Cosmological simulation package.
- **CAMB & recfast++:** Astrophysical simulation packages.
""")
