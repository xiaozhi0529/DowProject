# -*- coding: utf-8 -*-
"""
数据模型定义文件
定义API请求和响应的数据结构
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class DownloadRequest(BaseModel):
    """
    视频下载请求模型
    定义客户端发送的下载请求数据结构
    """
    url: HttpUrl = Field(
        ...,  # 表示必填字段
        description="要下载的视频链接",
        example="https://www.douyin.com/video/123456789"
    )
    
    remove_watermark: bool = Field(
        default=False,  # 默认不去水印
        description="是否去除水印",
        example=True
    )
    
    quality: Optional[str] = Field(
        default="best",  # 默认最佳质量
        description="视频质量选择",
        example="best"
    )

class DownloadResponse(BaseModel):
    """
    视频下载响应模型
    定义服务器返回的下载结果数据结构
    """
    success: bool = Field(
        ...,  # 表示必填字段
        description="下载是否成功",
        example=True
    )
    
    message: str = Field(
        ...,  # 表示必填字段
        description="响应消息",
        example="下载成功"
    )
    
    video_url: Optional[str] = Field(
        default=None,
        description="下载后的视频URL",
        example="https://example.com/videos/video_123.mp4"
    )
    
    filename: Optional[str] = Field(
        default=None,
        description="视频文件名",
        example="video_123.mp4"
    )
    
    file_size: Optional[int] = Field(
        default=None,
        description="文件大小（字节）",
        example=1024000
    )
    
    duration: Optional[float] = Field(
        default=None,
        description="视频时长（秒）",
        example=30.5
    )
    
    thumbnail_url: Optional[str] = Field(
        default=None,
        description="视频缩略图URL",
        example="https://example.com/thumbnails/thumb_123.jpg"
    )
    
    platform: Optional[str] = Field(
        default=None,
        description="视频来源平台",
        example="抖音"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.now,  # 使用当前时间作为默认值
        description="创建时间"
    )

class ErrorResponse(BaseModel):
    """
    错误响应模型
    定义API错误响应的数据结构
    """
    success: bool = Field(
        default=False,
        description="操作是否成功"
    )
    
    message: str = Field(
        ...,  # 表示必填字段
        description="错误消息",
        example="下载失败：不支持的视频链接"
    )
    
    error_code: Optional[str] = Field(
        default=None,
        description="错误代码",
        example="INVALID_URL"
    )
    
    details: Optional[dict] = Field(
        default=None,
        description="错误详情",
        example={"url": "https://example.com/video", "reason": "链接无效"}
    )

class PlatformInfo(BaseModel):
    """
    平台信息模型
    定义支持的视频平台信息
    """
    name: str = Field(
        ...,  # 表示必填字段
        description="平台名称",
        example="抖音"
    )
    
    domain: str = Field(
        ...,  # 表示必填字段
        description="平台域名",
        example="douyin.com"
    )
    
    supported_features: list = Field(
        default=[],
        description="支持的功能列表",
        example=["下载", "去水印", "提取音频"]
    )
    
    max_duration: Optional[int] = Field(
        default=None,
        description="最大支持时长（秒）",
        example=300
    )

class HealthCheckResponse(BaseModel):
    """
    健康检查响应模型
    定义服务健康检查的响应数据结构
    """
    status: str = Field(
        ...,  # 表示必填字段
        description="服务状态",
        example="healthy"
    )
    
    service: str = Field(
        ...,  # 表示必填字段
        description="服务名称",
        example="video-downloader"
    )
    
    version: str = Field(
        ...,  # 表示必填字段
        description="服务版本",
        example="1.0.0"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,  # 使用当前时间作为默认值
        description="检查时间"
    )
    
    uptime: Optional[float] = Field(
        default=None,
        description="服务运行时间（秒）",
        example=3600.5
    ) 