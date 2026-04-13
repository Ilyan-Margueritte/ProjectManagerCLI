"""Command to initialize a new project."""

import os
from pmcli.core.models import Project
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects, save_projects
from pmcli.output import formatter


def run(args: list[str]) -> int:
    name = args[0]
    
    # Create project folder
    if not os.path.exists(name):
        try:
            os.mkdir(name)
        except OSError as e:
            formatter.print_error(f"Impossible de créer le dossier '{name}': {e}")
            return 1
            
    projects = load_projects()
    
    if name in projects:
        formatter.print_warning(f"Le projet '{name}' existe déjà dans l'index.")
        return 1
        
    # Register project
    projects[name] = Project(name=name)
    save_projects(projects)
    
    formatter.print_success(f"Projet '{name}' initialisé avec succès 🚀")
    
    # Auto-initialize git
    formatter.print_info("Initialisation du dépôt Git...")
    if os.system(f"cd {name} && git init > /dev/null 2>&1") == 0:
        formatter.print_success("Dépôt Git initialisé automatiquement.")
    else:
        formatter.print_warning("Git n'a pas pu être initialisé.")
        
    return 0


REGISTRY.register(CommandDef(
    name="init",
    description="Initialise un nouveau projet et crée le dossier",
    usage="<nom_projet>",
    min_args=1,
    handler=run
))
