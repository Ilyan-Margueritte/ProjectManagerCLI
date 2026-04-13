"""Command to add a task to a project."""

from pmcli.core.models import Task
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects, save_projects
from pmcli.output import formatter


def run(args: list[str]) -> int:
    name = args[0]
    task_title = args[1]
    
    projects = load_projects()
    
    if name not in projects:
        formatter.print_error(f"Projet '{name}' introuvable ❌")
        return 1
        
    project = projects[name]
    
    if project.find_task(task_title):
        formatter.print_warning(f"La tâche '{task_title}' existe déjà.")
        return 1
        
    project.tasks.append(Task(title=task_title))
    save_projects(projects)
    
    formatter.print_success(f"Tâche '{task_title}' ajoutée à '{name}'")
    return 0


REGISTRY.register(CommandDef(
    name="add-task",
    description="Ajoute une tâche à un projet",
    usage="<nom_projet> <titre_tâche>",
    min_args=2,
    handler=run,
    aliases=["add"]
))
