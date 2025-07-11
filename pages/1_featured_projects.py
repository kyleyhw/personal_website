import streamlit as st
import requests
from utils import load_font

# Load the custom font
load_font()

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
        for repo in repos:
            st.markdown(f"#### [{repo.get('name', 'No name')}]({repo.get('url', '#')})")
            st.write(repo.get('description', 'No description provided.'))
            if repo.get('primaryLanguage'):
                st.write(f"**Language:** {repo['primaryLanguage']['name']}")
            st.write("---")
