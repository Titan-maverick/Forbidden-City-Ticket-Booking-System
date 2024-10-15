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

  handleBackClick() {
    wx.navigateBack({
      delta: 1 // 返回上一级页面
    });
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
  


  confirmOrder() {
    const audienceList = this.data.audienceList;
    const phoneNumber = this.data.phoneNumber;
    const selectedDate = this.data.selectedDate;
    const selectedTime = this.data.selectedTime;
    const totalPrice = this.data.totalPrice;
    const token = this.data.token; 
    const purchaseQuantities = (audienceList.map(audience => audience.quantity)).length; // 购买数量
    console.log('test_audienceList: ',audienceList)

    wx.request({
      url: 'https://bass-epic-mentally.ngrok-free.app/comfirm-orders/',
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`  // 如果需要 token 进行认证
      },
      data: {
        audienceList: audienceList, 
        phoneNumber: phoneNumber,  
        totalPrice: totalPrice,  
        selectedTime: selectedTime,
        selectedDate: selectedDate,
        purchaseQuantities: purchaseQuantities,  // 传递购买数量
      },
      success: (res) => { // 使用箭头函数
        if (res.statusCode === 201) {
          wx.showToast({
            title: '订单提交成功',
            icon: 'success'
          });
          // 将数据转化为 URL 编码的字符串
          const audienceListString = encodeURIComponent(JSON.stringify(audienceList));
          const selectedDateEncoded = encodeURIComponent(selectedDate);
          const selectedTimeEncoded = encodeURIComponent(selectedTime);
          const phoneNumberEncoded = encodeURIComponent(phoneNumber);
          const totalPriceEncoded = encodeURIComponent(totalPrice);
          const order_idEncoded = encodeURIComponent(res.data.order_id);
          // 跳转到确认页面
          wx.navigateTo({
            url: `/pages/pay/pay?audienceList=${audienceListString}&selectedDate=${selectedDateEncoded}&selectedTime=${selectedTimeEncoded}&phoneNumber=${phoneNumberEncoded}&totalPrice=${totalPriceEncoded}&order_id=${order_idEncoded}`,
          });
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
