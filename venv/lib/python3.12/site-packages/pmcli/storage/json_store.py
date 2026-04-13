"""
JSON storage layer for PMCLI.
Handles reading and writing the projects JSON file.
Automatically migrates legacy data on load.
"""

import os
import json
from pmcli.core.models import Project

# Use ~/.pmcli/projects.json as the standard location,
# but fallback to current directory if not configured and existing.
OLD_PROJECTS_FILE = "pmcli_projects.json"
GLOBAL_DIR = os.path.expanduser("~/.pmcli")
GLOBAL_PROJECTS_FILE = os.path.join(GLOBAL_DIR, "projects.json")

def get_projects_file() -> str:
    """Determine which file to use. Prefers global, falls back to local if existing."""
    if os.path.exists(GLOBAL_PROJECTS_FILE):
        return GLOBAL_PROJECTS_FILE
    if os.path.exists(OLD_PROJECTS_FILE):
        return OLD_PROJECTS_FILE
    
    # If neither exists, establish the global one
    if not os.path.exists(GLOBAL_DIR):
        os.makedirs(GLOBAL_DIR, exist_ok=True)
    return GLOBAL_PROJECTS_FILE

def load_projects() -> dict[str, Project]:
    """Loads all projects from the JSON store. Returns dict keyed by project name."""
    file_path = get_projects_file()
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {}

    projects = {}
    for name, p_data in data.items():
        if "name" not in p_data:
            p_data["name"] = name  # fix old schema missing name
        projects[name] = Project.from_dict(p_data)
        
    return projects

def save_projects(projects: dict[str, Project]) -> None:
    """Saves a dict of Projects to the JSON store."""
    file_path = get_projects_file()
    
    # Ensure directory exists if it's the global one
    if file_path == GLOBAL_PROJECTS_FILE and not os.path.exists(GLOBAL_DIR):
        os.makedirs(GLOBAL_DIR, exist_ok=True)
        
    data = {name: proj.to_dict() for name, proj in projects.items()}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
