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

:: Якщо шлях не вказано, використати шлях по замовчуванню
if "%USER_PATH%"=="" (
    set "FOOOCUS_MODELS_DIR=%DEFAULT_MODELS_DIR%"
) else (
    set "FOOOCUS_MODELS_DIR=%USER_PATH%"
)

:: Прибрати лапки
set "FOOOCUS_MODELS_DIR=%FOOOCUS_MODELS_DIR:"=%"

:: Замінити прямий слеш на обернений
set "FOOOCUS_MODELS_DIR=%FOOOCUS_MODELS_DIR:/=\%"

:: Додати обернений слеш вкінці, якщо відсутній
if not "%FOOOCUS_MODELS_DIR:~-1%"=="\" set "FOOOCUS_MODELS_DIR=%FOOOCUS_MODELS_DIR%\"

echo.

:: Зупинити контейнер, якщо запущений
echo [1/3] Stopping previous container (if running)...
docker rm -f fooocus_container 2>nul

echo [3/3] Starting new container
docker run -it --rm --name fooocus_container --gpus=all ^
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility ^
  -e NVIDIA_VISIBLE_DEVICES=all ^
  -v "%FOOOCUS_MODELS_DIR%:/app/repositories/Fooocus/models" ^
  -p 8888:8888 konieshadow/fooocus-api
