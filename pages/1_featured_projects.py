import streamlit as st
import requests
from bs4 import BeautifulSoup
from utils import load_font

# Load the custom font
load_font()

# --- LOAD CUSTOM CSS FOR PROJECT CARDS ---
st.markdown(
    """
    <style>
# --- LOAD CUSTOM CSS FOR PROJECT CARDS ---
st.markdown(
    """
    <style>
    /* Style for the project cards - Using CSS Grid for consistent height */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    .project-card {
        border: 1px solid #d0d7de; /* Light gray border */
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #f6f8fa; /* Light background */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
        height: 100%; /* Fill the grid cell */
    }
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .project-card h4 {
        margin-top: 0;
    }
    .project-card h4 a {
        text-decoration: none;
        color: #0969da; /* Standard link blue */
    }
    .project-card p {
        color: #57606a; /* Dark gray text */
        font-size: 0.9rem;
        flex-grow: 1;
        margin-bottom: 1rem;
    }
    .project-footer {
        font-size: 0.8rem;
        color: #57606a;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
    }
    .lang-color-dot {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600)
def fetch_repos(username, repo_whitelist):
    """
    Fetches specific repositories from the public GitHub profile 'Repositories' tab.
    No API token required.
    """
    url = f"https://github.com/{username}?tab=repositories"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            st.error(f"Failed to load GitHub profile (Status: {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        # Find all repo list items
        repo_list = soup.find("div", id="user-repositories-list")
        if not repo_list:
             # Fallback if ID changes or not found
            items = soup.find_all("li", itemprop="owns")
        else:
            items = repo_list.find_all("li")

        repos_data = []
        
        # Helper to normalize names for comparison
        whitelist_set = {r.lower() for r in repo_whitelist}

        for item in items:
            # Repo Name and URL
            repo_link = item.find("a", itemprop="name codeRepository")
            if not repo_link:
                continue
                
            name = repo_link.get_text(strip=True)
            if name.lower() not in whitelist_set:
                continue

            project_url = f"https://github.com{repo_link['href']}"

            # Description (prop="description")
            desc_tag = item.find("p", itemprop="description")
            description = desc_tag.get_text(strip=True) if desc_tag else "No description available."

            # Language and Color
            lang_tag = item.find("span", itemprop="programmingLanguage")
            lang = lang_tag.get_text(strip=True) if lang_tag else "N/A"

            color_tag = item.find("span", class_="repo-language-color")
            color = color_tag["style"].split("background-color:")[1].strip().rstrip(";") if color_tag else "#808080"

            repos_data.append({
                "name": name,
                "url": project_url,
                "description": description,
                "language": lang,
                "color": color
            })
            
        # Sort repos based on the order in the whitelist
        repos_data.sort(key=lambda x: repo_whitelist.index(x['name']) if x['name'] in repo_whitelist else 999)
        
        return repos_data

    except Exception as e:
        st.error(f"Error scraping GitHub: {e}")
        return None


# --- PORTFOLIO PAGE CONTENT ---
st.title("featured code repositories")
st.subheader("a selection of my GitHub repositories.")

GITHUB_USERNAME = "kyleyhw"
REPO_NAMES = [
    "quant_core",
    "sound_simulation",
    "double_pendulum_stabilization",
    "digit_recognition",
    "tracing_turing_machines",
    "mast_project_final_report"
]

projects = fetch_repos(GITHUB_USERNAME, REPO_NAMES)

if not projects:
    st.info("No repositories found. Please check your internet connection or the repository list.")
else:
    # Generate HTML for the project cards
    project_cards_html = ""
    for repo in projects:
        repo_name = repo['name']
        repo_url = repo['url']
        description = repo['description']
        # skills = repo.get('skills', '') 
        lang_name = repo['language']
        lang_color = repo['color']

        project_cards_html += f"""
<div class="project-card">
    <div>
        <h4><a href="{repo_url}" target="_blank">{repo_name}</a></h4>
        <p>{description}</p>
    </div>
    <div class="project-footer">
        <span class="lang-color-dot" style="background-color:{lang_color};"></span> {lang_name}
    </div>
</div>
"""

    # Display the cards in a grid
    st.markdown(f'<div class="project-grid">{project_cards_html}</div>', unsafe_allow_html=True)
