# PMCLI 🚀 — Project Manager

**PMCLI** (Project Manager CLI) est un outil de productivité ultra-rapide conçu pour les développeurs qui vivent dans le terminal. Gérez vos projets, vos tâches et générez du code via l'IA en une seule ligne de commande.

---

## 🔥 Fonctionnalités Phares

- **⚡ Instant Init** : Créez des dossiers de projet et initialisez Git automatiquement.
- **🔌 Plugin System** : Architecture modulaire permettant d'ajouter des fonctionnalités via des extensions externes.
- **🤖 AI Scaffolding** : Générez des boilerplates complets (HTML/CSS/JS) en décrivant votre projet (via Ollama & Kimi).
- **📦 Global Storage** : Vos projets sont suivis globalement dans `~/.pmcli/`.
- **📊 Progress Tracking** : Visualisez l'avancement de vos tâches avec des barres de progression stylisées.
- **🛡️ Security Hardened** : Protections natives contre les injections de commandes et le Path Traversal (v1.6.0+).

---

## 🛡️ Sécurité & Robustesse

La version **1.1.1** apporte des améliorations majeures de sécurité :
- **Isolation des commandes** : Utilisation de `subprocess.run` pour empêcher les injections de scripts via les noms de projets.
- **Validation des chemins** : Protection contre le *Path Traversal* lors de la manipulation des plugins.
- **Gestion des erreurs** : Résistance aux entrées malformées (noms trop longs, octets nuls).

### Lancer les tests de sécurité (Fuzzing)
Pour vérifier la robustesse de votre installation :
```bash
# Installer les outils de test
pip install -e ".[test]"

# Lancer la batterie de tests Hypothesis
pytest tests/test_security_hypothesis.py
```

## 🛠️ Installation

### Via Pip (Recommandé)

```bash
# Clonez le repo
git clone https://github.com/Ilyan-Margueritte/ProjectManagerCLI.git
cd ProjectManagerCLI

# Installez
pip install .
```

> [!TIP]
> **Sur Windows** : Si la commande `pmcli` n'est pas reconnue après l'installation, lancez une fois `./install.ps1` pour configurer automatiquement votre PATH Windows.


### Via l'installeur natif

**Sur Linux / macOS :**
```bash
git clone https://github.com/Ilyan-Margueritte/ProjectManagerCLI.git
cd ProjectManagerCLI
./install.sh
```

**Sur Windows :**
1. Téléchargez le dossier ou clonez-le.
2. Ouvrez un terminal (PowerShell ou CMD) dans le dossier.
3. Exécutez :
   - PowerShell : `./install.ps1`
   - CMD : `setup.bat`
   - *Ou faites simplement un clic droit sur `install.ps1` > "Exécuter avec PowerShell" ou double-cliquez sur `setup.bat`.*


---

## 🔌 Gestion des Plugins

PMCLI est totalement extensible. Vous pouvez installer des plugins depuis un fichier local ou depuis le **Store Officiel**.

```bash
# Voir les plugins installés
pmcli plugin list

# Installer le générateur IA (depuis le repo)
pmcli plugin install extensions/ai_gen

# Supprimer une extension
pmcli plugin remove ai_gen
```

---

## 🤖 Utilisation de l'IA (Génération)

Une fois le plugin `ai-gen` installé, décrivez simplement votre projet :

```bash
pmcli generate mon_site_web
# ❓ Description : Une landing page sombre pour une agence de design
```
*PMCLI appellera votre instance locale Ollama pour coder le projet à votre place !*

---

## 📋 Commandes de base

| Commande | Usage | Description |
| :--- | :--- | :--- |
| `init` | `pmcli init <nom>` | Crée un nouveau projet et init Git. |
| `list` | `pmcli list` | Affiche tous vos projets et leur progression. |
| `add` | `pmcli add <projet> <tâche>` | Ajoute une tâche à faire. |
| `done` | `pmcli done <projet> <id>` | Marque une tâche comme terminée. |
| `open` | `pmcli open <projet>` | Ouvre le dossier dans votre explorateur. |

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à proposer vos propres plugins dans le dossier `extensions/`.

**Auteur** : [Ilyan Margueritte](https://github.com/Ilyan-Margueritte)  
**Licence** : MIT
