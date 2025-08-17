// app.js
// 视频下载小程序全局配置和逻辑

App({
  // 全局数据
  globalData: {
    // API配置
    apiBaseUrl: 'http://localhost:8000',  // 后端API地址
    
    // 用户信息
    userInfo: null,
    
    // 系统信息
    systemInfo: null,
    
    // 网络状态
    networkType: 'unknown',
    
    // 版本信息
    version: '1.0.0',
    
    // 配置信息
    config: {
      // 下载配置
      maxDownloadSize: 500 * 1024 * 1024,  // 最大下载文件大小（500MB）
      downloadTimeout: 60000,  // 下载超时时间（60秒）
      
      // 历史记录配置
      maxHistoryCount: 20,  // 最大历史记录数量
      
      // 缓存配置
      cacheExpireTime: 24 * 60 * 60 * 1000,  // 缓存过期时间（24小时）
    }
  },

  // 小程序初始化完成时触发
  onLaunch() {
    console.log('小程序启动')
    
    // 获取系统信息
    this.getSystemInfo()
    
    // 检查网络状态
    this.checkNetworkStatus()
    
    // 初始化用户信息
    this.initUserInfo()
    
    // 检查更新
    this.checkUpdate()
  },

  // 小程序显示时触发
  onShow() {
    console.log('小程序显示')
    
    // 重新检查网络状态
    this.checkNetworkStatus()
  },

  // 小程序隐藏时触发
  onHide() {
    console.log('小程序隐藏')
  },

  // 小程序错误时触发
  onError(msg) {
    console.error('小程序错误:', msg)
    
    // 可以在这里添加错误上报逻辑
    this.reportError(msg)
  },

  // 获取系统信息
  getSystemInfo() {
    try {
      const systemInfo = wx.getSystemInfoSync()
      this.globalData.systemInfo = systemInfo
      console.log('系统信息:', systemInfo)
    } catch (e) {
      console.error('获取系统信息失败:', e)
    }
  },

  // 检查网络状态
  checkNetworkStatus() {
    wx.getNetworkType({
      success: (res) => {
        this.globalData.networkType = res.networkType
        console.log('网络类型:', res.networkType)
        
        // 监听网络状态变化
        wx.onNetworkStatusChange((res) => {
          this.globalData.networkType = res.networkType
          console.log('网络状态变化:', res.networkType)
          
          // 网络断开时提示用户
          if (res.networkType === 'none') {
            wx.showToast({
              title: '网络连接已断开',
              icon: 'error',
              duration: 2000
            })
          }
        })
      },
      fail: (err) => {
        console.error('获取网络状态失败:', err)
      }
    })
  },

  // 初始化用户信息
  initUserInfo() {
    // 检查用户是否已授权
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.userInfo']) {
          // 已授权，获取用户信息
          wx.getUserInfo({
            success: (userInfo) => {
              this.globalData.userInfo = userInfo.userInfo
              console.log('用户信息:', userInfo.userInfo)
            }
          })
        }
      }
    })
  },

  // 检查更新
  checkUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      
      updateManager.onCheckForUpdate((res) => {
        console.log('检查更新结果:', res.hasUpdate)
      })
      
      updateManager.onUpdateReady(() => {
        wx.showModal({
          title: '更新提示',
          content: '新版本已经准备好，是否重启应用？',
          success: (res) => {
            if (res.confirm) {
              updateManager.applyUpdate()
            }
          }
        })
      })
      
      updateManager.onUpdateFailed(() => {
        wx.showToast({
          title: '更新失败',
          icon: 'error',
          duration: 2000
        })
      })
    }
  },

  // 错误上报
  reportError(error) {
    // 这里可以添加错误上报到服务器的逻辑
    console.error('错误上报:', error)
  },

  // 网络请求封装
  request(options) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          ...options.header
        },
        timeout: options.timeout || this.globalData.config.downloadTimeout,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${res.statusText}`))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },

  // 下载文件封装
  downloadFile(options) {
    return new Promise((resolve, reject) => {
      wx.downloadFile({
        url: options.url,
        header: options.header || {},
        timeout: options.timeout || this.globalData.config.downloadTimeout,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res)
          } else {
            reject(new Error(`下载失败: HTTP ${res.statusCode}`))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },

  // 显示提示信息
  showToast(message, type = 'info') {
    const iconMap = {
      success: 'success',
      error: 'error',
      info: 'none'
    }
    
    wx.showToast({
      title: message,
      icon: iconMap[type] || 'none',
      duration: 2000
    })
  },

  // 显示确认对话框
  showConfirm(title, content) {
    return new Promise((resolve) => {
      wx.showModal({
        title: title,
        content: content,
        success: (res) => {
          resolve(res.confirm)
        }
      })
    })
  },

  // 保存数据到本地存储
  setStorage(key, data) {
    try {
      wx.setStorageSync(key, data)
      return true
    } catch (e) {
      console.error('保存数据失败:', e)
      return false
    }
  },

  // 从本地存储获取数据
  getStorage(key) {
    try {
      return wx.getStorageSync(key)
    } catch (e) {
      console.error('获取数据失败:', e)
      return null
    }
  },

  // 删除本地存储数据
  removeStorage(key) {
    try {
      wx.removeStorageSync(key)
      return true
    } catch (e) {
      console.error('删除数据失败:', e)
      return false
    }
  },

  // 清空本地存储
  clearStorage() {
    try {
      wx.clearStorageSync()
      return true
    } catch (e) {
      console.error('清空存储失败:', e)
      return false
    }
  },

  // 格式化文件大小
  formatFileSize(bytes) {
    if (bytes === 0) return '0 B'
    
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  },

  // 格式化时间
  formatTime(date) {
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hour = date.getHours().toString().padStart(2, '0')
    const minute = date.getMinutes().toString().padStart(2, '0')
    
    return `${year}-${month}-${day} ${hour}:${minute}`
  },

  // 验证URL格式
  isValidUrl(url) {
    try {
      new URL(url)
      return true
    } catch (e) {
      return false
    }
  },

  // 获取平台名称
  getPlatformName(url) {
    const platformMap = {
      'douyin.com': '抖音',
      'kuaishou.com': '快手',
      'weibo.com': '微博',
      'bilibili.com': 'B站',
      'youtube.com': 'YouTube',
      'instagram.com': 'Instagram',
      'tiktok.com': 'TikTok',
      'xiaohongshu.com': '小红书',
      'ixigua.com': '西瓜视频'
    }
    
    try {
      const domain = new URL(url).hostname.toLowerCase()
      for (const [key, value] of Object.entries(platformMap)) {
        if (domain.includes(key)) {
          return value
        }
      }
      return '未知平台'
    } catch (e) {
      return '未知平台'
    }
  }
})
