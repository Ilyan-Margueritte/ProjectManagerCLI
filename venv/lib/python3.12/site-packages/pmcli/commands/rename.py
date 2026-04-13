"""Command to rename a project."""

import os
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects, save_projects
from pmcli.output import formatter


def run(args: list[str]) -> int:
    old_name = args[0]
    new_name = args[1]
    
    projects = load_projects()
    
    if old_name not in projects:
        formatter.print_error(f"Projet '{old_name}' introuvable ❌")
        return 1
        
    if new_name in projects:
        formatter.print_error(f"Un projet nommé '{new_name}' existe déjà ❌")
        return 1
        
    # Rename directory if it exists
    if os.path.exists(old_name) and os.path.isdir(old_name):
        try:
            os.rename(old_name, new_name)
        except OSError as e:
            formatter.print_error(f"Impossible de renommer le dossier '{old_name}': {e}")
            return 1
            
    # Update data
    project = projects.pop(old_name)
    project.name = new_name
    projects[new_name] = project
    save_projects(projects)
    
    formatter.print_success(f"Projet renommé de '{old_name}' à '{new_name}' 🔄")
    return 0


REGISTRY.register(CommandDef(
    name="rename",
    description="Renomme un projet (et son dossier)",
    usage="<ancien_nom> <nouveau_nom>",
    min_args=2,
    handler=run,
    aliases=["mv"]
))
