"""Command to list all projects."""

from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.storage.json_store import load_projects
from pmcli.output import formatter


def run(args: list[str]) -> int:
    projects = load_projects()
    formatter.print_project_list(projects)
    return 0


REGISTRY.register(CommandDef(
    name="list",
    description="Liste tous les projets",
    usage="",
    min_args=0,
    handler=run,
    aliases=["ls"]
))
