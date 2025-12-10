@echo off
chcp 65001 >nul
REM Package tuxs to whl file

echo ========================================
echo Start building tuxs package
echo ========================================

REM Activate conda environment
call conda activate comfyui
if %errorlevel% neq 0 (
    echo Error: Cannot activate comfyui environment
    pause
    exit /b 1
)

echo.
echo Current environment:
call conda info --envs

echo.
echo ========================================
echo Step 1: Install build tools
echo ========================================
pip install --upgrade pip setuptools wheel build

echo.
echo ========================================
echo Step 2: Clean old build files
echo ========================================
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist tuxs.egg-info rmdir /s /q tuxs.egg-info

echo.
echo ========================================
echo Step 3: Build whl file
echo ========================================
python -m build

if %errorlevel% neq 0 (
    echo.
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed!
echo ========================================
echo.
echo whl file location: dist\tuxs-0.1.0-py3-none-any.whl
echo.
echo Install command:
echo   pip install dist\tuxs-0.1.0-py3-none-any.whl
echo.
echo Development mode install:
echo   pip install -e .
echo.

pause
