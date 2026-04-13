"""
Output formatters to ensure a consistent, friendly CLI experience.
"""

from pmcli.core.models import Project, Task

def print_success(msg: str) -> None:
    print(f"✅  {msg}")

def print_error(msg: str) -> None:
    print(f"❌  {msg}")

def print_warning(msg: str) -> None:
    print(f"⚠️  {msg}")

def print_info(msg: str) -> None:
    print(f"ℹ️  {msg}")

def _progress_bar(done: int, total: int, length: int = 10) -> str:
    """Returns a visual progress bar e.g. [██████░░░░]"""
    if total == 0:
        return f"[{'░' * length}] 0%"
    
    ratio = done / total
    filled = int(round(ratio * length))
    empty = length - filled
    percent = int(ratio * 100)
    
    return f"[{'█' * filled}{'░' * empty}] {percent}%"

def print_project_item(project: Project) -> None:
    """Print a single project entry for list."""
    stats = project.task_summary()
    total = len(project.tasks)
    done = sum(1 for t in project.tasks if t.done)
    
    bar = _progress_bar(done, total)
    print(f" 📦 {project.name: <15} | Status: {project.status: <8} | Tasks: {stats: <5} | {bar}")

def print_project_list(projects: dict[str, Project]) -> None:
    if not projects:
        print("Aucun projet 📭")
        return
        
    print("Liste des projets :")
    print("─" * 45)
    for name, project in projects.items():
        print_project_item(project)
    print("─" * 45)

def print_task_list(project: Project) -> None:
    if not project.tasks:
        print_info(f"Aucune tâche pour '{project.name}'")
        return
        
    print(f"Tâches pour '{project.name}' :")
    print("─" * 45)
    for task in project.tasks:
        icon = "✅" if task.done else "⬜"
        print(f" {icon} {task.title}")
    print("─" * 45)

def print_status_panel(project: Project) -> None:
    print("\n" + "═" * 40)
    print(f" 📊 PROJET : {project.name.upper()}")
    print("═" * 40)
    print(f" Status   : {project.status}")
    print(f" Création : {project.created_at}")
    print(f" Tâches   : {project.task_summary()}")
    print("─" * 40)
    if project.tasks:
        for task in project.tasks:
            icon = "✅" if task.done else "⬜"
            print(f"   {icon} {task.title}")
    else:
        print("   (aucune tâche)")
    print("═" * 40 + "\n")
