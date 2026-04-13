"""
Main entry point for PMCLI.
Handles plugin loading and command dispatching.
"""

import sys
from pmcli.core.registry import REGISTRY
from pmcli.output import formatter
from pmcli.plugins import loader

# Ensure all core commands are registered
import pmcli.commands  # noqa

def print_help():
    loader.load_everything()  # Load all extensions
    
    print("\n🚀 PMCLI v2.0 - Project Manager Ultimate\n")
    print("USAGE:")
    print("  pmcli <commande> [arguments...]\n")
    
    print("COMMANDES DISPONIBLES :")
    commands = REGISTRY.all_commands()
    for cmd in sorted(commands, key=lambda x: x.name):
        alias_str = f" (alias: {', '.join(cmd.aliases)})" if cmd.aliases else ""
        print(f"  {cmd.name:<12} {cmd.description}{alias_str}")
        
    print("\nASTUCE: Tapez 'pmcli <commande> --help' pour voir l'usage.")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command_name = sys.argv[1].lower()
    args = sys.argv[2:]

    if command_name in ("help", "--help", "-h"):
        print_help()
        sys.exit(0)

    # Chargement dynamique des plugins pour voir si la commande existe dedans
    loader.load_everything()
    
    cmd_def = REGISTRY.get(command_name)
    if not cmd_def:
        formatter.print_error(f"Commande inconnue : '{command_name}'")
        print("Tapez 'pmcli help' pour voir la liste des commandes.")
        sys.exit(1)

    code = REGISTRY.dispatch(command_name, args)
    
    if code == -2: # Missing arguments based on Registry convention
        formatter.print_error(f"Arguments manquants pour '{command_name}'")
        print(f"Usage : pmcli {command_name} {cmd_def.usage}")
        sys.exit(1)
        
    sys.exit(code)

if __name__ == "__main__":
    main()
