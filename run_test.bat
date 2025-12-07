@echo off
REM Kimi Table to HTML 测试运行脚本（Windows批处理）
echo ======================================================================
echo Kimi Table to HTML 工具测试套件
echo ======================================================================
echo.

REM 激活 conda 环境
echo [INFO] 正在激活 conda 环境: comfyui
call conda activate comfyui
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] 无法激活 comfyui 环境，请确保已安装 conda 并创建了 comfyui 环境
    pause
    exit /b 1
)
echo [OK] 已激活 comfyui 环境
echo.

REM 检查是否设置了环境变量
if defined KIMI_API_KEY (
    echo [OK] 检测到 KIMI_API_KEY 环境变量
    echo.
) else (
    echo [INFO] 未设置 KIMI_API_KEY 环境变量，将跳过集成测试
    echo       如需运行集成测试，请先设置环境变量：
    echo       set KIMI_API_KEY=your_api_key_here
    echo.
)

echo 开始运行测试...
echo.

REM 运行测试
python test\test_kimi_table_to_html.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] 测试完成！
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo [FAILED] 测试失败，请检查上面的错误信息
    echo ======================================================================
)

pause
