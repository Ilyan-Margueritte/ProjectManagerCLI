"""Command to delete a project."""

import os
import shutil
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects, save_projects
from pmcli.output import formatter


def run(args: list[str]) -> int:
    name = args[0]
    
    projects = load_projects()
    
    if name not in projects:
        formatter.print_error(f"Projet '{name}' introuvable ❌")
        return 1
        
    del projects[name]
    save_projects(projects)
    
    # Also delete directory if it exists and we're in the right place
    if os.path.exists(name) and os.path.isdir(name):
        try:
            shutil.rmtree(name)
            formatter.print_success(f"Dossier '{name}' supprimé.")
        except OSError as e:
            formatter.print_error(f"Impossible de supprimer le dossier '{name}': {e}")
            
    formatter.print_success(f"Projet '{name}' supprimé de l'index 🗑️")
    return 0


REGISTRY.register(CommandDef(
    name="delete",
    description="Supprime un projet (et son dossier)",
    usage="<nom_projet>",
    min_args=1,
    handler=run,
    aliases=["remove", "rm"]
))
