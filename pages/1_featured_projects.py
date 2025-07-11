import streamlit as st
import requests
import html
from utils import load_font

# Load the custom font
load_font()

# --- LOAD CUSTOM CSS FOR PROJECT CARDS ---
st.markdown(
    """
    <style>
    /* Style for the project cards - Using Flexbox for alignment */
    .project-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    .project-card {
        flex: 1 1 350px; /* Flex-grow, flex-shrink, flex-basis */
        border: 1px solid #d0d7de; /* Light gray border */
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #f6f8fa; /* Light background */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
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

# --- GITHUB AND ASSET SETUP ---
GITHUB_USERNAME = "kyleyhw"


# --- GITHUB REPO FETCHER ---
@st.cache_data(ttl=3600)
def fetch_pinned_repos(username: str, github_token: str):
    """
    Fetches pinned repositories using the official GitHub GraphQL API.
    Requires a Personal Access Token (PAT) for authentication.
    """
    api_url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {github_token}"}
    query = """
    query($username: String!) {
      user(login: $username) {
        pinnedItems(first: 6, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              description
              url
              stargazerCount
              forkCount
              primaryLanguage {
                name
                color
              }
            }
          }
        }
      }
    }
    """
    variables = {"username": username}

    try:
        response = requests.post(api_url, json={"query": query, "variables": variables}, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            if "errors" in response_json:
                st.error(f"GitHub API returned errors: {response_json['errors']}")
                return None
            return response_json.get("data", {}).get("user", {}).get("pinnedItems", {}).get("nodes")
        else:
            st.error(f"GitHub API error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None
    except (KeyError, TypeError) as e:
        st.error(f"Error parsing the response from GitHub. Please check your token and username. Details: {e}")
        return None


# --- PORTFOLIO PAGE CONTENT ---
st.title("featured projects")
st.subheader("a selection of my pinned GitHub repositories.")

if "GITHUB_TOKEN" not in st.secrets:
    st.error("`GITHUB_TOKEN` not found in Streamlit secrets. Please follow the instructions to add it.")
else:
    github_token = st.secrets["GITHUB_TOKEN"]
    repos = fetch_pinned_repos(GITHUB_USERNAME, github_token)

    if repos is None:
        st.warning(
            "Could not fetch GitHub projects. Please check the app logs or the error messages above for more details.")
    elif not repos:
        st.info(
            f"No pinned repositories found for user '{GITHUB_USERNAME}'. Please ensure you have pinned some repositories on your GitHub profile.")
    else:
        # Generate HTML for the project cards
        project_cards_html = ""
        for repo in repos:
            repo_name = repo.get('name', 'No name')
            repo_url = repo.get('url', '#')
            # Escape the description to prevent HTML injection issues
            description = html.escape(repo.get('description', 'No description provided.'))

            lang_name = "N/A"
            lang_color = "#808080"
            if repo.get('primaryLanguage'):
                lang_name = repo['primaryLanguage'].get('name', 'N/A')
                lang_color = repo['primaryLanguage'].get('color', '#808080')

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
