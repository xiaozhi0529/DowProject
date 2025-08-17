# -*- coding: utf-8 -*-
"""
视频下载服务主入口文件
提供视频下载和去水印功能的API接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.video_downloader import VideoDownloader
from app.models import DownloadRequest, DownloadResponse
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用实例
app = FastAPI(
    title="视频下载服务API",  # API文档标题
    description="提供视频下载和去水印功能的RESTful API接口",  # API描述
    version="1.0.0",  # API版本号
    docs_url="/docs",  # Swagger文档地址
    redoc_url="/redoc"  # ReDoc文档地址
)

# 配置CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境建议设置具体域名）
    allow_credentials=True,  # 允许携带认证信息
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 创建视频下载器实例
video_downloader = VideoDownloader()

@app.get("/")
async def root():
    """
    根路径接口 - 服务健康检查
    返回服务状态信息
    """
    return {"message": "视频下载服务运行正常", "status": "running"}

@app.get("/health")
async def health_check():
    """
    健康检查接口
    用于监控服务是否正常运行
    """
    return {"status": "healthy", "service": "video-downloader"}

@app.post("/api/download", response_model=DownloadResponse)
async def download_video(request: DownloadRequest):
    """
    视频下载接口
    
    参数:
    - request: 包含下载链接和选项的请求对象
    
    返回:
    - 下载结果信息，包括视频URL、文件名等
    """
    try:
        # 记录请求日志
        logger.info(f"收到下载请求: {request.url}")
        
        # 调用视频下载器处理请求
        result = await video_downloader.download_video(
            url=request.url,
            remove_watermark=request.remove_watermark
        )
        
        # 返回下载结果
        return DownloadResponse(
            success=True,
            message="下载成功",
            video_url=result.get("video_url"),
            filename=result.get("filename"),
            file_size=result.get("file_size"),
            duration=result.get("duration")
        )
        
    except Exception as e:
        # 记录错误日志
        logger.error(f"下载失败: {str(e)}")
        
        # 返回错误响应
        raise HTTPException(
            status_code=500,
            detail=f"下载失败: {str(e)}"
        )

@app.get("/api/supported_platforms")
async def get_supported_platforms():
    """
    获取支持的平台列表
    返回当前系统支持下载视频的平台信息
    """
    platforms = [
        "抖音", "快手", "微博", "B站", "YouTube", 
        "Instagram", "TikTok", "小红书", "西瓜视频"
    ]
    return {"platforms": platforms}

if __name__ == "__main__":
    # 启动服务器
    uvicorn.run(
        "main:app",  # 应用入口点
        host="0.0.0.0",  # 监听所有网络接口
        port=8000,  # 服务端口
        reload=True,  # 开发模式下自动重载
        log_level="info"  # 日志级别
    )
