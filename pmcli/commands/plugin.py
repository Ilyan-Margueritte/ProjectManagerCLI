"""Dedicated command to manage plugins (Local & Remote)."""

import os
import shutil
import json
import urllib.request
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.output import formatter
from pmcli.storage.json_store import GLOBAL_DIR

# Dossier des plugins utilisateurs
USER_PLUGIN_DIR = os.path.join(GLOBAL_DIR, "plugins")

# URL du Registre Central (À remplacer par ton futur repo GitHub)
# Exemple imaginaire : https://raw.githubusercontent.com/Ilyan-Margueritte/PMCLI/main/registry.json
REMOTE_REGISTRY_URL = "https://raw.githubusercontent.com/Ilyan-Margueritte/ProjectManagerCLI/main/plugins/registry.json"

def run(args: list[str]) -> int:
    if not args: return -2
    subcmd = args[0]
    
    if subcmd == "list":
        return _list_plugins()
    elif subcmd == "install":
        if len(args) < 2:
            formatter.print_error("Usage: pmcli plugin install <nom_du_plugin>")
            return 1
        return _install_plugin(args[1])
    elif subcmd in ("remove", "rm"):
        if len(args) < 2:
            formatter.print_error("Usage: pmcli plugin remove <nom>")
            return 1
        return _remove_plugin(args[1])
    else:
        formatter.print_error(f"Sous-commande inconnue : {subcmd}")
        return 1

def _list_plugins():
    # ... (code local existant)
    formatter.print_info("Plugins installés :")
    if not os.path.exists(USER_PLUGIN_DIR):
        print("  (Aucun)")
    else:
        items = [i for i in os.listdir(USER_PLUGIN_DIR) if i != "__pycache__"]
        for item in items: print(f"  🔌 {item}")
    
    # On affiche une astuce pour voir le store
    print("\n💡 Tapez 'pmcli plugin install <nom>' pour télécharger une extension sur le Store.")
    return 0

def _install_plugin(name):
    # 1. Tester si c'est un chemin local direct
    if os.path.exists(name):
        return _perform_install(name)
        
    # 2. Sinon, essayer de le trouver sur le STORE (Remote)
    formatter.print_info(f"Recherche de '{name}' sur le store distant...")
    try:
        # On télécharge la liste des plugins
        with urllib.request.urlopen(REMOTE_REGISTRY_URL, timeout=5) as resp:
            registry = json.loads(resp.read().decode())
            
        if name in registry:
            download_url = registry[name]["url"]
            dest_file = os.path.join(USER_PLUGIN_DIR, f"{name}.py")
            
            formatter.print_info(f"Téléchargement de {name} depuis GitHub...")
            urllib.request.urlretrieve(download_url, dest_file)
            formatter.print_success(f"Plugin '{name}' installé via le Store ! 🌐")
            return 0
    except Exception as e:
        # Si le store est inaccessible ou plugin absent, on cherche en local pour ton test actuel
        local_potential = os.path.join(os.getcwd(), "extensions", name)
        if os.path.exists(local_potential):
            return _perform_install(local_potential)
            
    formatter.print_error(f"Impossible de trouver le plugin '{name}' (Local ou Store).")
    return 1

def _perform_install(src):
    name = os.path.basename(src)
    dest = os.path.join(USER_PLUGIN_DIR, name)
    try:
        os.makedirs(USER_PLUGIN_DIR, exist_ok=True)
        if os.path.isdir(src):
            if os.path.exists(dest): shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        formatter.print_success(f"Plugin '{name}' installé localement. 🎉")
        return 0
    except Exception as e:
        formatter.print_error(f"Erreur d'installation : {e}")
        return 1

def _remove_plugin(name):
    # ... (code de suppression existant)
    path = os.path.join(USER_PLUGIN_DIR, name)
    if not os.path.exists(path):
        if not name.endswith(".py"): path += ".py"
    if not os.path.exists(path):
        formatter.print_error(f"Plugin '{name}' introuvable.")
        return 1
    shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    formatter.print_success(f"Plugin '{name}' supprimé. 🗑️")
    return 0

REGISTRY.register(CommandDef(
    name="plugin",
    description="Gère les extensions (Store distant supporté)",
    usage="<list | install | remove> [nom]",
    min_args=1,
    handler=run
))
