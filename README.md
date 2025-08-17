# 视频下载助手

一个支持多平台视频下载和去水印的微信小程序，配合Python FastAPI后端服务。

## 项目结构

```
DowProject/
├── Back/                    # Python后端服务
│   ├── app/                # 应用模块
│   │   ├── __init__.py     # 包初始化文件
│   │   ├── models.py       # 数据模型定义
│   │   └── video_downloader.py  # 视频下载器核心
│   ├── main.py             # 主入口文件
│   ├── requirements.txt    # Python依赖包
│   └── API_DOCUMENTATION.md # API接口文档
├── WebUi/                  # 微信小程序前端
│   ├── pages/             # 页面文件
│   │   └── index/         # 主页面
│   │       ├── index.wxml # 页面模板
│   │       ├── index.wxss # 页面样式
│   │       ├── index.js   # 页面逻辑
│   │       └── index.json # 页面配置
│   ├── app.js             # 小程序入口文件
│   ├── app.json           # 小程序配置文件
│   ├── app.wxss           # 全局样式文件
│   └── project.config.json # 项目配置文件
└── README.md              # 项目说明文档
```

## 功能特性

### 后端功能 (Python FastAPI)
- ✅ 支持多平台视频下载（抖音、快手、微博、B站、YouTube等）
- ✅ 视频去水印功能
- ✅ 多种视频质量选择
- ✅ RESTful API接口
- ✅ 自动生成API文档
- ✅ 错误处理和日志记录
- ✅ CORS跨域支持

### 前端功能 (微信小程序)
- ✅ 现代化UI设计
- ✅ 视频链接输入和验证
- ✅ 下载选项配置（去水印、质量选择）
- ✅ 下载历史记录
- ✅ 保存到相册功能
- ✅ 网络状态检测
- ✅ 错误提示和用户反馈

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

## 技术栈

### 后端
- **Python 3.8+**
- **FastAPI** - 现代、快速的Web框架
- **uvicorn** - ASGI服务器
- **yt-dlp** - 强大的视频下载工具
- **FFmpeg** - 视频处理工具
- **Pydantic** - 数据验证

### 前端
- **微信小程序** - 移动端应用框架
- **WXML/WXSS** - 模板和样式
- **JavaScript** - 逻辑处理

## 安装和部署

### 后端部署

1. **安装Python依赖**
```bash
cd Back
pip install -r requirements.txt
```

2. **安装FFmpeg**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载FFmpeg并添加到系统PATH
```

3. **启动服务**
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

### 前端部署

1. **安装微信开发者工具**
从 [微信开发者工具官网](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 下载并安装

2. **导入项目**
- 打开微信开发者工具
- 选择"导入项目"
- 选择 `WebUi` 文件夹
- 填写小程序AppID（如果没有可以选择"测试号"）

3. **配置API地址**
在 `WebUi/pages/index/index.js` 中修改 `apiBaseUrl` 为你的后端服务地址

4. **编译和预览**
- 点击"编译"按钮
- 在模拟器中预览效果
- 可以扫码在真机上测试

## API接口

### 主要接口

1. **健康检查**
   - `GET /` - 服务状态检查
   - `GET /health` - 详细健康检查

2. **视频下载**
   - `POST /api/download` - 下载视频
   - `GET /api/supported_platforms` - 获取支持的平台

### 详细文档
查看 `Back/API_DOCUMENTATION.md` 获取完整的API文档

## 使用说明

### 用户使用流程

1. **复制视频链接**
   - 从支持的平台复制视频分享链接

2. **粘贴到小程序**
   - 打开小程序
   - 将链接粘贴到输入框

3. **选择下载选项**
   - 选择是否去除水印
   - 选择视频质量

4. **开始下载**
   - 点击"开始下载"或"去水印下载"
   - 等待下载完成

5. **保存到相册**
   - 下载完成后选择保存到相册
   - 授权相册权限

### 开发者配置

1. **修改API地址**
```javascript
// 在 WebUi/pages/index/index.js 中
data: {
  apiBaseUrl: 'http://your-server-ip:8000'
}
```

2. **配置网络请求域名**
在微信小程序后台配置合法域名：
- 添加你的后端服务域名到"request合法域名"
- 添加视频文件域名到"downloadFile合法域名"

## 注意事项

### 法律合规
- 请确保遵守相关法律法规
- 仅下载您有权访问的内容
- 尊重原创作者的版权
- 不要用于商业用途

### 技术限制
- 某些平台可能有反爬虫机制
- 网络环境可能影响下载速度
- 大文件下载可能需要较长时间
- 建议在生产环境中添加用户认证和频率限制

### 性能优化
- 定期清理下载文件
- 监控服务器资源使用
- 考虑使用CDN加速
- 添加缓存机制

## 开发计划

### 已实现功能
- ✅ 基础视频下载功能
- ✅ 去水印功能
- ✅ 多平台支持
- ✅ 微信小程序界面
- ✅ API文档

### 计划功能
- 🔄 批量下载功能
- 🔄 下载进度显示
- 🔄 用户登录系统
- 🔄 下载统计和分析
- 🔄 更多平台支持
- 🔄 视频格式转换
- 🔄 音频提取功能

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发环境设置
1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

### 代码规范
- 遵循PEP 8 Python代码规范
- 使用有意义的变量和函数名
- 添加适当的注释
- 编写单元测试

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件到项目维护者

---

**版本**: 1.0.0  
**更新时间**: 2023-12-01  
**维护者**: Video Downloader Team 