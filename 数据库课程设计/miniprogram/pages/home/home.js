// pages/home/home.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    swiperImages: [
      { src: '/assets/images/home/slide1.png', page: 'notice_page1' },
      { src: '/assets/images/home/slide2.png', page: 'notice_page2' },
      { src: '/assets/images/home/slide3.png', page: 'notice_page3' }
    ],
    notices: [
      '【公告】故宫博物馆订票须知',
      '【公告】故宫博物馆订票须知',
      '【公告】故宫博物馆关于优化分时段预约参观的通告'
    ],
    currentNotice: '',
    currentIndex: 0
  },

  handleBuyClick() {
    wx.navigateTo({
      url: `/pages/ticket/ticket` // 跳转到相应的购票页面
    });
  },
  handleYear_ticketClick(){
    wx.showToast({
      title: '尽请期待',
      icon: 'none'
    });
  },

  handleSwiperItemClick(e) {
    const index = e.currentTarget.dataset.index; // 从事件对象中获取当前索引
    const page = e.currentTarget.dataset.page; // 从事件对象中获取页面信息
    if (index === 2) { // 判断是否为第三个轮播图
      wx.navigateTo({
        url: '小程序://问卷星/cABHYIyPgyTQtNc' // 跳转到外部链接
      });
    } else if (page) {
      wx.navigateTo({
        url: `/pages/${page}/${page}` // 跳转到相应的页面
      });
    } else {
      console.error('Page is not defined');
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.startNoticeSwitch();
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {
    // 页面卸载时清除定时器
    clearInterval(this.noticeInterval);
  },

  /**
   * 切换公告内容
   */
  startNoticeSwitch() {
    // 初始化显示第一条公告
    this.setData({
      currentNotice: this.data.notices[0]
    });

    // 设置定时器每隔 3 秒切换公告
    this.noticeInterval = setInterval(() => {
      let nextIndex = (this.data.currentIndex + 1) % this.data.notices.length;
      this.setData({
        currentNotice: this.data.notices[nextIndex],
        currentIndex: nextIndex
      });
    }, 3000); // 3 秒切换一次
  },

  /**
   * 处理声音按钮点击事件
   */
  handleSoundClick() {
    wx.showToast({
      title: '你好',
      icon: 'none'
    });
    // 可以在这里添加播放声音的逻辑
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {
    // 添加下拉刷新逻辑
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    // 添加上拉触底逻辑
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    // 添加分享逻辑
  }
});
