import streamlit as st
from utils import load_font

# Load the custom font
load_font()

# --- RESEARCH & SKILLS PAGE CONTENT ---
st.title("research experience")

st.header("research projects")

with st.expander(
        "Master's of Advanced Study Research Project | *Institute of Astronomy, University of Cambridge (Oct 2024 - Present)*"):
    st.markdown("""
    - **Topic:** Implementation and statistical testing of variable initial conditions and resolution in the 21cmSPACE code package for simulating hydrogen gas clouds in the early universe.
    - **Goal:** To enable efficient forecasting for future radio astronomy experiments, particularly the Square Kilometre Array (SKA).
    - **Skills:** Simulation, MATLAB, High-Performance Computing, Linux, Data Visualization, Cosmology.
    """)

with st.expander(
        "Canadian Institute for Theoretical Astrophysics (CITA) Summer Fellowship | *University of Toronto (May 2023 - Dec 2023)*"):
    st.markdown("""
    - **Topic:** Probing neutron star tidal deformability from gravitational wave signals using Markov Chain Monte Carlo (MCMC) parameter estimation.
    - **Goal:** Incorporating new models for neutron star equation of state correlations into the LIGO Scientific Collaboration's analysis pipeline.
    - **Skills:** Simulation, MCMC, Machine Learning, Bayesian Inference, High-Performance Computing, Linux.
    """)

with st.expander("McGill Space Institute Summer Research Award | *McGill University (May 2022 - Apr 2023)*"):
    st.markdown("""
    - **Topic:** Incorporating statistical priors into the power spectrum data estimator for the Hydrogen Epoch of Reionization Array (HERA) collaboration.
    - **Goal:** To improve the analysis of radio astronomy data from HERA's cosmic dawn experiment.
    - **Skills:** Simulation, Fourier Transform, Radio Astronomy, Python.
    """)

st.write("---")

st.header("technical skills")

st.subheader("programming")
st.markdown("""
- Python
- MATLAB
- Java
- *Emphasis on design, vectorization, and best practices.*
""")

st.subheader("data analysis & simulation")
st.markdown("""
- Fast Fourier Transform (FFT)
- Numerical Methods (differentiation, integration, root finding)
- Monte Carlo Methods
- Bayesian Inference
""")

st.subheader("key libraries & software")
st.markdown("""
- **Bilby:** Extensive use for parameter estimation.
- **21cmSPACE:** Cosmological simulation package.
- **CAMB & recfast++:** Astrophysical simulation packages.
""")
