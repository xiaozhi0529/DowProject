# 快速开始指南

## 🚀 5分钟快速部署

### 1. 环境准备

#### 安装Python 3.8+
```bash
# 检查Python版本
python --version

# 如果未安装，请从 https://python.org 下载安装
```

#### 安装FFmpeg
```bash
# Windows
# 下载FFmpeg并添加到系统PATH

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

### 2. 后端部署

#### 方法一：使用启动脚本（推荐）
```bash
# 进入后端目录
cd Back

# Windows用户
start_server.bat

# Linux/macOS用户
python start_server.py
```

#### 方法二：手动启动
```bash
# 进入后端目录
cd Back

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

#### 验证服务
- 服务地址：http://localhost:8000
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 3. 前端部署

#### 安装微信开发者工具
1. 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
2. 安装并登录

#### 导入项目
1. 打开微信开发者工具
2. 选择"导入项目"
3. 项目目录选择：`WebUi` 文件夹
4. AppID填写：测试号（如果没有小程序账号）

#### 配置API地址
编辑 `WebUi/pages/index/index.js`：
```javascript
data: {
  apiBaseUrl: 'http://localhost:8000'  // 修改为你的服务器地址
}
```

#### 编译运行
1. 点击"编译"按钮
2. 在模拟器中预览
3. 扫码在真机上测试

## 📱 使用说明

### 用户操作流程
1. **复制视频链接** - 从抖音、快手等平台复制分享链接
2. **粘贴到小程序** - 打开小程序，粘贴链接
3. **选择下载选项** - 选择是否去水印、视频质量
4. **开始下载** - 点击下载按钮
5. **保存到相册** - 下载完成后保存到手机相册

### 支持的平台
- ✅ 抖音
- ✅ 快手
- ✅ 微博
- ✅ B站
- ✅ YouTube
- ✅ Instagram
- ✅ TikTok
- ✅ 小红书
- ✅ 西瓜视频

## 🔧 常见问题

### 后端问题

#### Q: 启动时提示缺少依赖包
```bash
# 解决方案
cd Back
pip install -r requirements.txt
```

#### Q: FFmpeg未安装
```bash
# Windows: 下载FFmpeg并添加到PATH
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

#### Q: 端口被占用
```bash
# 修改端口
python start_server.py --port 8001
```

### 前端问题

#### Q: 网络请求失败
- 检查后端服务是否启动
- 确认API地址配置正确
- 检查防火墙设置

#### Q: 无法保存到相册
- 确保已授权相册权限
- 检查手机存储空间
- 重启小程序重试

#### Q: 下载失败
- 检查视频链接是否有效
- 确认网络连接正常
- 查看后端日志信息

## 📊 测试用例

### 测试视频链接
```
抖音: https://www.douyin.com/video/xxxxx
快手: https://www.kuaishou.com/short-video/xxxxx
微博: https://weibo.com/tv/show/xxxxx
B站: https://www.bilibili.com/video/xxxxx
```

### API测试
```bash
# 健康检查
curl http://localhost:8000/health

# 获取支持的平台
curl http://localhost:8000/api/supported_platforms

# 下载视频（示例）
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/video","remove_watermark":false}'
```

## 🔒 安全注意事项

### 生产环境部署
1. **修改默认配置**
   - 更改API密钥
   - 设置访问限制
   - 配置HTTPS

2. **添加认证机制**
   - 用户登录
   - API密钥验证
   - 请求频率限制

3. **监控和日志**
   - 启用详细日志
   - 监控服务器资源
   - 设置告警机制

### 法律合规
- 仅下载您有权访问的内容
- 遵守平台使用条款
- 尊重原创作者版权
- 不要用于商业用途

## 📞 技术支持

### 获取帮助
- 📖 查看完整文档：`README.md`
- 🔧 API文档：`Back/API_DOCUMENTATION.md`
- 🐛 提交Issue：GitHub Issues
- 💬 技术交流：GitHub Discussions

### 日志查看
```bash
# 后端日志
tail -f Back/logs/app.log

# 小程序日志
# 在微信开发者工具控制台查看
```

---

**快速开始完成！** 🎉

如果遇到问题，请查看完整文档或提交Issue获取帮助。 