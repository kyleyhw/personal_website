import streamlit as st
import requests
from PIL import Image
from utils import load_font

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kyle Wong | Astrophysics",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the custom font
load_font()

# --- GITHUB AND ASSET SETUP ---
GITHUB_USERNAME = "kyleyhw"
CV_URL = "https://kyleyhw.github.io/kyle_wong_cv/kyle_wong_cv_mar_2025.pdf"
PROFILE_PIC_URL = "https://raw.githubusercontent.com/kyleyhw/personal_website/master/assets/profile_pic.jpeg"

# --- SVG ICONS ---
ICON_STYLE = 'style="vertical-align: middle; margin-right: 10px; width: 24px; height: 24px;"'
SVG_FILL_COLOR = "#000000"
EMAIL_ICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{SVG_FILL_COLOR}" {ICON_STYLE}><path d="M0 3v18h24v-18h-24zm21.518 2l-9.518 7.713-9.518-7.713h19.036zm-19.518 14v-11.817l10 8.104 10-8.104v11.817h-20z"/></svg>'
GITHUB_ICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{SVG_FILL_COLOR}" {ICON_STYLE}><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.91 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'
LINKEDIN_ICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{SVG_FILL_COLOR}" {ICON_STYLE}><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>'

# --- SIDEBAR ---
with st.sidebar:
    try:
        response = requests.get(PROFILE_PIC_URL, stream=True)
        if response.status_code == 200:
            profile_pic = Image.open(response.raw)
            st.image(profile_pic, width=250)
        else:
            st.warning("Could not load profile picture.")
    except Exception as e:
        st.warning(f"Error loading profile picture: {e}")

    st.title("Kyle Wong")
    st.write("MASt Astrophysics Student")
    st.write("University of Cambridge")

    st.markdown(f"[View CV]({CV_URL})", unsafe_allow_html=True)

    st.write("---")
    st.subheader("contact")
    st.markdown(f"{EMAIL_ICON} [kyhw2@cam.ac.uk](mailto:kyhw2@cam.ac.uk)", unsafe_allow_html=True)
    st.markdown(f"{GITHUB_ICON} [kyleyhw](https://github.com/{GITHUB_USERNAME})", unsafe_allow_html=True)
    st.markdown(f"{LINKEDIN_ICON} [Kyle Wong](https://www.linkedin.com/in/kyle-wong-a95030281/)",
                unsafe_allow_html=True)

# --- HOME PAGE CONTENT ---
st.title("about me")
st.write(
    """
    I am a postgraduate student at the University of Cambridge pursuing a Master of Advanced Study in Astrophysics. 
    My academic and research interests are centered on computational cosmology and gravitational wave astronomy. 
    I have a strong foundation in physics and mathematics, graduating with High Distinction from the University of Toronto.

    My research experience includes developing simulations for 21-cm cosmology with the **Cosmic Dawn Group** at Cambridge, 
    aiming to support future radio astronomy experiments like the Square Kilometre Array (SKA). I have also worked on probing 
    neutron star physics using gravitational wave data from the **LIGO Scientific Collaboration** and contributed to the data 
    analysis pipeline for the **HERA** radio telescope collaboration. I am proficient in Python, MATLAB, and various high-performance 
    computing tools, with a focus on simulation, Bayesian inference, and data visualization.
    """
)
