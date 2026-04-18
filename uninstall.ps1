# PMCLI Windows Uninstaller
$ErrorActionPreference = "SilentlyContinue"

Write-Host "============================" -ForegroundColor Yellow
Write-Host "   Désinstallation de PMCLI  " -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

# 1. Désinstallation via pip
Write-Host "[1/2] Suppression du package via pip..."
python -m pip uninstall projectmcli -y

# 2. Suppression des données (Optionnel)
$choice = Read-Host "Souhaitez-vous aussi supprimer vos données (projets suivis et plugins) ? (O/N)"
if ($choice -eq "O" -or $choice -eq "o") {
    $dataDir = Join-Path $HOME ".pmcli"
    if (Test-Path $dataDir) {
        Remove-Item -Path $dataDir -Recurse -Force
        Write-Host "[2/2] Dossier de données supprimé (~/.pmcli)." -ForegroundColor Cyan
    }
} else {
    Write-Host "[2/2] Données conservées."
}

Write-Host "`n✅ Désinstallation terminée !" -ForegroundColor Green
pause
