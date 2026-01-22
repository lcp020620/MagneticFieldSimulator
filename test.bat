@echo off
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Set-Location '%~dp0'; .\run.ps1}"
pause
