#!/usr/bin/env bash
# PMCLI Native Installer

set -e

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}      Installation de PMCLI v2.0...       ${NC}"
echo -e "${BLUE}==========================================${NC}"

# Dossiers d'installation
INSTALL_DIR="$HOME/.pmcli-app"
BIN_DIR="$HOME/.local/bin"

# 1. Copier le code dans ~/.pmcli-app
echo -e "📦 Copie des fichiers vers ${INSTALL_DIR}..."
mkdir -p "$INSTALL_DIR"
cp -r ./* "$INSTALL_DIR/"

# 2. Rendre le script pmcli.py exécutable
chmod +x "$INSTALL_DIR/pmcli.py"

# 3. Créer le lien symbolique dans ~/.local/bin
echo -e "🔗 Création du lien symbolique dans ${BIN_DIR}..."
mkdir -p "$BIN_DIR"

if [ -L "$BIN_DIR/pmcli" ]; then
    rm "$BIN_DIR/pmcli"
fi

ln -s "$INSTALL_DIR/pmcli.py" "$BIN_DIR/pmcli"

echo -e "${GREEN}✅ Installation terminée avec succès !${NC}"

# 4. Vérifier si ~/.local/bin est dans le PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠️  ATTENTION : ${BIN_DIR} n'est pas dans votre \$PATH.${NC}"
    echo -e "Pour utiliser la commande 'pmcli' partout, ajoutez cette ligne à votre ~/.bashrc ou ~/.zshrc :"
    echo -e "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo -e "Puis rechargez votre terminal ou tapez : source ~/.bashrc"
else
    echo -e "🚀 Vous pouvez maintenant taper ${YELLOW}pmcli${NC} depuis n'importe quel dossier !"
fi
