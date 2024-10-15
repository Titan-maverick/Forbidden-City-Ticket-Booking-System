Page({
  data: {
    audienceList: [],     // 存储观众信息
    selectedDate: '',     // 存储传递过来的日期
    selectedTime: '',     // 存储传递过来的时间
    phoneNumber: '',      // 存储本机用户手机号码
    totalPrice: 0,        // 存储总价
    token: '',
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
      const token = wx.getStorageSync('token');
      this.setData({
        token: token,
      });
      wx.request({
        url: 'https://bass-epic-mentally.ngrok-free.app/get-available-othertickets/',
        method: 'POST',
        header: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`  // 如果需要 token 进行认证
        },
        data: {
          selectedDate: selectedDate,
          selectedTime: selectedTime,
        },
        success: (res) => {
          if (res.statusCode === 200) { // 修正状态码
            const treasure_tickets_available = res.data.treasure_tickets_available;
            const clock_tickets_available = res.data.clock_tickets_available;
            const exhibition_tickets_available = res.data.exhibition_tickets_available;
            this.setData({
              treasure_tickets_available: treasure_tickets_available,
              clock_tickets_available: clock_tickets_available,
              exhibition_tickets_available: exhibition_tickets_available,
            });
            console.log(treasure_tickets_available);
            console.log(clock_tickets_available);
            console.log(exhibition_tickets_available);
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
      // 初始化每个观众的选择状态
      const updatedAudienceList = audienceList.map(audience => ({
        ...audience,
        isTreasureIslandSelected: false,  // 初始化时为未选中状态
        isClockMuseumSelected: false,     // 初始化时为未选中状态
        isExhibitionSelected: false,       // 初始化时为未选中状态
        ticketPrice: audience.price,
        TreasureIslandPrice: this.getPriceByIdNumber(audience.price).TreasureIslandPrice,
        ClockMuseumPrice: this.getPriceByIdNumber(audience.price).ClockMuseumPrice,
        exhibitionPrice: 0 // 展览价格为 0
      }));
  
      // 使用接收到的数据
      this.setData({
        audienceList: updatedAudienceList,
        selectedDate,
        selectedTime,
        phoneNumber
      });
    } catch (error) {
      console.error("Error parsing audienceList: ", error);
    }
    this.updateTotalPrice();

  },

    // 根据 idNumber 获取价格
    getPriceByIdNumber(price) {
      switch (price) {
        case 60:
          return { TreasureIslandPrice: 10, ClockMuseumPrice: 10 };
        case 20:
          return { TreasureIslandPrice: 5, ClockMuseumPrice: 5 };
        case 0:
          return { TreasureIslandPrice: 0, ClockMuseumPrice: 0 };
        case 30:
          return { TreasureIslandPrice: 5, ClockMuseumPrice: 5 };
        default:
          return { TreasureIslandPrice: 0, ClockMuseumPrice: 0 };
      }
    },

  // 更新总价
// 更新总价
updateTotalPrice() {
  const totalPrice = this.data.audienceList.reduce((total, audience) => {
    let audienceTotal = audience.ticketPrice;
    if (audience.isTreasureIslandSelected) {
      audienceTotal += audience.TreasureIslandPrice;
    }
    if (audience.isClockMuseumSelected) {
      audienceTotal += audience.ClockMuseumPrice;
    }
    if (audience.isExhibitionSelected) {
      audienceTotal += audience.exhibitionPrice;
    }
    return total + audienceTotal;
  }, 0);
  this.setData({ totalPrice });
},
    
  // 选择两馆：珍宝岛
  select_TreasureIsland(e) {
    const index = e.currentTarget.dataset.index;
    const updatedList = [...this.data.audienceList];
    updatedList[index].isTreasureIslandSelected = !updatedList[index].isTreasureIslandSelected; // 切换状态

    this.setData({ audienceList: updatedList });
    this.updateTotalPrice();
  },

  // 选择两馆：钟表馆
  select_ClockMuseum(e) {
    const index = e.currentTarget.dataset.index;
    const updatedList = [...this.data.audienceList];
    updatedList[index].isClockMuseumSelected = !updatedList[index].isClockMuseumSelected; // 切换状态
    this.setData({ audienceList: updatedList });
    this.updateTotalPrice();
  },

  // 选择展览
  select_exhibition(e) {
    const index = e.currentTarget.dataset.index;
    const updatedList = [...this.data.audienceList];
    updatedList[index].isExhibitionSelected = !updatedList[index].isExhibitionSelected; // 切换状态
    this.setData({ audienceList: updatedList });
    this.updateTotalPrice();
  },

  confirmOrder() {
    const audienceList = this.data.audienceList;
    const phoneNumber = this.data.phoneNumber;
    const selectedDate = this.data.selectedDate;
    const selectedTime = this.data.selectedTime;
    const totalPrice = this.data.totalPrice;

          // 将数据转化为 URL 编码的字符串
          const audienceListString = encodeURIComponent(JSON.stringify(audienceList));
          const selectedDateEncoded = encodeURIComponent(selectedDate);
          const selectedTimeEncoded = encodeURIComponent(selectedTime);
          const phoneNumberEncoded = encodeURIComponent(phoneNumber);
          const totalPriceEncoded = encodeURIComponent(totalPrice);
          // 跳转到确认页面
          wx.navigateTo({
            url: `/pages/confirm/confirm?audienceList=${audienceListString}&selectedDate=${selectedDateEncoded}&selectedTime=${selectedTimeEncoded}&phoneNumber=${phoneNumberEncoded}&totalPrice=${totalPriceEncoded}`,
          });
  }
  
});
