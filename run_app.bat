@echo off
REM Launches the Hullstone app.
REM Checks for missing packages, installs them if needed, then opens the app.
REM Usage: keep it in the same folder as hullstone_app.py and double-click it.

setlocal EnableDelayedExpansion
REM Inside if-blocks, paths use delayed expansion (exclamation marks, not percent
REM signs) so a folder name with parentheses, e.g. "hullstone-main (1)", works.
title Hullstone
cd /d "%~dp0"

set "APP=hullstone_app.py"
set "VENV=.venv"
set "PACKAGES=streamlit plotly scipy numpy pandas"
set "PY=%VENV%\Scripts\python.exe"

if not exist "%APP%" (
    echo ERROR: %APP% not found in this folder: !CD!
    goto :fail
)

REM --- Create the virtual environment if it doesn't exist ---
if exist "%PY%" goto :check

call :findpython
if not defined PYBASE (
    echo Python not found. Installing it with winget...
    where winget >nul 2>&1
    if errorlevel 1 (
        echo ERROR: winget is not available. Install Python from https://www.python.org/downloads/
        echo and tick "Add python.exe to PATH" during setup, then run this file again.
        goto :fail
    )
    winget install -e --id Python.Python.3.12 --scope user --accept-package-agreements --accept-source-agreements
    if exist "!LocalAppData!\Programs\Python\Python312\python.exe" set "PYBASE=!LocalAppData!\Programs\Python\Python312\python.exe"
)
if not defined PYBASE (
    echo ERROR: Python was installed but could not be found. Close this window and run this file again.
    goto :fail
)

echo ^>^> First run: creating the virtual environment...
"%PYBASE%" -m venv "%VENV%"
if not exist "%PY%" (
    if exist "%VENV%" rmdir /s /q "%VENV%"
    echo ERROR: Could not create the virtual environment.
    goto :fail
)

:check
REM --- Find missing packages ---
set "MISSING="
for %%p in (%PACKAGES%) do (
    "%PY%" -c "import %%p" >nul 2>&1
    if errorlevel 1 (
        echo    [missing] %%p
        set "MISSING=!MISSING! %%p"
    ) else (
        echo    [ok]      %%p
    )
)

if defined MISSING (
    echo ^>^> Installing:!MISSING!  - this can take a few minutes the first time
    "%PY%" -m pip install --upgrade pip -q
    "%PY%" -m pip install!MISSING!
    if errorlevel 1 (
        echo ERROR: Package installation failed. Check your internet connection.
        goto :fail
    )
)

echo.
echo ^>^> Starting the app, it will open in your browser automatically.
echo ^>^> Close this window to stop it.
"%PY%" -m streamlit run "%APP%" --browser.gatherUsageStats false
echo.
pause
exit /b 0

:findpython
REM Try the py launcher first, then python on PATH. The Microsoft Store stub returns nothing and is skipped.
set "PYBASE="
for /f "delims=" %%i in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do set "PYBASE=%%i"
if defined PYBASE exit /b 0
for /f "delims=" %%i in ('python -c "import sys;print(sys.executable)" 2^>nul') do set "PYBASE=%%i"
exit /b 0

:fail
echo.
pause
exit /b 1
