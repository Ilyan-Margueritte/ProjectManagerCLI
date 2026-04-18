import os
import shutil
import tempfile
import pytest
from contextlib import contextmanager
from hypothesis import given, strategies as st
from pmcli.commands import init, plugin
from pmcli.storage import json_store

@contextmanager
def clean_env_context():
    """Gestionnaire de contexte pour un environnement de test isolé."""
    # Sauvegarde de l'état actuel
    old_home = os.environ.get("HOME")
    old_cwd = os.getcwd()
    temp_dir = tempfile.mkdtemp()
    
    # Isolation de l'environnement
    os.environ["HOME"] = temp_dir
    work_dir = os.path.join(temp_dir, "workspace")
    os.makedirs(work_dir)
    os.chdir(work_dir)
    
    # Réinitialisation forcée des chemins dans json_store pour le test
    old_global_dir = json_store.GLOBAL_DIR
    old_global_file = json_store.GLOBAL_PROJECTS_FILE
    json_store.GLOBAL_DIR = os.path.join(temp_dir, ".pmcli")
    json_store.GLOBAL_PROJECTS_FILE = os.path.join(json_store.GLOBAL_DIR, "projects.json")
    
    try:
        yield work_dir, temp_dir
    finally:
        # Restauration de l'état
        os.chdir(old_cwd)
        if old_home:
            os.environ["HOME"] = old_home
        json_store.GLOBAL_DIR = old_global_dir
        json_store.GLOBAL_PROJECTS_FILE = old_global_file
        
        # Nettoyage
        try:
            shutil.rmtree(temp_dir)
        except OSError:
            pass

@given(name=st.text(min_size=1, alphabet=st.characters(blacklist_categories=('Cs',), blacklist_characters='/\\:;*?"<>|')))
def test_init_safety(name):
    """Vérifie que la création de projet est sûre pour des noms valides."""
    with clean_env_context() as (work_dir, temp_dir):
        res = init.run([name])
        
        # Si le projet est créé, il doit l'être dans le workspace
        project_path = os.path.join(work_dir, name)
        if res == 0:
            assert os.path.exists(project_path)
            assert os.path.isdir(project_path)

@given(name=st.text(min_size=1))
def test_path_traversal_protection(name):
    """
    Test de propriété pour détecter des injections de chemin (Path Traversal).
    On vérifie qu'aucun fichier n'est créé en dehors de l'arborescence autorisée.
    """
    with clean_env_context() as (work_dir, temp_dir):
        try:
            # On tente d'initialiser avec un nom potentiellement malveillant
            init.run([name])
        except Exception:
            pass
        
        # Vérification : aucun fichier ne doit avoir été créé en dehors de temp_dir
        for root, dirs, files in os.walk(temp_dir):
            rel = os.path.relpath(root, temp_dir)
            if rel == ".": continue
            if rel == ".pmcli" or rel.startswith(".pmcli/"): continue
            if rel == "workspace" or rel.startswith("workspace/"): continue
            
            # Si on arrive ici, un dossier a été créé ailleurs !
            pytest.fail(f"ALERTE SÉCURITÉ : Tentative de Path Traversal détectée. Dossier créé : {rel}")

@given(plugin_name=st.text(min_size=1))
def test_plugin_remove_security(plugin_name):
    """
    Vérifie que la suppression de plugin ne peut pas supprimer de fichiers système.
    """
    with clean_env_context() as (work_dir, temp_dir):
        # On simule un fichier "sensible" dans le home temporaire
        secret_file = os.path.join(temp_dir, "sensitive_data.txt")
        with open(secret_file, "w") as f:
            f.write("top secret")
            
        try:
            # Tentative de suppression via le plugin manager
            plugin.run(["remove", plugin_name])
        except Exception:
            pass
            
        # Le fichier secret doit toujours exister
        assert os.path.exists(secret_file), f"ALERTE SÉCURITÉ : Le fichier {secret_file} a été supprimé lors du retrait du plugin {plugin_name}"

if __name__ == "__main__":
    pytest.main([__file__])
