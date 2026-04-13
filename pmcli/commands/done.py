"""Command to mark a task as done."""

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
    task = project.find_task(task_title)
    
    if not task:
        formatter.print_error(f"Tâche '{task_title}' introuvable dans '{name}' ❌")
        return 1
        
    if task.done:
        formatter.print_info(f"La tâche '{task.title}' est déjà terminée.")
        return 0
        
    task.done = True
    save_projects(projects)
    
    formatter.print_success(f"Tâche terminée : {task.title} ✅")
    return 0


REGISTRY.register(CommandDef(
    name="done",
    description="Marque une tâche comme terminée",
    usage="<nom_projet> <titre_tâche>",
    min_args=2,
    handler=run
))
