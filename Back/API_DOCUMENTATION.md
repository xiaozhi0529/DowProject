# 视频下载服务 API 文档

## 概述

视频下载服务是一个基于 FastAPI 构建的 RESTful API 服务，提供视频下载和去水印功能。支持多个主流视频平台，包括抖音、快手、微博、B站、YouTube 等。

## 基础信息

- **服务地址**: `http://localhost:8000`
- **API 版本**: v1.0.0
- **文档地址**: 
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

## 支持的平台

- 抖音 (douyin.com)
- 快手 (kuaishou.com)
- 微博 (weibo.com)
- B站 (bilibili.com)
- YouTube (youtube.com)
- Instagram (instagram.com)
- TikTok (tiktok.com)
- 小红书 (xiaohongshu.com)
- 西瓜视频 (ixigua.com)

## API 接口

### 1. 服务健康检查

#### GET /

检查服务是否正常运行。

**请求示例:**
```bash
curl -X GET "http://localhost:8000/"
```

**响应示例:**
```json
{
  "message": "视频下载服务运行正常",
  "status": "running"
}
```

### 2. 健康检查

#### GET /health

详细的健康检查接口，用于监控服务状态。

**请求示例:**
```bash
curl -X GET "http://localhost:8000/health"
```

**响应示例:**
```json
{
  "status": "healthy",
  "service": "video-downloader"
}
```

### 3. 视频下载

#### POST /api/download

下载视频的主要接口，支持原视频下载和去水印下载。

**请求参数:**

| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| url | string | 是 | 视频链接 | "https://www.douyin.com/video/123456789" |
| remove_watermark | boolean | 否 | 是否去除水印，默认 false | true |
| quality | string | 否 | 视频质量，默认 "best" | "best" |

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.douyin.com/video/123456789",
    "remove_watermark": true,
    "quality": "best"
  }'
```

**响应示例 (成功):**
```json
{
  "success": true,
  "message": "下载成功",
  "video_url": "https://example.com/videos/video_123.mp4",
  "filename": "video_123.mp4",
  "file_size": 1024000,
  "duration": 30.5,
  "thumbnail_url": "https://example.com/thumbnails/thumb_123.jpg",
  "platform": "抖音",
  "created_at": "2023-12-01T10:30:00"
}
```

**响应示例 (失败):**
```json
{
  "detail": "下载失败: 不支持的视频链接"
}
```

**错误码说明:**

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查URL格式和参数 |
| 500 | 服务器内部错误 | 检查视频链接是否有效 |
| 422 | 数据验证失败 | 确保请求参数符合要求 |

### 4. 获取支持的平台

#### GET /api/supported_platforms

获取当前系统支持的所有视频平台列表。

**请求示例:**
```bash
curl -X GET "http://localhost:8000/api/supported_platforms"
```

**响应示例:**
```json
{
  "platforms": [
    "抖音",
    "快手", 
    "微博",
    "B站",
    "YouTube",
    "Instagram",
    "TikTok",
    "小红书",
    "西瓜视频"
  ]
}
```

## 数据模型

### DownloadRequest

下载请求数据模型。

```json
{
  "url": "string (required)",
  "remove_watermark": "boolean (optional, default: false)",
  "quality": "string (optional, default: 'best')"
}
```

### DownloadResponse

下载响应数据模型。

```json
{
  "success": "boolean (required)",
  "message": "string (required)",
  "video_url": "string (optional)",
  "filename": "string (optional)",
  "file_size": "integer (optional)",
  "duration": "number (optional)",
  "thumbnail_url": "string (optional)",
  "platform": "string (optional)",
  "created_at": "datetime (required)"
}
```

## 使用示例

### Python 客户端示例

```python
import requests
import json

# 服务地址
base_url = "http://localhost:8000"

# 下载视频
def download_video(url, remove_watermark=False):
    """
    下载视频函数
    
    参数:
    - url: 视频链接
    - remove_watermark: 是否去除水印
    
    返回:
    - 下载结果
    """
    endpoint = f"{base_url}/api/download"
    
    # 请求数据
    data = {
        "url": url,
        "remove_watermark": remove_watermark,
        "quality": "best"
    }
    
    try:
        # 发送POST请求
        response = requests.post(endpoint, json=data)
        response.raise_for_status()  # 检查HTTP错误
        
        # 返回响应数据
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 下载原视频
    result = download_video("https://www.douyin.com/video/123456789")
    if result and result.get("success"):
        print(f"下载成功: {result['filename']}")
    
    # 下载去水印视频
    result = download_video("https://www.douyin.com/video/123456789", remove_watermark=True)
    if result and result.get("success"):
        print(f"去水印下载成功: {result['filename']}")
```

### JavaScript 客户端示例

```javascript
// 服务地址
const baseUrl = 'http://localhost:8000';

// 下载视频函数
async function downloadVideo(url, removeWatermark = false) {
    /**
     * 下载视频函数
     * 
     * @param {string} url - 视频链接
     * @param {boolean} removeWatermark - 是否去除水印
     * @returns {Promise<Object>} 下载结果
     */
    const endpoint = `${baseUrl}/api/download`;
    
    // 请求数据
    const data = {
        url: url,
        remove_watermark: removeWatermark,
        quality: 'best'
    };
    
    try {
        // 发送POST请求
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        // 检查响应状态
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // 返回响应数据
        return await response.json();
        
    } catch (error) {
        console.error('请求失败:', error);
        return null;
    }
}

// 使用示例
async function main() {
    // 下载原视频
    const result = await downloadVideo('https://www.douyin.com/video/123456789');
    if (result && result.success) {
        console.log(`下载成功: ${result.filename}`);
    }
    
    // 下载去水印视频
    const result2 = await downloadVideo('https://www.douyin.com/video/123456789', true);
    if (result2 && result2.success) {
        console.log(`去水印下载成功: ${result2.filename}`);
    }
}

// 执行示例
main();
```

### cURL 示例

```bash
# 下载原视频
curl -X POST "http://localhost:8000/api/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.douyin.com/video/123456789",
    "remove_watermark": false
  }'

# 下载去水印视频
curl -X POST "http://localhost:8000/api/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.douyin.com/video/123456789",
    "remove_watermark": true
  }'

# 检查服务状态
curl -X GET "http://localhost:8000/health"

# 获取支持的平台
curl -X GET "http://localhost:8000/api/supported_platforms"
```

## 部署说明

### 环境要求

- Python 3.8+
- FFmpeg (用于视频处理)
- 足够的磁盘空间用于视频存储

### 安装步骤

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **安装 FFmpeg**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载 FFmpeg 并添加到系统 PATH
```

3. **启动服务**
```bash
python main.py
```

### 生产环境部署

1. **使用 Gunicorn**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. **使用 Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 注意事项

1. **法律合规**: 请确保遵守相关法律法规，仅下载您有权访问的内容
2. **版权保护**: 尊重原创作者的版权，不要用于商业用途
3. **服务限制**: 建议在生产环境中添加请求频率限制和用户认证
4. **存储管理**: 定期清理下载文件，避免磁盘空间不足
5. **网络环境**: 某些平台可能需要特定的网络环境才能正常访问

## 技术支持

如有问题或建议，请联系开发团队。

---

**版本**: 1.0.0  
**更新时间**: 2023-12-01  
**维护者**: Video Downloader Team 