Page({
  data: {
    todayDate: '', 
    tomorrowDate: '', 
    dayAfterTomorrowDate: '', 
    selectedDate: '', 
    selectedTime: '',
    isDateSelected: false, 
    isTimeSelected: false, 
    isSpecifytime: false, 
    showCalendarPopup: false,
    minDate: new Date().getTime(),
    maxDate: new Date(new Date().setDate(new Date().getDate() + 6)).getTime(), 
    tickets_count_am: 0,
    tickets_count_pm: 0,
    ticketList: [
      { ticketId: 1, name: '标准票', price: 60, count: 0 , hint: '成人'},
      { ticketId: 2, name: '老年人票', price: 30, count: 0 , hint: '60周岁以上(含60周岁)老年人'},
      { ticketId: 3, name: '未成年人免费票', price: 0, count: 0 , hint: '未满18周岁的中国公民'},
      { ticketId: 4, name: '学生票', price: 20, count: 0 , hint: '18周岁以上、本科及以下学历(不含成人教育，研究生需购买标准票)'}
    ],
    totalSelectedCount: 0,
  },

  onLoad: function () {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    const dayAfterTomorrow = new Date(today);
    dayAfterTomorrow.setDate(today.getDate() + 2);

    const formatDate = (date) => {
      const year = date.getFullYear(); // 获取年份
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      return `${year}年${month}月${day}日`;
    };

    this.setData({
      todayDate: formatDate(today),
      tomorrowDate: formatDate(tomorrow),
      dayAfterTomorrowDate: formatDate(dayAfterTomorrow)
    });
  },

  checkAvailableTickets(selectedDate) {
    const token = wx.getStorageSync('token');
    wx.request({
      url: 'https://bass-epic-mentally.ngrok-free.app/get-available-tickets/',
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`  // 如果需要 token 进行认证
      },
      data: {
        selectedDate: selectedDate,
      },
      success: (res) => {
        if (res.statusCode === 200) { // 修正状态码
          const morning_tickets_available = res.data.morning_tickets_available;
          const afternoon_tickets_available = res.data.afternoon_tickets_available;
          this.setData({
            morning_tickets_available: morning_tickets_available,
            afternoon_tickets_available: afternoon_tickets_available,
          });
          console.log(morning_tickets_available);
          console.log(afternoon_tickets_available);
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

  showCalendar() {
    this.setData({ showCalendarPopup: true });
  },

  onDateConfirm(event) {
    const date = new Date(event.detail); 
    const formatDate = (date) => {
      const year = date.getFullYear(); // 获取年份
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      return `${year}年${month}月${day}日`;
    };
    const formattedDate = formatDate(date); 
      // 清空票数
  const resetTicketList = this.data.ticketList.map(ticket => {
    return { ...ticket, count: 0 }; // 将所有票的数量重置为 0
  });
    this.setData({
      selectedDate: formattedDate,
      isDateSelected: true,
      showCalendarPopup: false,
      isSpecifytime: true,
      ticketList: resetTicketList, // 更新票列表
      totalSelectedCount: 0 // 也重置总票数
    });
    this.checkAvailableTickets(formattedDate);
  },

  onDateCancel() {
    this.setData({ showCalendarPopup: false });
  },

  handleDateClick(e) {
    const resetTicketList = this.data.ticketList.map(ticket => {
      return { ...ticket, count: 0 }; // 将所有票的数量重置为 0
    });
    const selectedDate = e.currentTarget.dataset.date;
    this.setData({
      selectedDate: selectedDate,
      isDateSelected: true,
      isTimeSelected: false,
      selectedTime: '',
      isSpecifytime: false,
      ticketList: resetTicketList, // 更新票列表
      totalSelectedCount: 0 // 也重置总票数
    });
    this.checkAvailableTickets(selectedDate);
  },


  selectAM() {
  const resetTicketList = this.data.ticketList.map(ticket => {
    return { ...ticket, count: 0 }; // 将所有票的数量重置为 0
  });
    this.setData({
      isTimeSelected: true,
      selectedTime: '上午',
      ticketList: resetTicketList, // 更新票列表
      totalSelectedCount: 0 // 也重置总票数
    });
  },

  selectPM() {
    const resetTicketList = this.data.ticketList.map(ticket => {
      return { ...ticket, count: 0 }; // 将所有票的数量重置为 0
    });
    this.setData({
      isTimeSelected: true,
      selectedTime: '下午',
      ticketList: resetTicketList, // 更新票列表
      totalSelectedCount: 0 // 也重置总票数
    });
  },

  handlePurchase() {
    wx.showToast({
      title: '购票成功',
      icon: 'success'
    });
  },

  changeTicketNum(e) {
    const { id } = e.currentTarget.dataset;
    const newCount = e.detail;
    
    let totalSelectedCount = 0;
    const updatedTicketList = this.data.ticketList.map(ticket => {
      if (ticket.ticketId === id) {
        ticket.count = newCount;
      }
      totalSelectedCount += ticket.count;
      return ticket;
    });
    
    if (totalSelectedCount > 5) {
      wx.showToast({
        title: '每单限购5张票',
        icon: 'none'
      });
      return;
    }
  
    this.setData({
      ticketList: updatedTicketList,
      totalSelectedCount
    });
  },

  confirmOrder() {
    const ticketList = this.data.ticketList;
    const selectedDate = this.data.selectedDate;
    const selectedTime = this.data.selectedTime;
    const totalSelectedCount = this.data.totalSelectedCount;
    if (totalSelectedCount === 0) {
      wx.showToast({
        title: '请先选择门票数量',
        icon: 'none',
        duration: 2000,
      });
    } else {
      wx.navigateTo({
        url: `/pages/write_info/write_info?ticketList=${JSON.stringify(ticketList)}&selectedDate=${selectedDate}&selectedTime=${selectedTime}&totalSelectedCount=${totalSelectedCount}`,
      });      
    }
  },

  handleBackClick() {
    wx.navigateBack({
      delta: 1
    });
  },
});
