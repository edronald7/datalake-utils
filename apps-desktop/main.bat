:: validate if "python" or "py" command is available
@echo off
setlocal
set "PYTHON_CMD="
:: Check if python command is available
where python >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
) else (
    :: Check if py command is available
    where py >nul 2>&1
    if %errorlevel%==0 (
        set "PYTHON_CMD=py"
    ) else (
        echo Python is not installed or not found in PATH.
        exit /b 1
    )
)

if "%PYTHON_CMD%"=="" (
    echo Python is not installed or not found in PATH.
    exit /b 1
) else (
    echo Using Python command: %PYTHON_CMD%
)

:: comprobar si la libreria Qt está instalada
if not exist "%PYTHON_CMD% -c \"import PyQt5\"" (
    echo PyQt5 is not installed. Please install it using pip.
    exit /b 1
)

:: comprobar si la libreria pandas, pyarrow, pyyaml, openpyxl está instalada
if not exist "%PYTHON_CMD% -c \"import pandas\"" (
    echo pandas is not installed. Please install it using pip.
    exit /b 1
)
if not exist "%PYTHON_CMD% -c \"import pyarrow\"" (
    echo pyarrow is not installed. Please install it using pip.
    exit /b 1
)
if not exist "%PYTHON_CMD% -c \"import yaml\"" (
    echo pyyaml is not installed. Please install it using pip.
    exit /b 1
)
if not exist "%PYTHON_CMD% -c \"import openpyxl\"" (
    echo openpyxl is not installed. Please install it using pip.
    exit /b 1
)

:: ejecutar escript python
set "SCRIPT_NAME=main.py"

echo Running %SCRIPT_NAME%...
"%PYTHON_CMD%" "%SCRIPT_NAME%" %*
if %errorlevel% neq 0 (
    echo Failed to run %SCRIPT_NAME%.
    exit /b %errorlevel%
)
echo %SCRIPT_NAME% finished successfully.
exit /b 0
:: End of script