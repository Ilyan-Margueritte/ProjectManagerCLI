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
        os.mkdir(name)

    projects[name] = Project(name=name)
    save_projects(projects)
    
    formatter.print_success(f"Projet '{name}' initialisé (Base) 🚀")
    os.system(f"cd {name} && git init > /dev/null 2>&1")
    return 0

REGISTRY.register(CommandDef(
    name="init",
    description="Initialise un nouveau projet (base)",
    usage="<nom_projet>",
    min_args=1,
    handler=run
))
