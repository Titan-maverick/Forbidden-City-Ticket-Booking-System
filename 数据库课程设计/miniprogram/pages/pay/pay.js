Page({
  data: {
    audienceList: [],     // 存储观众信息
    selectedDate: '',     // 存储传递过来的日期
    selectedTime: '',     // 存储传递过来的时间
    phoneNumber: '',      // 存储本机用户手机号码
    totalPrice: 0,        // 存储总价
    token: '',
    ticket_types: [],
    order_id: '',
  },

  onLoad: function(options) {
    try {
      const audienceList = JSON.parse(decodeURIComponent(options.audienceList));
      const selectedDate = decodeURIComponent(options.selectedDate);
      const selectedTime = decodeURIComponent(options.selectedTime);
      const phoneNumber = decodeURIComponent(options.phoneNumber);
      const totalPrice = decodeURIComponent(options.totalPrice);
      const order_id = encodeURIComponent(options.order_id);
      const token = wx.getStorageSync('token');
      const ticket_types = wx.getStorageSync('ticket_types');
        // 转换 price 为数字
      const ticketTypesWithNumbers = ticket_types.map(ticket => {
          return {
            ...ticket,
            price: parseFloat(ticket.price) // 转换为数字
          };
        });
      // 使用接收到的数据
      this.setData({
        audienceList: audienceList, // 使用解析后的 audienceList
        selectedDate: selectedDate,
        selectedTime: selectedTime,
        phoneNumber: phoneNumber,
        totalPrice: totalPrice,
        token: token,
        ticket_types: ticketTypesWithNumbers,
        order_id: order_id,
      });
  
      //console.log('audienceList:', audienceList);
      //console.log('ticket_types:', ticket_types);
      
    } catch (error) {
      console.error("Error parsing audienceList: ", error);
    }
  },
  


  goToPay() {
    const order_id = this.data.order_id;
    const token = this.data.token; 
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
            title: '提交成功',
            icon: 'success'
          });
          wx.showToast({
            title: '假设您已经付钱了',
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

  }
  
});
