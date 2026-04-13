# PMCLI 🚀 — Ultimate Project Manager

![PMCLI Banner](/home/ilyan/.gemini/antigravity/brain/6b8af278-7599-43d1-b12c-288ac9f91120/pmcli_banner_1776076746343.png)

**PMCLI** (Project Manager CLI) est un outil de productivité ultra-rapide conçu pour les développeurs qui vivent dans le terminal. Gérez vos projets, vos tâches et générez du code via l'IA en une seule ligne de commande.

---

## 🔥 Fonctionnalités Phares

- **⚡ Instant Init** : Créez des dossiers de projet et initialisez Git automatiquement.
- **🔌 Plugin System** : Architecture modulaire permettant d'ajouter des fonctionnalités via des extensions externes.
- **🤖 AI Scaffolding** : Générez des boilerplates complets (HTML/CSS/JS) en décrivant votre projet (via Ollama & Kimi).
- **📦 Global Storage** : Vos projets sont suivis globalement dans `~/.pmcli/`.
- **📊 Progress Tracking** : Visualisez l'avancement de vos tâches avec des barres de progression stylisées.

---

## 🛠️ Installation

### Via Pip (Recommandé)
```bash
pip install projectmcli
```

### Via l'installeur natif
```bash
git clone https://github.com/Ilyan-Margueritte/ProjectManagerCLI.git
cd ProjectManagerCLI
./install.sh
```

---

## 🔌 Gestion des Plugins

PMCLI est totalement extensible. Vous pouvez installer des plugins depuis un fichier local ou depuis le **Store Officiel**.

```bash
# Voir les plugins installés
pmcli plugin list

# Installer le générateur IA (depuis le repo)
pmcli plugin install ai_gen

# Supprimer une extension
pmcli plugin remove ai_gen
```

---

## 🤖 Utilisation de l'IA (Génération)

Une fois le plugin `ai_scaffolder` installé, décrivez simplement votre projet :

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
