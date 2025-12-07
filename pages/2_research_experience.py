import streamlit as st
from utils import load_font

# Load the custom font
load_font()

# --- RESEARCH EXPERIENCE PAGE CONTENT ---
st.title("research experience")

with st.expander(
        "Master of Advanced Study Research Project | *Institute of Astronomy, University of Cambridge (Oct 2024 - Sep 2025)*"):
    st.markdown("""
    - **Position:** Postgraduate Student
    - **Supervisor:** Prof. Anastasia Fialkov
    - **Topic:** Implementation and statistical testing of variable initial conditions (cosmologies) in 21cmSPACE code package for simulating the distribution of hydrogen gas clouds in the early universe, making possible efficient forecasting of future radio astronomy experiments, most notably for the Square Kilometre Array (SKA).
    - **Skills:** Simulation, high performance computing, data visualization, cosmology, Python, MATLAB
    """)

with st.expander(
        "Canadian Institute for Theoretical Astrophysics Summer Undergraduate Research Fellowship | *Toronto, Ontario, Canada (May 2023 - Dec 2023)*"):
    st.markdown("""
    - **Position:** Undergraduate Researcher
    - **Supervisor:** Dr. Philippe Landry
    - **Topic:** Probing neutron star tidal deformability from gravitational wave signals using Markov chain Monte Carlo (MCMC) parameter estimation in many dimensions, and incorporating new models for neutron star equation of state correlations in the analysis pipeline of Laser Interferometer Gravitational-Wave Observatory (LIGO) Scientific Collaboration gravitational wave data.
    - **Skills:** Simulation, MCMC, Bayesian inference, high performance computing, Python
    """)

with st.expander("McGill Space Institute Summer Undergraduate Research Award | *Montreal, Quebec, Canada (May 2022 - Apr 2023)*"):
    st.markdown("""
    - **Position:** Undergraduate Researcher
    - **Supervisor:** Prof. Adrian Liu (Trottier Space Institute)
    - **Topic:** Incorporating statistical priors into the power spectrum data estimator used in the data pipeline, for analysis of radio astronomy data from the Hydrogen Epoch of Reionization Array (HERA) collaboration's cosmic dawn experiment, using the Python programming language.
    - **Skills:** Simulation, Fourier transform, radio astronomy, radio frequency interference, Python
    """)
