@echo off
chcp 65001 >nul
title 文档批量转 Markdown
cd /d "%~dp0"

REM 检查项目虚拟环境是否存在
if not exist ".venv\Scripts\streamlit.exe" (
    echo 找不到项目虚拟环境，请先安装 requirements.txt 中的依赖。
    pause
    exit /b 1
)

REM 如果服务已经运行，直接打开浏览器，避免端口冲突
curl.exe -s -f --max-time 2 http://localhost:8501/_stcore/health >nul 2>&1
if not errorlevel 1 (
    echo 文档转换工具已经运行，正在打开浏览器...
    start "" "http://localhost:8501"
    exit /b 0
)

echo 正在启动文档批量转 Markdown 工具...

REM 使用无交互模式启动，避免第一次运行询问邮箱
start "" /b ".venv\Scripts\streamlit.exe" run src\main\app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false

REM 最多等待 15 秒，服务就绪后自动打开浏览器
for /l %%i in (1,1,15) do (
    curl.exe -s -f --max-time 1 http://localhost:8501/_stcore/health >nul 2>&1
    if not errorlevel 1 goto ready
    timeout /t 1 /nobreak >nul
)

echo 工具启动失败，请检查依赖或 8501 端口是否被占用。
pause
exit /b 1

:ready
start "" "http://localhost:8501"
echo 工具已启动，浏览器地址：http://localhost:8501
echo 关闭本窗口或按 Ctrl+C 可以停止工具。
pause