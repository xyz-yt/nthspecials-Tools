@echo off
:: Batch script to disable UAC prompts
:: Requires administrator privileges

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script must be run as administrator!
    pause
    exit /b
)

echo Disabling UAC prompts...
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v "EnableLUA" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f

echo UAC has been disabled. A system restart is required for changes to take effect.
echo.
pause