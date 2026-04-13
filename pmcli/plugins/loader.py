"""
Plugin System Loader for PMCLI.
Scans Internal and External directories for extensions.
"""

import os
import importlib.util
from pmcli.core.registry import REGISTRY
from pmcli.output import formatter
from pmcli.storage.json_store import GLOBAL_DIR

# 1. Path definitions
INTERNAL_PLUGINS_PATH = os.path.join(os.path.dirname(__file__), "internal")
EXTERNAL_PLUGINS_PATH = os.path.join(GLOBAL_DIR, "plugins")

def load_everything():
    """Charge automatiquement tout ce qui traîne dans les dossiers plugins."""
    _ensure_directories()
    # On charge d'abord les extensions internes, puis les externes du user
    _scan_path(INTERNAL_PLUGINS_PATH)
    _scan_path(EXTERNAL_PLUGINS_PATH)

def _ensure_directories():
    os.makedirs(INTERNAL_PLUGINS_PATH, exist_ok=True)
    os.makedirs(EXTERNAL_PLUGINS_PATH, exist_ok=True)

def _scan_path(path):
    if not os.path.exists(path): return
    for item in os.listdir(path):
        target = os.path.join(path, item)
        
        # Support Fichier .py ou Dossier avec main.py
        if item.endswith(".py"):
            _import_module(target, item[:-3])
        elif os.path.isdir(target):
            main_script = os.path.join(target, "main.py")
            if os.path.exists(main_script):
                _import_module(main_script, item)

def _import_module(filepath, name):
    try:
        spec = importlib.util.spec_from_file_location(f"ext_{name}", filepath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        formatter.print_error(f"Plugin '{name}' [Échec] : {e}")
