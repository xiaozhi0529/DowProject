# -*- coding: utf-8 -*-
"""
视频下载器核心模块
使用yt-dlp库实现视频下载和去水印功能
"""

import yt_dlp
import os
import re
import asyncio
import aiohttp
import logging
from typing import Dict, Optional, Any
from urllib.parse import urlparse
import time
import hashlib

# 配置日志记录
logger = logging.getLogger(__name__)

class VideoDownloader:
    """
    视频下载器类
    负责处理各种平台的视频下载和去水印功能
    """
    
    def __init__(self):
        """
        初始化视频下载器
        设置下载目录和配置参数
        """
        # 设置下载目录
        self.download_dir = "downloads"  # 下载文件存储目录
        
        # 确保下载目录存在
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)  # 创建下载目录
            
        # 支持的平台配置
        self.supported_platforms = {
            "douyin.com": "抖音",
            "kuaishou.com": "快手", 
            "weibo.com": "微博",
            "bilibili.com": "B站",
            "youtube.com": "YouTube",
            "instagram.com": "Instagram",
            "tiktok.com": "TikTok",
            "xiaohongshu.com": "小红书",
            "ixigua.com": "西瓜视频"
        }
        
        # yt-dlp配置选项
        self.ydl_opts = {
            'format': 'best',  # 下载最佳质量
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),  # 输出模板
            'quiet': True,  # 静默模式
            'no_warnings': True,  # 不显示警告
            'extract_flat': False,  # 不提取平面信息
            'write_thumbnail': True,  # 下载缩略图
            'writethumbnail': True,  # 写入缩略图
            'writeinfojson': True,  # 写入信息JSON
            'writesubtitles': False,  # 不下载字幕
            'writeautomaticsub': False,  # 不下载自动字幕
            'ignoreerrors': False,  # 不忽略错误
            'no_color': True,  # 无颜色输出
            'geo_bypass': True,  # 绕过地理限制
            'geo_bypass_country': 'CN',  # 设置国家代码
            'geo_bypass_ip_block': True,  # 绕过IP封锁
        }
        
        logger.info("视频下载器初始化完成")
    
    def _detect_platform(self, url: str) -> Optional[str]:
        """
        检测视频链接所属平台
        
        参数:
        - url: 视频链接
        
        返回:
        - 平台名称，如果不支持则返回None
        """
        try:
            # 解析URL获取域名
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()  # 转换为小写
            
            # 移除www前缀
            if domain.startswith('www.'):
                domain = domain[4:]
                
            # 检查是否在支持的平台列表中
            for platform_domain, platform_name in self.supported_platforms.items():
                if platform_domain in domain:
                    logger.info(f"检测到平台: {platform_name}")
                    return platform_name
                    
            logger.warning(f"不支持的平台: {domain}")
            return None
            
        except Exception as e:
            logger.error(f"平台检测失败: {str(e)}")
            return None
    
    def _generate_filename(self, url: str, title: str = None) -> str:
        """
        生成唯一的文件名
        
        参数:
        - url: 视频链接
        - title: 视频标题
        
        返回:
        - 唯一的文件名
        """
        try:
            # 使用URL和时间戳生成唯一标识
            timestamp = str(int(time.time()))  # 当前时间戳
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]  # URL的MD5哈希前8位
            
            # 清理标题中的非法字符
            if title:
                # 移除或替换文件名中的非法字符
                title = re.sub(r'[<>:"/\\|?*]', '_', title)  # 替换非法字符为下划线
                title = re.sub(r'\s+', '_', title)  # 替换空格为下划线
                filename = f"{title}_{url_hash}_{timestamp}"
            else:
                filename = f"video_{url_hash}_{timestamp}"
                
            return filename
            
        except Exception as e:
            logger.error(f"文件名生成失败: {str(e)}")
            # 返回默认文件名
            return f"video_{int(time.time())}"
    
    async def _download_with_ytdlp(self, url: str, remove_watermark: bool = False) -> Dict[str, Any]:
        """
        使用yt-dlp下载视频
        
        参数:
        - url: 视频链接
        - remove_watermark: 是否去除水印
        
        返回:
        - 包含下载信息的字典
        """
        try:
            # 创建临时配置
            temp_opts = self.ydl_opts.copy()
            
            # 如果要去水印，添加相关配置
            if remove_watermark:
                temp_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',  # 使用FFmpeg转换
                    'preferedformat': 'mp4',  # 转换为MP4格式
                }]
                
            # 创建yt-dlp下载器实例
            with yt_dlp.YoutubeDL(temp_opts) as ydl:
                # 提取视频信息
                logger.info(f"开始提取视频信息: {url}")
                info = ydl.extract_info(url, download=False)  # 先不下载，只提取信息
                
                # 生成文件名
                filename = self._generate_filename(url, info.get('title'))
                temp_opts['outtmpl'] = os.path.join(self.download_dir, f"{filename}.%(ext)s")
                
                # 重新创建下载器并下载
                with yt_dlp.YoutubeDL(temp_opts) as ydl_download:
                    logger.info(f"开始下载视频: {url}")
                    ydl_download.download([url])
                
                # 构建返回结果
                result = {
                    'video_url': url,  # 原始URL
                    'filename': f"{filename}.{info.get('ext', 'mp4')}",
                    'title': info.get('title', '未知标题'),
                    'duration': info.get('duration'),
                    'thumbnail_url': info.get('thumbnail'),
                    'platform': self._detect_platform(url),
                    'file_size': info.get('filesize'),
                    'format': info.get('format'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'comment_count': info.get('comment_count'),
                    'description': info.get('description'),
                    'tags': info.get('tags', []),
                    'categories': info.get('categories', []),
                    'language': info.get('language'),
                    'age_limit': info.get('age_limit'),
                    'is_live': info.get('is_live', False),
                    'was_live': info.get('was_live', False),
                    'live_status': info.get('live_status'),
                    'availability': info.get('availability'),
                    'webpage_url': info.get('webpage_url'),
                    'webpage_url_basename': info.get('webpage_url_basename'),
                    'webpage_url_domain': info.get('webpage_url_domain'),
                    'extractor': info.get('extractor'),
                    'extractor_key': info.get('extractor_key'),
                    'epoch': info.get('epoch'),
                    'timestamp': info.get('timestamp'),
                    'release_timestamp': info.get('release_timestamp'),
                    'release_date': info.get('release_date'),
                    'release_year': info.get('release_year'),
                    'modified_timestamp': info.get('modified_timestamp'),
                    'modified_date': info.get('modified_date'),
                    'uploader_id': info.get('uploader_id'),
                    'uploader_url': info.get('uploader_url'),
                    'channel': info.get('channel'),
                    'channel_id': info.get('channel_id'),
                    'channel_url': info.get('channel_url'),
                    'channel_follower_count': info.get('channel_follower_count'),
                    'location': info.get('location'),
                    'subtitles': info.get('subtitles'),
                    'automatic_captions': info.get('automatic_captions'),
                    'chapters': info.get('chapters'),
                    'thumbnails': info.get('thumbnails'),
                    'audio_streams': info.get('audio_streams'),
                    'video_streams': info.get('video_streams'),
                    'formats': info.get('formats'),
                    'requested_formats': info.get('requested_formats'),
                    'format_id': info.get('format_id'),
                    'ext': info.get('ext'),
                    'resolution': info.get('resolution'),
                    'aspect_ratio': info.get('aspect_ratio'),
                    'fps': info.get('fps'),
                    'vcodec': info.get('vcodec'),
                    'acodec': info.get('acodec'),
                    'container': info.get('container'),
                    'filesize_approx': info.get('filesize_approx'),
                    'tbr': info.get('tbr'),
                    'vbr': info.get('vbr'),
                    'abr': info.get('abr'),
                    'asr': info.get('asr'),
                    'height': info.get('height'),
                    'width': info.get('width'),
                    'protocol': info.get('protocol'),
                    'source_preference': info.get('source_preference'),
                    'quality': info.get('quality'),
                    'has_drm': info.get('has_drm'),
                    'filesize': info.get('filesize'),
                    'downloader_options': info.get('downloader_options'),
                    'http_headers': info.get('http_headers'),
                    'url': info.get('url'),
                    'manifest_url': info.get('manifest_url'),
                    'manifest_stream_number': info.get('manifest_stream_number'),
                    'fragment_base_url': info.get('fragment_base_url'),
                    'fragment_index': info.get('fragment_index'),
                    'fragment_count': info.get('fragment_count'),
                    'lazy': info.get('lazy'),
                    'is_from_start': info.get('is_from_start'),
                    'direct': info.get('direct'),
                    'preference': info.get('preference'),
                    'language_preference': info.get('language_preference'),
                    'quality_preference': info.get('quality_preference'),
                    'source_preference': info.get('source_preference'),
                    'protocol_preference': info.get('protocol_preference'),
                    'geo_preference': info.get('geo_preference'),
                    'has_drm_preference': info.get('has_drm_preference'),
                    'filesize_preference': info.get('filesize_preference'),
                    'tbr_preference': info.get('tbr_preference'),
                    'vbr_preference': info.get('vbr_preference'),
                    'abr_preference': info.get('abr_preference'),
                    'asr_preference': info.get('asr_preference'),
                    'height_preference': info.get('height_preference'),
                    'width_preference': info.get('width_preference'),
                    'fps_preference': info.get('fps_preference'),
                    'vcodec_preference': info.get('vcodec_preference'),
                    'acodec_preference': info.get('acodec_preference'),
                    'container_preference': info.get('container_preference'),
                    'ext_preference': info.get('ext_preference'),
                    'resolution_preference': info.get('resolution_preference'),
                    'aspect_ratio_preference': info.get('aspect_ratio_preference'),
                    'protocol_preference': info.get('protocol_preference'),
                    'source_preference': info.get('source_preference'),
                    'has_drm_preference': info.get('has_drm_preference'),
                    'filesize_preference': info.get('filesize_preference'),
                    'tbr_preference': info.get('tbr_preference'),
                    'vbr_preference': info.get('vbr_preference'),
                    'abr_preference': info.get('abr_preference'),
                    'asr_preference': info.get('asr_preference'),
                    'height_preference': info.get('height_preference'),
                    'width_preference': info.get('width_preference'),
                    'fps_preference': info.get('fps_preference'),
                    'vcodec_preference': info.get('vcodec_preference'),
                    'acodec_preference': info.get('acodec_preference'),
                    'container_preference': info.get('container_preference'),
                    'ext_preference': info.get('ext_preference'),
                    'resolution_preference': info.get('resolution_preference'),
                    'aspect_ratio_preference': info.get('aspect_ratio_preference'),
                }
                
                logger.info(f"视频下载完成: {result['filename']}")
                return result
                
        except Exception as e:
            logger.error(f"yt-dlp下载失败: {str(e)}")
            raise Exception(f"视频下载失败: {str(e)}")
    
    async def download_video(self, url: str, remove_watermark: bool = False) -> Dict[str, Any]:
        """
        下载视频的主方法
        
        参数:
        - url: 视频链接
        - remove_watermark: 是否去除水印
        
        返回:
        - 包含下载信息的字典
        """
        try:
            # 验证URL格式
            if not url or not url.startswith(('http://', 'https://')):
                raise ValueError("无效的视频链接")
            
            # 检测平台支持
            platform = self._detect_platform(url)
            if not platform:
                raise ValueError("不支持的视频平台")
            
            logger.info(f"开始处理视频下载请求: {url}")
            
            # 使用yt-dlp下载视频
            result = await self._download_with_ytdlp(url, remove_watermark)
            
            # 添加处理标记
            result['processed'] = True
            result['remove_watermark'] = remove_watermark
            
            logger.info(f"视频处理完成: {result['filename']}")
            return result
            
        except Exception as e:
            logger.error(f"视频下载处理失败: {str(e)}")
            raise Exception(f"视频下载失败: {str(e)}")
    
    def get_supported_platforms(self) -> Dict[str, str]:
        """
        获取支持的平台列表
        
        返回:
        - 平台域名到平台名称的映射字典
        """
        return self.supported_platforms.copy()
    
    def cleanup_downloads(self, max_age_hours: int = 24):
        """
        清理过期的下载文件
        
        参数:
        - max_age_hours: 文件最大保留时间（小时）
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600  # 转换为秒
            
            # 遍历下载目录
            for filename in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, filename)
                
                # 检查文件修改时间
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    
                    # 如果文件超过最大保留时间，删除它
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        logger.info(f"删除过期文件: {filename}")
                        
        except Exception as e:
            logger.error(f"清理下载文件失败: {str(e)}") 