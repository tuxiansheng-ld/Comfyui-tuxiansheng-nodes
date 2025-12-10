@echo off
chcp 65001 >nul
REM Install tuxs package

echo ========================================
echo Install tuxs package
echo ========================================

REM Activate conda environment
call conda activate comfyui
if %errorlevel% neq 0 (
    echo Error: Cannot activate comfyui environment
    pause
    exit /b 1
)

echo.
echo Select installation method:
echo 1. Install from whl file
echo 2. Development mode (recommended for development)
echo 3. Install from source
echo.

set /p choice=Enter option (1/2/3): 

if "%choice%"=="1" goto install_whl
if "%choice%"=="2" goto install_dev
if "%choice%"=="3" goto install_source

echo Invalid option
pause
exit /b 1

:install_whl
echo.
echo ========================================
echo Install from whl file
echo ========================================
if not exist dist\tuxs-0.1.0-py3-none-any.whl (
    echo Error: whl file not found, please run build_package.bat first
    pause
    exit /b 1
)
pip install dist\tuxs-0.1.0-py3-none-any.whl
goto end

:install_dev
echo.
echo ========================================
echo Development mode installation
echo ========================================
echo Development mode creates symlinks, code changes take effect immediately
pip install -e .
goto end

:install_source
echo.
echo ========================================
echo Install from source
echo ========================================
pip install .
goto end

:end
if %errorlevel% neq 0 (
    echo.
    echo Error: Installation failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
echo Test installation:
python -c "import tuxs; print('tuxs version:', tuxs.__version__); print('Available modules:', tuxs.__all__)"
echo.

pause
