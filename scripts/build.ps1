# Build script for Excel Sheet Unlocker
$ErrorActionPreference = "Stop"

# Directories
$buildDir = "build"
$distDir = "dist"
$installerOutputDir = "installer_output"

Write-Host "--- Starting Build Process ---" -ForegroundColor Cyan

# 1. Cleanup
Write-Host "Cleaning old build artifacts..." -ForegroundColor Gray
if (Test-Path $buildDir) { Remove-Item -Recurse -Force $buildDir }
if (Test-Path $distDir) { Remove-Item -Recurse -Force $distDir }
if (Test-Path $installerOutputDir) { Remove-Item -Recurse -Force $installerOutputDir }

# 2. Install Dependencies
Write-Host "Installing dependencies..." -ForegroundColor Gray
pip install -r requirements.txt

# Run PyInstaller
Write-Host "Generating standalone executable..." -ForegroundColor Gray
pyinstaller --noconfirm installer\excel_unlocker_gui.spec
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

# Run Inno Setup Compiler
Write-Host "Generating installer with Inno Setup..." -ForegroundColor Gray
# iscc is in PATH as per user requirements
iscc installer\excel_unlocker.iss
if ($LASTEXITCODE -ne 0) {
    Write-Host "Inno Setup Compiler failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`n--- Build Complete! ---" -ForegroundColor Green
Write-Host "Installer location: $installerOutputDir\ExcelSheetUnlocker_Setup.exe" -ForegroundColor Yellow
