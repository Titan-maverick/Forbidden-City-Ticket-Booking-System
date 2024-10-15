// pages/orders/orders.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    orderDetails: [],
    ticket_types: [],
  },
  
  handleBackClick() {
    wx.navigateBack({
      delta: 1 // 返回上一级页面
    });
  },
  
  onLoad(options) {
    try {
      const selectedOrder = JSON.parse(decodeURIComponent(options.selectedOrder));
      const ticket_typesString = JSON.parse(decodeURIComponent(options.ticket_types));
  
      if (!Array.isArray(ticket_typesString)) {
        throw new Error('Ticket types is not an array');
      }
      // 转换 price 为数字
      const ticketTypesWithNumbers = ticket_typesString.map(ticket => {
        return {
          ...ticket,
          price: parseFloat(ticket.price) // 转换为数字
        };
      });
      this.setData({
        orderDetails: selectedOrder,
        ticket_types: ticketTypesWithNumbers,
      });
  
      // console.log('Order details:', this.data.orderDetails);
      // console.log('Ticket types:', this.data.ticket_types);
    } catch (error) {
      console.error('Error parsing order data:', error);
    }
    console.log('orderDetails: ',this.data.orderDetails)
  },

  // 去支付
  goToPay() {
      const order_id = this.data.orderDetails.order_id;
      const token = wx.getStorageSync('token');
      wx.request({
        url: 'https://bass-epic-mentally.ngrok-free.app/pay/',
        method: 'POST',
        header: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`  // 如果需要 token 进行认证
        },
        data: {
          order_id: order_id,
        },
        success: (res) => { // 使用箭头函数
          if (res.statusCode === 200) { // 修正状态码
            wx.showToast({
              title: '假设您付钱了,提交成功',
              icon: 'success'
            });
            setTimeout(() => {
              wx.reLaunch({
                url: '/pages/orders/orders'  // 跳转到主页
              });
            }, 1000);  // 停顿1秒
          } else {
            wx.showToast({
              title: res.data.error || '提交失败',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error(err);
          wx.showToast({
            title: '网络错误',
            icon: 'none'
          });
        }
      });
  },

    // 再次预订
    bookAgain() {
      // 逻辑代码，例如重新创建订单
      wx.navigateTo({
        url: '/pages/ticket/ticket'
      });
    },

    //退票
    refund() {
      const orderDetails = this.data.orderDetails;
      const token = wx.getStorageSync('token');
    
      wx.request({
        url: 'https://bass-epic-mentally.ngrok-free.app/refund/',  // 替换为实际的退票接口
        method: 'POST',
        header: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`  // 使用 token 进行认证
        },
        data: {
          orderDetails: orderDetails, 
        },
        success: (res) => {
          if (res.statusCode === 200) {
            wx.showToast({
              title: '退票申请成功',
              icon: 'success'
            });
            setTimeout(() => {
              wx.reLaunch({
                url: '/pages/orders/orders'  // 跳转到订单页面
              });
            }, 1000);  // 停顿1秒
          } else {
            wx.showToast({
              title: res.data.error || '退票失败',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error(err);
          wx.showToast({
            title: '网络错误',
            icon: 'none'
          });
        }
      });
    },
    
    requestInvoice(){
      wx.showToast({
        title: '尽请期待',
        icon: 'none'
      });
    }
});
