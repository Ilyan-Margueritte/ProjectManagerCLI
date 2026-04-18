"""Basic Init command (Core). Just creates the project folder and registers it."""

import os
from pmcli.core.models import Project
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects, save_projects
from pmcli.output import formatter

def run(args: list[str]) -> int:
    if not args: return -2
    name = args[0]

    projects = load_projects()
    if name in projects:
        formatter.print_warning(f"Projet '{name}' existe déjà.")
        return 1

    if not os.path.exists(name):
        try:
            os.mkdir(name)
        except (OSError, ValueError) as e:
            formatter.print_error(f"Impossible de créer le dossier '{name}': {e}")
            return 1

    projects[name] = Project(name=name)
    save_projects(projects)
    
    formatter.print_success(f"Projet '{name}' initialisé (Base) 🚀")
    
    # Cross-platform git init
    import subprocess
    try:
        subprocess.run(["git", "init", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, ValueError):
        # ValueError peut arriver si le nom contient des null bytes (\0)
        pass
    return 0

REGISTRY.register(CommandDef(
    name="init",
    description="Initialise un nouveau projet (base)",
    usage="<nom_projet>",
    min_args=1,
    handler=run
))
