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
# URL to the CV hosted on GitHub Pages for in-browser viewing
CV_URL = "https://kyleyhw.github.io/kyle_wong_cv/kyle_wong_cv_mar_2025.pdf"
# Raw URL to your profile picture on GitHub
PROFILE_PIC_URL = "https://raw.githubusercontent.com/kyleyhw/personal_website/master/assets/profile_pic.jpeg"


# --- GITHUB REPO FETCHER ---
# This function fetches your public repositories from the official GitHub API.
@st.cache_data(ttl=3600)  # Cache the data for 1 hour
def fetch_github_repos(username):
    """
    Fetches public repositories for a given GitHub username using the official GitHub API,
    sorted by stars.
    """
    url = f"https://api.github.com/users/{username}/repos?sort=stars&per_page=6"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                # Sort repositories by stars in descending order and take the top 6
                repos = response.json()
                repos.sort(key=lambda r: r.get('stargazers_count', 0), reverse=True)
                return repos[:6]
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to parse the response from the GitHub API.")
                return None
        else:
            st.error(f"GitHub API returned status code {response.status_code}.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
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
st.subheader("Featured GitHub Projects")

# Fetch and display repositories
repos = fetch_github_repos(GITHUB_USERNAME)

if repos is None:
    st.warning("Could not fetch GitHub projects at the moment. This may be a temporary issue. Please try again later.")
elif not repos:
    st.info(f"No public repositories found for user '{GITHUB_USERNAME}'.")
else:
    # Create a two-column layout for the projects
    col1, col2 = st.columns(2)
    for i, repo in enumerate(repos):
        # Use .get() for all keys to prevent errors if a key is missing from the API response
        repo_name = repo.get('name', 'No name')
        repo_link = repo.get('html_url', '#')
        repo_desc = repo.get('description', 'No description provided.')
        repo_lang = repo.get('language', 'N/A')
        repo_stars = repo.get('stargazers_count', 0)
        repo_forks = repo.get('forks_count', 0)

        # Distribute projects between the two columns
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"#### [{repo_name}]({repo_link})")
            st.write(f"⭐ {repo_stars} | 🍴 {repo_forks}")
            st.write(repo_desc)
            st.write(f"**Language:** {repo_lang}")
            st.write("---")
