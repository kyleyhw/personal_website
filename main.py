import streamlit as st
import requests
from pathlib import Path

# --- PATH SETTINGS ---
# Update this path to the location of your CV PDF file
CV_PATH = Path("assets/kyle_wong_2page_cv_jun_2025.pdf")

# --- GITHUB SETUP ---
GITHUB_USERNAME = "kyleyhw"  # <-- IMPORTANT: Replace with your username

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital CV | John Doe",
    page_icon="👋",
    layout="wide"
)


# --- CV DOWNLOAD ---
# This function reads the CV file and provides it for download
def get_cv_as_bytes():
    with open(CV_PATH, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    return PDFbyte


# --- GITHUB REPO FETCHER ---
# This function fetches your pinned repositories from GitHub
def fetch_pinned_repos(username):
    # Using an external service as a proxy to get pinned repos, as GitHub API v4 (GraphQL) is more complex
    # This is a simpler approach for this use case.
    try:
        response = requests.get(f"https://gh-pinned-repos.egoist.dev/?username={username}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching GitHub repos: {e}")
        return None


# --- SIDEBAR & MAIN CONTENT ---

# --- Sidebar ---
with st.sidebar:
    st.image("assets/profile_pic.jpeg", width=250)  # <-- Add your profile picture in an 'assets' folder
    st.title("John Doe")  # <-- Your Name
    st.write("Senior Data Analyst at Fictional Corp.")  # <-- Your Title
    st.write("📍 Cambridge, UK")  # <-- Your Location

    st.download_button(
        label="📄 Download CV",
        data=get_cv_as_bytes(),
        file_name="JohnDoe_CV.pdf",  # <-- The name for the downloaded file
        mime="application/octet-stream",
    )

    st.write("---")
    st.subheader("Contact")
    st.write("📫: john.doe@email.com")
    st.write("🔗: [LinkedIn](https://linkedin.com/in/yourprofile)")  # <-- Add your LinkedIn
    st.write("🐙: [GitHub](https://github.com/YourGitHubUsername)")  # <-- Add your GitHub

# --- Main Page ---
st.title("About Me")
st.write(
    """
    I am a highly motivated and detail-oriented Senior Data Analyst with over 8 years of experience in turning data into actionable insights. 
    My expertise lies in statistical analysis, machine learning, and data visualization. I am passionate about solving complex problems and have a proven track record of developing data-driven strategies that lead to significant business growth. I am proficient in Python, SQL, and various business intelligence tools.
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
    st.info("No pinned repositories found.")
else:
    for repo in repos:
        st.markdown(f"#### [{repo['repo']}]({repo['link']})")
        st.write(f"⭐ {repo.get('stars', 'N/A')} | 🍴 {repo.get('forks', 'N/A')}")
        st.write(repo['description'])
        st.write(f"**Language:** {repo['language']}")
        st.write("---")