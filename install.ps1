# PMCLI Windows Installer (PowerShell) - Robust & Automatic
$ErrorActionPreference = "Stop"

Write-Host "=========================================="
Write-Host "      Installation de PMCLI v2.0...       "
Write-Host "=========================================="

# 1. Verification de Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERREUR] Python n'a pas été trouvé. Veuillez l'installer." -ForegroundColor Red
    exit 1
}

# 2. Installation via pip
Write-Host "[1/3] Installation des fichiers..."
python -m pip install . --user --upgrade --quiet

# 3. Récupération du dossier Scripts (méthode plus fiable)
$userScripts = python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))"

# Vérification que le script est bien là
if (!(Test-Path (Join-Path $userScripts "pmcli.exe"))) {
    # Si non trouvé, on cherche dans le dossier parent (parfois nécessaire selon version Python)
    $parent = Split-Path $userScripts -Parent
    if (Test-Path (Join-Path $parent "Scripts\pmcli.exe")) {
        $userScripts = Join-Path $parent "Scripts"
    }
}



# 4. Vérification et mise à jour du PATH
Write-Host "[2/3] Configuration du PATH..."
$userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

if ($userPath -notlike "*$userScripts*") {
    Write-Host "      -> Ajout de $userScripts au PATH utilisateur..."
    $newPath = "$userPath;$userScripts"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    # Mise à jour de la session actuelle pour un test immédiat
    $env:PATH = "$env:PATH;$userScripts"
} else {
    Write-Host "      -> Le PATH est déjà configuré."
}

# 5. Vérification finale
Write-Host "[3/3] Vérification finale..."
if (Get-Command pmcli -ErrorAction SilentlyContinue) {
    Write-Host "`n[SUCCÈS] PMCLI est prêt à l'emploi !" -ForegroundColor Green
    Write-Host "🚀 Vous pouvez taper 'pmcli' dès maintenant." -ForegroundColor Yellow
} else {
    Write-Host "`n[NOTE] Installation réussie, mais vous devez REDÉMARRER votre terminal" -ForegroundColor Cyan
    Write-Host "       pour que la commande 'pmcli' soit reconnue partout." -ForegroundColor Cyan
}

Write-Host "`nPressez une touche pour quitter..."
# Simple wait instead of pause which might fail in some environments
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
