import requests
from bs4 import BeautifulSoup

username = "kyleyhw"
url = f"https://github.com/{username}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Fetching {url}...")
    # Try without headers first (to replicate current state)
    response = requests.get(url)
    print(f"Without Headers Status: {response.status_code}")
    
    # Try with headers
    response_headers = requests.get(url, headers=headers)
    print(f"With Headers Status: {response_headers.status_code}")

    soup = BeautifulSoup(response_headers.text, "html.parser")
    pinned_items = soup.find_all("div", class_="pinned-item-list-item-content")
    print(f"Found {len(pinned_items)} pinned items with headers.")

except Exception as e:
    print(f"Error: {e}")
