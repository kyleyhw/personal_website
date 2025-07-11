import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kyle Wong | Astrophysics",
    page_icon="🔭",
    layout="wide"
)

# --- GITHUB AND ASSET SETUP ---
GITHUB_USERNAME = "kyleyhw"
# Permalink to your CV PDF on GitHub, which opens in the browser
CV_URL = "https://raw.githubusercontent.com/kyleyhw/kyle_wong_cv/e7d2e8333b1d3c22502dc5a9bcadac1c95cb7251/kyle_wong_cv_mar_2025.pdf"
# Raw URL to your profile picture on GitHub
PROFILE_PIC_URL = "https://raw.githubusercontent.com/kyleyhw/personal_website/master/assets/profile_pic.jpeg"


# --- GITHUB REPO FETCHER ---
# This function fetches your pinned repositories from GitHub.
@st.cache_data(ttl=3600)  # Cache the data for 1 hour
def fetch_pinned_repos(username):
    """
    Fetches pinned repositories for a given GitHub username.
    Uses an external proxy as the official GitHub GraphQL API is more complex for this use case.
    """
    try:
        response = requests.get(f"https://gh-pinned-repos.egoist.dev/?username={username}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch GitHub repos. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching GitHub repos: {e}")
        return None


# --- SIDEBAR & MAIN CONTENT ---

# --- Sidebar ---
with st.sidebar:
    st.image(PROFILE_PIC_URL, width=250)
    st.title("Kyle Wong")
    st.write("MASt Astrophysics Student")
    st.write("University of Cambridge")

    st.markdown(f"📄 [View CV]({CV_URL})")

    st.write("---")
    st.subheader("Contact")
    st.write(f"📫 kyhw2@cam.ac.uk")
    st.write(f"🐙 [GitHub Profile](https://github.com/{GITHUB_USERNAME})")

# --- Main Page ---
st.title("About Me")
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

st.write("---")

# --- Portfolio Section ---
st.header("Portfolio")
st.subheader("Pinned GitHub Projects")

# Fetch and display repositories
repos = fetch_pinned_repos(GITHUB_USERNAME)

if repos is None:
    st.warning("Could not fetch GitHub projects. Please check the username or try again later.")
elif not repos:
    st.info(f"No pinned repositories found for user '{GITHUB_USERNAME}'.")
else:
    # Create a two-column layout for the projects
    col1, col2 = st.columns(2)
    for i, repo in enumerate(repos):
        # Distribute projects between the two columns
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"#### [{repo['repo']}]({repo['link']})")
            st.write(f"⭐ {repo.get('stars', 'N/A')} | � {repo.get('forks', 'N/A')}")
            st.write(repo['description'])
            st.write(f"**Language:** {repo.get('language', 'N/A')}")
            st.write("---")
