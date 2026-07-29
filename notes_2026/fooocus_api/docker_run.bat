@echo off
title Fooocus API Docker Launcher
setlocal enabledelayedexpansion

:: Налаштування дефолтного шляху на основі поточної папки скрипта
set "DEFAULT_MODELS_DIR=%~dp0repositories\Fooocus\models"

echo --------------------------------------------------
echo Enter the path to the Fooocus models directory.
echo Or just press ENTER to use the default path:
echo [%DEFAULT_MODELS_DIR%]
echo --------------------------------------------------
set /p "USER_PATH=Enter path: "

:: If empty, use the pre-calculated default path
if "%USER_PATH%"=="" (
    set "FOOOCUS_MODELS_DIR=%DEFAULT_MODELS_DIR%"
) else (
    set "FOOOCUS_MODELS_DIR=%USER_PATH%"
)

:: Strip any quotes entered by the user
set "FOOOCUS_MODELS_DIR=%FOOOCUS_MODELS_DIR:"=%"

:: Replace forward slashes (/) with backward slashes (\)
set "FOOOCUS_MODELS_DIR=%FOOOCUS_MODELS_DIR:/=\%"

:: Check if the path ends with a backslash; if not, add one
if not "%FOOOCUS_MODELS_DIR:~-1%"=="\" set "FOOOCUS_MODELS_DIR=%FOOOCUS_MODELS_DIR%\"

echo.
echo [1/3] Stopping previous container (if running)...
docker rm -f fooocus_container 2>nul

echo [3/3] Starting new container
docker run -it --rm --name fooocus_container --gpus=all ^
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility ^
  -e NVIDIA_VISIBLE_DEVICES=all ^
  -v "%FOOOCUS_MODELS_DIR%:/app/repositories/Fooocus/models" ^
  -p 8888:8888 konieshadow/fooocus-api
