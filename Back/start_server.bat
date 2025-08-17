@echo off
chcp 65001 >nul
echo ========================================
echo           视频下载服务启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo Python已安装
echo.

REM 检查依赖包
echo 检查依赖包...
python -c "import fastapi, uvicorn, yt_dlp, pydantic" >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo 依赖包检查完成
echo.

REM 创建必要目录
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs
echo 目录创建完成
echo.

REM 启动服务器
echo 启动服务器...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务器
echo.

python start_server.py

pause 