#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频下载服务启动脚本
用于快速启动后端服务
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        logger.error("需要Python 3.8或更高版本")
        sys.exit(1)
    logger.info(f"Python版本: {sys.version}")

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'yt-dlp',
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少依赖包: {', '.join(missing_packages)}")
        logger.info("请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    logger.info("所有依赖包已安装")

def check_ffmpeg():
    """检查FFmpeg是否安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("FFmpeg已安装")
            return True
    except FileNotFoundError:
        pass
    
    logger.warning("FFmpeg未安装，某些功能可能无法正常工作")
    logger.info("请安装FFmpeg:")
    logger.info("  Ubuntu/Debian: sudo apt install ffmpeg")
    logger.info("  CentOS/RHEL: sudo yum install ffmpeg")
    logger.info("  macOS: brew install ffmpeg")
    logger.info("  Windows: 下载FFmpeg并添加到PATH")
    return False

def create_directories():
    """创建必要的目录"""
    directories = ['downloads', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"目录已创建: {directory}")

def start_server(host='0.0.0.0', port=8000, reload=True, workers=1):
    """启动服务器"""
    logger.info(f"启动服务器: {host}:{port}")
    
    # 构建启动命令
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'main:app',
        '--host', host,
        '--port', str(port),
        '--log-level', 'info'
    ]
    
    if reload:
        cmd.append('--reload')
    
    if workers > 1:
        cmd.extend(['--workers', str(workers)])
    
    try:
        # 启动服务器
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except subprocess.CalledProcessError as e:
        logger.error(f"启动服务器失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='视频下载服务启动脚本')
    parser.add_argument('--host', default='0.0.0.0', help='服务器地址')
    parser.add_argument('--port', type=int, default=8000, help='服务器端口')
    parser.add_argument('--no-reload', action='store_true', help='禁用自动重载')
    parser.add_argument('--workers', type=int, default=1, help='工作进程数')
    parser.add_argument('--check-only', action='store_true', help='仅检查环境')
    
    args = parser.parse_args()
    
    logger.info("=== 视频下载服务启动脚本 ===")
    
    # 检查环境
    check_python_version()
    check_dependencies()
    check_ffmpeg()
    create_directories()
    
    if args.check_only:
        logger.info("环境检查完成")
        return
    
    # 启动服务器
    start_server(
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
        workers=args.workers
    )

if __name__ == '__main__':
    main() 