"""Command to list tasks for a project."""

from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects
from pmcli.output import formatter


def run(args: list[str]) -> int:
    name = args[0]
    projects = load_projects()
    
    if name not in projects:
        formatter.print_error(f"Projet '{name}' introuvable ❌")
        return 1
        
    formatter.print_task_list(projects[name])
    return 0


REGISTRY.register(CommandDef(
    name="tasks",
    description="Liste les tâches d'un projet",
    usage="<nom_projet>",
    min_args=1,
    handler=run
))
