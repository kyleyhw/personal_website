# Kyle Wong - Personal Website

A personal portfolio website built with [Streamlit](https://streamlit.io/), showcasing my research in astrophysics, CV, and software projects.

## Project Structure

```
c:\Users\Kyle\PycharmProjects\personal_website\
├── assets/                  # Static assets (images, etc.)
├── pages/                   # Streamlit sub-pages
│   ├── 1_featured_projects.py
│   ├── 2_research_experience.py
│   └── 3_presentations.py
├── .streamlit/              # Streamlit configuration
├── main.py                  # Entry point for the application
├── utils.py                 # Utility functions (font loading)
├── pyproject.toml           # Project dependencies (managed by uv)
└── README.md                # This file
```

## Setup & Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for fast package management.

### 1. Install uv
If you haven't already, install `uv`:
```bash
# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies
Sync the project dependencies:
```bash
uv sync
```

## Running the Website

To launch the website locally:

```bash
uv run streamlit run main.py
```

This will automatically open the site in your default web browser (usually at `http://localhost:8501`).

## Features
*   **Dynamic Project Fetching**: The "Featured Projects" page scrapes your pinned repositories from GitHub automatically.
*   **Profile Integration**: Loads profile picture locally from `assets/`.
*   **CV Integration**: Displays research experience, education, and skills matching your latest CV.
