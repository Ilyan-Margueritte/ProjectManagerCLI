"""
Entry point for PMCLI.
Handles parsing arguments and dispatching to the configured commands.
"""

import sys
from pmcli.core.registry import REGISTRY
from pmcli.output import formatter

# Ensure all commands are imported so they register themselves
import pmcli.commands  # noqa


def print_help():
    print("\nPMCLI v2.0 — Project Manager CLI\n")
    print("USAGE:")
    print("  pmcli <commande> [arguments...]\n")
    print("COMMANDES:")
    
    commands = REGISTRY.all_commands()
    for cmd in commands:
        aliases = f" (alias: {', '.join(cmd.aliases)})" if cmd.aliases else ""
        print(f"  {cmd.name: <12} {cmd.usage: <25} {cmd.description}{aliases}")
    print()


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command_name = sys.argv[1]
    args = sys.argv[2:]

    if command_name in ("help", "--help", "-h"):
        print_help()
        sys.exit(0)

    cmd_def = REGISTRY.get(command_name)
    if not cmd_def:
        formatter.print_error(f"Commande inconnue : '{command_name}'")
        print("Tapez 'pmcli help' pour voir la liste des commandes.")
        sys.exit(1)

    code = REGISTRY.dispatch(command_name, args)
    
    if code == -2:
        formatter.print_error(f"Arguments manquants pour '{command_name}'")
        print(f"Usage : pmcli {command_name} {cmd_def.usage}")
        sys.exit(1)
    elif code == -1:
        formatter.print_error(f"Erreur interne de distribution pour '{command_name}'")
        sys.exit(1)
        
    sys.exit(code)

if __name__ == "__main__":
    main()
