"""
PMCLI AI Scaffolder Plugin.
Enhanced with Retry matching 503 errors and advanced JSON parsing.
"""

import os
import json
import re
import ollama
import time
from pmcli.core.registry import REGISTRY, CommandDef
from pmcli.core.models import Project
from pmcli.storage.json_store import load_projects, save_projects
from pmcli.output import formatter

MODEL_NAME = "kimi-k2.5:cloud"

def generate_handler(args: list[str]) -> int:
    if not args: return 1
    name = args[0]
    prompt_desc = input(" 🤖 Description : ")
    
    # Tentatives automatiques (Retry)
    for attempt in range(3):
        try:
            formatter.print_info(f"Appel de l'IA (Essai {attempt+1}/3)...")
            
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[
                    {'role': 'system', 'content': "Output ONLY a JSON object with keys 'index.html', 'style.css', 'script.js'. No markdown."},
                    {'role': 'user', 'content': f"Project '{name}': {prompt_desc}"}
                ]
            )
            
            raw_content = response['message']['content'].strip()
            
            # Parsing plus robuste
            json_match = re.search(r"(\{.*\})", raw_content, re.DOTALL)
            if json_match:
                files = json.loads(json_match.group(1))
                _create_project(name, files)
                return 0
            else:
                raise ValueError("L'IA n'a pas renvoyé de format JSON valide.")
                
        except Exception as e:
            if "503" in str(e):
                formatter.print_warning(f"Le serveur est surchargé (503). Retente dans 5s...")
                time.sleep(5)
                continue
            else:
                formatter.print_error(f"Erreur fatale : {e}")
                return 1

    formatter.print_error("Échec après 3 tentatives. Réessayez plus tard !")
    return 1

def _create_project(name, files):
    if not os.path.exists(name): os.mkdir(name)
    for filename, content in files.items():
        with open(os.path.join(name, filename), "w", encoding="utf-8") as f:
            f.write(content)
            
    projects = load_projects()
    projects[name] = Project(name=name)
    save_projects(projects)
    formatter.print_success(f"Projet '{name}' généré avec succès ! ✨")
    os.system(f"cd {name} && git init > /dev/null 2>&1")

REGISTRY.register(CommandDef(
    name="generate",
    description="Génère un projet complet via l'IA Ollama (avec retries)",
    usage="<nom_projet>",
    min_args=1,
    handler=generate_handler
))
