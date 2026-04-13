"""Command to print PMCLI version."""

from pmcli.core.registry import REGISTRY, CommandDef
from pmcli import __version__


def run(args: list[str]) -> int:
    print(f"PMCLI v{__version__}")
    return 0


REGISTRY.register(CommandDef(
    name="version",
    description="Affiche la version de PMCLI",
    usage="",
    min_args=0,
    handler=run,
    aliases=["-v", "--version"]
))
