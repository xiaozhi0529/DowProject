// 视频下载小程序主页面逻辑
// 包含视频链接输入、下载处理、历史记录等功能

// 获取应用实例
const app = getApp()

// 页面数据
Page({
  // 页面的初始数据
  data: {
    // 视频链接输入
    videoUrl: '',  // 用户输入的视频链接
    
    // 下载选项
    removeWatermark: false,  // 是否去除水印
    qualityOptions: ['最佳质量', '高清', '标清'],  // 质量选项
    qualityIndex: 0,  // 当前选择的质量索引
    
    // 下载状态
    isDownloading: false,  // 是否正在下载
    
    // 支持的平台列表
    supportedPlatforms: [
      '抖音', '快手', '微博', 'B站', 'YouTube', 
      'Instagram', 'TikTok', '小红书', '西瓜视频'
    ],
    
    // 下载历史记录
    downloadHistory: [],
    
    // 结果弹窗
    showResultModal: false,  // 是否显示结果弹窗
    resultModal: {
      title: '',  // 弹窗标题
      message: '',  // 弹窗消息
      success: false  // 是否成功
    },
    
    // API配置
    apiBaseUrl: 'http://localhost:8000',  // 后端API地址
    currentDownloadResult: null  // 当前下载结果
  },

  // 生命周期函数--监听页面加载
  onLoad: function (options) {
    console.log('页面加载完成')
    
    // 从本地存储加载下载历史
    this.loadDownloadHistory()
    
    // 检查网络状态
    this.checkNetworkStatus()
    
    // 获取支持的平台信息
    this.getSupportedPlatforms()
  },

  // 生命周期函数--监听页面显示
  onShow: function () {
    console.log('页面显示')
  },

  // 生命周期函数--监听页面隐藏
  onHide: function () {
    console.log('页面隐藏')
  },

  // 生命周期函数--监听页面卸载
  onUnload: function () {
    console.log('页面卸载')
  },

  // 页面相关事件处理函数--监听用户下拉动作
  onPullDownRefresh: function () {
    console.log('用户下拉刷新')
    
    // 刷新页面数据
    this.refreshPageData()
    
    // 停止下拉刷新
    wx.stopPullDownRefresh()
  },

  // 页面上拉触底事件的处理函数
  onReachBottom: function () {
    console.log('页面上拉触底')
  },

  // 用户点击右上角分享
  onShareAppMessage: function () {
    return {
      title: '视频下载助手 - 支持抖音、快手、微博等平台',
      path: '/pages/index/index',
      imageUrl: '/images/share.png'
    }
  },

  // 输入事件处理
  onUrlInput: function (e) {
    // 处理视频链接输入
    const value = e.detail.value
    console.log('输入视频链接:', value)
    
    this.setData({
      videoUrl: value
    })
  },

  // 去水印选项切换
  onWatermarkChange: function (e) {
    // 处理去水印选项变化
    const value = e.detail.value
    console.log('去水印选项:', value)
    
    this.setData({
      removeWatermark: value
    })
  },

  // 质量选择变化
  onQualityChange: function (e) {
    // 处理视频质量选择变化
    const value = e.detail.value
    console.log('质量选择:', value)
    
    this.setData({
      qualityIndex: value
    })
  },

  // 开始下载视频
  downloadVideo: function () {
    // 下载原视频（不去水印）
    this.startDownload(false)
  },

  // 去水印下载
  downloadWithoutWatermark: function () {
    // 下载去水印视频
    this.startDownload(true)
  },

  // 开始下载处理
  startDownload: function (removeWatermark) {
    // 验证输入
    if (!this.validateInput()) {
      return
    }

    // 设置下载状态
    this.setData({
      isDownloading: true
    })

    console.log('开始下载视频:', {
      url: this.data.videoUrl,
      removeWatermark: removeWatermark,
      quality: this.data.qualityOptions[this.data.qualityIndex]
    })

    // 构建请求数据
    const requestData = {
      url: this.data.videoUrl,
      remove_watermark: removeWatermark,
      quality: this.getQualityValue()
    }

    // 调用下载API
    this.callDownloadAPI(requestData)
  },

  // 验证输入
  validateInput: function () {
    const url = this.data.videoUrl.trim()
    
    // 检查是否输入了链接
    if (!url) {
      this.showToast('请输入视频链接', 'error')
      return false
    }
    
    // 检查链接格式
    if (!this.isValidUrl(url)) {
      this.showToast('请输入有效的视频链接', 'error')
      return false
    }
    
    // 检查是否支持该平台
    if (!this.isSupportedPlatform(url)) {
      this.showToast('暂不支持该平台的视频下载', 'error')
      return false
    }
    
    return true
  },

  // 验证URL格式
  isValidUrl: function (url) {
    try {
      new URL(url)
      return true
    } catch (e) {
      return false
    }
  },

  // 检查是否支持该平台
  isSupportedPlatform: function (url) {
    const supportedDomains = [
      'douyin.com', 'kuaishou.com', 'weibo.com', 'bilibili.com',
      'youtube.com', 'instagram.com', 'tiktok.com', 'xiaohongshu.com',
      'ixigua.com'
    ]
    
    const domain = new URL(url).hostname.toLowerCase()
    return supportedDomains.some(domain => domain.includes(domain))
  },

  // 获取质量值
  getQualityValue: function () {
    const qualityMap = {
      0: 'best',    // 最佳质量
      1: 'high',    // 高清
      2: 'medium'   // 标清
    }
    return qualityMap[this.data.qualityIndex] || 'best'
  },

  // 调用下载API
  callDownloadAPI: function (requestData) {
    // 显示加载提示
    wx.showLoading({
      title: '正在下载...',
      mask: true
    })

    // 发起网络请求
    wx.request({
      url: `${this.data.apiBaseUrl}/api/download`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      data: requestData,
      success: (res) => {
        console.log('下载API响应:', res)
        this.handleDownloadSuccess(res.data)
      },
      fail: (err) => {
        console.error('下载API失败:', err)
        this.handleDownloadError(err)
      },
      complete: () => {
        // 隐藏加载提示
        wx.hideLoading()
        
        // 重置下载状态
        this.setData({
          isDownloading: false
        })
      }
    })
  },

  // 处理下载成功
  handleDownloadSuccess: function (data) {
    console.log('下载成功:', data)
    
    if (data.success) {
      // 保存下载结果
      this.setData({
        currentDownloadResult: data
      })
      
      // 添加到历史记录
      this.addToHistory(data)
      
      // 显示成功弹窗
      this.showResultModal('下载成功', '视频已成功下载，是否保存到相册？', true)
    } else {
      // 显示错误信息
      this.showResultModal('下载失败', data.message || '下载失败，请重试', false)
    }
  },

  // 处理下载错误
  handleDownloadError: function (error) {
    console.error('下载错误:', error)
    
    let errorMessage = '网络错误，请检查网络连接'
    
    if (error.errMsg) {
      if (error.errMsg.includes('timeout')) {
        errorMessage = '请求超时，请重试'
      } else if (error.errMsg.includes('fail')) {
        errorMessage = '网络连接失败，请检查网络设置'
      }
    }
    
    this.showResultModal('下载失败', errorMessage, false)
  },

  // 显示结果弹窗
  showResultModal: function (title, message, success) {
    this.setData({
      showResultModal: true,
      resultModal: {
        title: title,
        message: message,
        success: success
      }
    })
  },

  // 关闭结果弹窗
  closeResultModal: function () {
    this.setData({
      showResultModal: false
    })
  },

  // 保存到相册
  saveToAlbum: function () {
    const result = this.data.currentDownloadResult
    if (!result || !result.video_url) {
      this.showToast('没有可保存的视频', 'error')
      return
    }

    // 显示保存提示
    wx.showLoading({
      title: '正在保存...',
      mask: true
    })

    // 下载视频文件
    wx.downloadFile({
      url: result.video_url,
      success: (res) => {
        console.log('文件下载成功:', res)
        
        // 保存到相册
        wx.saveVideoToPhotosAlbum({
          filePath: res.tempFilePath,
          success: () => {
            wx.hideLoading()
            this.showToast('已保存到相册', 'success')
            this.closeResultModal()
          },
          fail: (err) => {
            wx.hideLoading()
            console.error('保存到相册失败:', err)
            
            if (err.errMsg.includes('auth deny')) {
              this.showToast('需要相册权限，请在设置中开启', 'error')
            } else {
              this.showToast('保存失败，请重试', 'error')
            }
          }
        })
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('文件下载失败:', err)
        this.showToast('视频下载失败，请重试', 'error')
      }
    })
  },

  // 添加到历史记录
  addToHistory: function (data) {
    const history = this.data.downloadHistory
    
    // 创建历史记录项
    const historyItem = {
      id: Date.now(),  // 使用时间戳作为ID
      title: data.filename || '未知标题',
      platform: data.platform || '未知平台',
      time: this.formatTime(new Date()),
      success: data.success,
      url: data.video_url,
      fileSize: data.file_size,
      duration: data.duration
    }
    
    // 添加到历史记录开头
    history.unshift(historyItem)
    
    // 限制历史记录数量（最多保存20条）
    if (history.length > 20) {
      history.splice(20)
    }
    
    // 更新数据
    this.setData({
      downloadHistory: history
    })
    
    // 保存到本地存储
    this.saveDownloadHistory()
  },

  // 查看历史记录项
  viewHistoryItem: function (e) {
    const item = e.currentTarget.dataset.item
    console.log('查看历史记录:', item)
    
    // 显示历史记录详情
    let message = `标题: ${item.title}\n平台: ${item.platform}\n时间: ${item.time}`
    
    if (item.fileSize) {
      message += `\n大小: ${this.formatFileSize(item.fileSize)}`
    }
    
    if (item.duration) {
      message += `\n时长: ${this.formatDuration(item.duration)}`
    }
    
    wx.showModal({
      title: '下载详情',
      content: message,
      showCancel: false,
      confirmText: '确定'
    })
  },

  // 清空历史记录
  clearHistory: function () {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有下载历史吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({
            downloadHistory: []
          })
          this.saveDownloadHistory()
          this.showToast('历史记录已清空', 'success')
        }
      }
    })
  },

  // 加载下载历史
  loadDownloadHistory: function () {
    try {
      const history = wx.getStorageSync('downloadHistory') || []
      this.setData({
        downloadHistory: history
      })
      console.log('加载历史记录:', history.length, '条')
    } catch (e) {
      console.error('加载历史记录失败:', e)
    }
  },

  // 保存下载历史
  saveDownloadHistory: function () {
    try {
      wx.setStorageSync('downloadHistory', this.data.downloadHistory)
      console.log('保存历史记录成功')
    } catch (e) {
      console.error('保存历史记录失败:', e)
    }
  },

  // 获取支持的平台
  getSupportedPlatforms: function () {
    wx.request({
      url: `${this.data.apiBaseUrl}/api/supported_platforms`,
      method: 'GET',
      success: (res) => {
        console.log('获取支持的平台:', res.data)
        if (res.data && res.data.platforms) {
          this.setData({
            supportedPlatforms: res.data.platforms
          })
        }
      },
      fail: (err) => {
        console.error('获取支持的平台失败:', err)
      }
    })
  },

  // 检查网络状态
  checkNetworkStatus: function () {
    wx.getNetworkType({
      success: (res) => {
        console.log('网络类型:', res.networkType)
        if (res.networkType === 'none') {
          this.showToast('请检查网络连接', 'error')
        }
      }
    })
  },

  // 刷新页面数据
  refreshPageData: function () {
    // 重新获取支持的平台
    this.getSupportedPlatforms()
    
    // 重新加载历史记录
    this.loadDownloadHistory()
    
    this.showToast('数据已刷新', 'success')
  },

  // 显示提示信息
  showToast: function (message, type = 'info') {
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

  // 格式化时间
  formatTime: function (date) {
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hour = date.getHours().toString().padStart(2, '0')
    const minute = date.getMinutes().toString().padStart(2, '0')
    
    return `${year}-${month}-${day} ${hour}:${minute}`
  },

  // 格式化文件大小
  formatFileSize: function (bytes) {
    if (bytes === 0) return '0 B'
    
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  },

  // 格式化时长
  formatDuration: function (seconds) {
    if (!seconds) return '未知'
    
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = Math.floor(seconds % 60)
    
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }
})
