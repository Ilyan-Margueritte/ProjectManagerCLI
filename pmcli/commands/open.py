"""Command to open a project directory."""

import os
import sys
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.output import formatter


def run(args: list[str]) -> int:
    name = args[0]
    
    if os.path.exists(name) and os.path.isdir(name):
        absolute_path = os.path.abspath(name)
        if os.name == 'nt':  # Windows
            os.startfile(absolute_path)
        elif sys.platform == 'darwin':  # macOS
            os.system(f'open "{absolute_path}"')
        else:  # Linux/Unix
            os.system(f'xdg-open "{absolute_path}" 2>/dev/null &')
        
        formatter.print_success(f"Dossier '{name}' ouvert 📂")
        return 0
    else:
        formatter.print_error(f"Dossier '{name}' introuvable dans le répertoire courant ❌")
        return 1


REGISTRY.register(CommandDef(
    name="open",
    description="Ouvre le dossier du projet dans l'explorateur de fichiers",
    usage="<nom_projet>",
    min_args=1,
    handler=run
))
