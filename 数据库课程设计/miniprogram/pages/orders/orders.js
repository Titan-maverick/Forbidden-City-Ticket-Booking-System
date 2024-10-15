// pages/orders/orders.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    activeTab: '全部', // 当前激活的tab
    orders: [], // 存储订单信息
    ticket_types: [],
  },

  // 检查登录状态
  checkLogin() {
    const token = wx.getStorageSync('token'); // 假设 token 存储在本地
    if(token)
    console.log('已登录')
    return !!token; // 返回布尔值
  },

    // 从后端获取订单数据
    fetchOrders() {
      const token = wx.getStorageSync('token'); // 获取token
      return new Promise((resolve, reject) => {
        wx.request({
          url: 'https://bass-epic-mentally.ngrok-free.app/my-orders/',
          method: 'POST',
          header: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // 设置请求头
          },
          success: (res) => {
            if (res.statusCode === 200) {
              resolve(res.data.orders); // 假设后端返回的订单数据在 orders 字段
              const orders = res.data.orders;
              const ticket_types = res.data.ticket_types;
              // console.log('orders',orders)
              // console.log('ticket_types',ticket_types)
              this.setData({
                ticket_types: ticket_types
              });
                        // 统计每种票的数量
              this.updateConciseOrders(orders, ticket_types);

            } else {
              reject('获取订单失败');
            }
          },
          fail: (err) => {
            reject(err);
          }
        });
      });
    },

    updateConciseOrders(orders, ticket_types) {
      // 遍历所有订单
      orders.forEach(order => {
        const ticketCount = {}; // 每个订单的票种计数
        let totalPrice = 0; // 初始化总价为 0
    
        // 遍历该订单的 order_details
        order.audienceList.forEach(detail => {
          const ticketTypeId = detail.ticket_type_id;
          const isClockMuseumSelected = detail.isClockMuseumSelected;
          const isExhibitionSelected = detail.isExhibitionSelected;
          const isTreasureIslandSelected = detail.isTreasureIslandSelected;
    
          // 原有的票计数
          if (ticketCount[ticketTypeId]) {
            ticketCount[ticketTypeId].quantity += 1; // 累加数量 +1
          } else {
            const ticketType = ticket_types.find(ticket => ticket.ticket_type_id === ticketTypeId);
            ticketCount[ticketTypeId] = {
              ticket_type_id: ticketTypeId,
              type_name: ticketType ? ticketType.type_name : '未知票种',
              price: ticketType ? Number(ticketType.price) : 0,
              quantity: 1
            };
          }
    
          // 统计票价
          totalPrice += ticketCount[ticketTypeId].price;
    
          // 根据选择判断是否是其他馆的票
          if (isTreasureIslandSelected) {
            switch (ticketTypeId) {
              case 1: ticketCount['treasure_island_5'] = { ticket_type_id: 5, type_name: "珍宝馆标准票", price: 10, quantity: (ticketCount['treasure_island_5']?.quantity || 0) + 1 }; break;
              case 2: ticketCount['treasure_island_6'] = { ticket_type_id: 6, type_name: "珍宝馆老年人票", price: 5, quantity: (ticketCount['treasure_island_6']?.quantity || 0) + 1 }; break;
              case 3: ticketCount['treasure_island_7'] = { ticket_type_id: 7, type_name: "珍宝馆未成年人票", price: 0, quantity: (ticketCount['treasure_island_7']?.quantity || 0) + 1 }; break;
              case 4: ticketCount['treasure_island_8'] = { ticket_type_id: 8, type_name: "珍宝馆学生票", price: 5, quantity: (ticketCount['treasure_island_8']?.quantity || 0) + 1 }; break;
            }
          }
    
          if (isClockMuseumSelected) {
            switch (ticketTypeId) {
              case 1: ticketCount['clock_museum_9'] = { ticket_type_id: 9, type_name: "钟表馆标准票", price: 10, quantity: (ticketCount['clock_museum_9']?.quantity || 0) + 1 }; break;
              case 2: ticketCount['clock_museum_10'] = { ticket_type_id: 10, type_name: "钟表馆老年人票", price: 5, quantity: (ticketCount['clock_museum_10']?.quantity || 0) + 1 }; break;
              case 3: ticketCount['clock_museum_11'] = { ticket_type_id: 11, type_name: "钟表馆未成年人票", price: 0, quantity: (ticketCount['clock_museum_11']?.quantity || 0) + 1 }; break;
              case 4: ticketCount['clock_museum_12'] = { ticket_type_id: 12, type_name: "钟表馆学生票", price: 5, quantity: (ticketCount['clock_museum_12']?.quantity || 0) + 1 }; break;
            }
          }
    
          if (isExhibitionSelected) {
            ticketCount['exhibition_13'] = { ticket_type_id: 13, type_name: "展览", price: 0, quantity: (ticketCount['exhibition_13']?.quantity || 0) + 1 };
          }
        });
    
        // 计算该订单的总价
        totalPrice = Object.values(ticketCount).reduce((sum, item) => sum + item.price * item.quantity, 0);
        order.Concise_orders = Object.values(ticketCount); // 添加到当前订单
        order.total = totalPrice; // 更新订单的总价
      });
    
      // 更新 data 中的 orders
      this.setData({
        orders: orders.reverse() // 更新 orders 数据
      });
    
    },
    
  // 点击切换标签
  changeTab: function(event) {
    const tab = event.currentTarget.dataset.tab; // 获取被点击标签的数据
    this.setData({
      activeTab: tab // 更新选中的标签
    });
  },

  goToOrderDetail(event) {
    const orderId = event.currentTarget.dataset.orderId; // 获取订单 ID
    const selectedOrder = this.data.orders.find(order => order.order_id === orderId); // 找到对应的订单信息

    // 将 selectedOrder 转换为 JSON 字符串并进行编码
    const selectedOrderString = encodeURIComponent(JSON.stringify(selectedOrder));
    const ticket_typesString = encodeURIComponent(JSON.stringify(this.data.ticket_types));

    wx.navigateTo({
      url: `/pages/order_detail/order_detail?selectedOrder=${selectedOrderString}&ticket_types=${ticket_typesString}`,
    });
  },
  
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    if (this.checkLogin()) {
      this.fetchOrders()
        .then(orders => {
          this.setData({ orders });
        })
        .catch(err => {
          wx.showToast({ title: '加载订单失败', icon: 'none' });
          console.error(err);
        });
    } else {
      wx.showToast({ title: '请先登录', icon: 'none' });
      // 这里可以跳转到登录页面
      wx.redirectTo({ url: '/pages/my/my' });
    }
  },


  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    if (this.checkLogin()) {
      this.fetchOrders()
        .then(orders => {
          this.setData({ orders });
        })
        .catch(err => {
          wx.showToast({ title: '加载订单失败', icon: 'none' });
          console.error(err);
        });
    } else {
      wx.showToast({ title: '请先登录', icon: 'none' });
      wx.redirectTo({ url: '/pages/my/my' });
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})