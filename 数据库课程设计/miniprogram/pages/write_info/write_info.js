Page({
  data: {
    ticketList: [],       // 存储传递过来的票种列表
    selectedDate: '',     // 存储传递过来的日期
    selectedTime: '',     // 存储传递过来的时间
    phoneNumber: '',      // 存储本机用户手机号码
    audienceList: [],     // 存储观众信息
    isVisitorSelectorVisible: false,
    currentInputIndex: null, // 当前输入框的索引
    totalSelectedCount: 0,
    idTypes: ['身份证', '港澳居民往来内地通行证', '外国人永久居留身份证', '护照', '台湾居民来往大陆通行证', '港澳居民居住证'], // 证件类型列表
    allInputsFilled: false, // 是否所有输入框都填写了
    frequent_visitors: {}, // 存储常用观众信息
    frequentVisitors: [], // 直接在data中声明
    token: '',
    selectedTicketCount: 0 // 存储选中的票种数量
  },


    // 显示常用观众选择框
    showVisitorSelector(e) {
      const index = e.currentTarget.dataset.index;
      this.setData({
        isVisitorSelectorVisible: true,
        currentInputIndex: index, // 保存当前输入框的索引
      });
    },

selectVisitor(e) {
  const selectedVisitor = e.currentTarget.dataset.visitor; // 获取选择的观众信息
  const index = this.data.currentInputIndex; // 获取当前输入框的索引
  // 复制观众列表并更新当前索引的姓名和证件信息
  const updatedList = [...this.data.audienceList];
  updatedList[index].name = selectedVisitor.name; // 填入选择的姓名
  updatedList[index].idNumber = selectedVisitor.id_card; // 填入选择的证件号码
  updatedList[index].selectedIdTypeIndex = selectedVisitor.id_type;

  // 如果常用观众的证件类型也需要填入，可以添加如下行：
  const idTypeIndex = this.data.idTypes.findIndex(type => type === selectedVisitor.id_type); // 找到对应的证件类型索引
  if (idTypeIndex !== -1) {
    updatedList[index].selectedIdTypeIndex = idTypeIndex; // 填入证件类型
  }

  this.setData({
    audienceList: updatedList,
    isVisitorSelectorVisible: false, // 关闭弹窗
    currentInputIndex: null, // 选择后关闭选择框
  });
  const audienceList = this.data.audienceList; // 获取当前输入框的索引
  this.checkInputs(); // 检查输入框状态
},

  
    closeVisitorSelector() {
      this.setData({
        currentInputIndex: null, // 关闭选择框时清空选中索引
        isVisitorSelectorVisible: false // 关闭弹窗
      });
    },

  handleBackClick() {
    wx.navigateBack({
      delta: 1 // 返回上一级页面
    });
  },

  onLoad: function(options) {
    const { ticketList, selectedDate, selectedTime, totalSelectedCount } = options;
    const phoneNumber = wx.getStorageSync('phoneNumber');
    const frequent_visitors = wx.getStorageSync('frequent_visitors') || {};

    // 设置手机号码
    if (phoneNumber) {
        this.setData({
            phoneNumber: phoneNumber,
            totalSelectedCount: totalSelectedCount,
        });
    }

    // 设置常用观众信息，包括证件类型
    this.setData({
      frequentVisitors: [
          { name: frequent_visitors.name_1, id_card: frequent_visitors.id_card_1, id_type: frequent_visitors.id_type_1 },
          { name: frequent_visitors.name_2, id_card: frequent_visitors.id_card_2, id_type: frequent_visitors.id_type_2 },
          { name: frequent_visitors.name_3, id_card: frequent_visitors.id_card_3, id_type: frequent_visitors.id_type_3 },
          { name: frequent_visitors.name_4, id_card: frequent_visitors.id_card_4, id_type: frequent_visitors.id_type_4 },
          { name: frequent_visitors.name_5, id_card: frequent_visitors.id_card_5, id_type: frequent_visitors.id_type_5 },
      ].filter(visitor => visitor.name), // 过滤掉没有姓名的条目
  });  
    // 处理票务信息
    if (ticketList) {
        // 将传递的 ticketList 解析为对象
        const parsedTicketList = JSON.parse(ticketList);
        // 设置数据
        this.setData({
            ticketList: parsedTicketList,
            selectedDate,
            selectedTime,
        });

        // 生成观众信息
        this.generateAudienceInfo(parsedTicketList);
    }
  const phoneNumberRegex = /^1[3-9]\d{9}$/; // 中国手机号码的正则表达式
  const isValid = phoneNumberRegex.test(phoneNumber);
  this.setData({
    phoneNumber,
    phoneNumberValid: isValid
  });
  this.countSelectedTicketTypes();
  // 调用检查输入框状态的函数
  this.checkInputs();
},

countSelectedTicketTypes() {
  const count = this.data.ticketList.filter(ticket => ticket.count > 0).length;
  this.setData({
    selectedTicketCount: count
  });
},

  generateAudienceInfo(ticketList) {
    const audienceList = [];
    ticketList.forEach(ticket => {
      for (let i = 0; i < ticket.count; i++) {
        audienceList.push({
          ticketId: ticket.ticketId,
          ticketType: ticket.name,
          name: '',
          idNumber: '',
          price: ticket.price,
          selectedIdTypeIndex: 0 // 默认为身份证
        });
      }
    });
    this.setData({
      audienceList
    });
    this.checkInputs(); // 初始检查
  },

  handleNameInput(e) {
    const index = e.currentTarget.dataset.index;
    const name = e.detail.value;
    const updatedList = [...this.data.audienceList];
    updatedList[index].name = name;
    this.setData({
      audienceList: updatedList,
      isVisitorSelectorVisible: false, // 关闭选择框
    });
    this.checkInputs(); // 检查输入框状态
  },

  // 验证身份证号码的函数
validateIdCard(idCard) {
  // 正则表达式验证
  const idCardRegex = /^(?:\d{15}|\d{18}|\d{17}[\dX])$/;
  if (!idCardRegex.test(idCard)) {
    return false; // 正则验证失败
  }
  // 身份证算法校验
  if (idCard.length === 18) {
    const factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
    const parityBit = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
    let sum = 0;
    for (let i = 0; i < 17; i++) {
      sum += idCard[i] * factors[i];
    }
    const mod = sum % 11;
    const validBit = parityBit[mod];

    return idCard[17].toUpperCase() === validBit; // 校验最后一位
  }
  return true; // 如果是15位身份证，直接返回true
},

  handleIdNumberInput(e) {
    const index = e.currentTarget.dataset.index;
    const idNumber = e.detail.value;
    const selectedIdTypeIndex = this.data.audienceList[index].selectedIdTypeIndex;
    const idType = this.data.idTypes[selectedIdTypeIndex];
    const updatedList = [...this.data.audienceList];
    updatedList[index].idNumber = idNumber;
    // 如果选择的是身份证，进行正则表达式验证和算法校验
    if (idType === '身份证') {
      const isValid = this.validateIdCard(idNumber);
      if (!isValid) {
        wx.showToast({
          title: '身份证号码不合法',
          icon: 'none'
        });
        return;
      }
    }
    this.setData({
      audienceList: updatedList,    
      isVisitorSelectorVisible: false, // 关闭选择框
    });
    this.checkInputs(); // 检查输入框状态
  },

  handleIdTypeChange(e) {
    const index = e.currentTarget.dataset.index;
    const selectedIndex = e.detail.value;

    // 更新观众列表中的证件类型索引
    const updatedList = [...this.data.audienceList];
    updatedList[index].selectedIdTypeIndex = selectedIndex;

    this.setData({
      audienceList: updatedList
    });
    this.checkInputs(); // 检查输入框状态
  },

  handlePhoneInput(e) {
    this.setData({
      phoneNumber: e.detail.value
    });
    this.checkInputs(); // 检查输入框状态
  },


  // 处理手机号码输入
handlePhoneInput(e) {
  const phoneNumber = e.detail.value;
  const phoneNumberRegex = /^1[3-9]\d{9}$/; // 中国手机号码的正则表达式
  
  const isValid = phoneNumberRegex.test(phoneNumber);
  
  this.setData({
    phoneNumber,
    phoneNumberValid: isValid
  });
  
  // 调用检查输入框状态的函数
  this.checkInputs();
},

// 检查所有输入框是否填写了
checkInputs() {


  const allFilled = this.data.audienceList.every(audience => 
    audience.name.trim() !== '' &&
    audience.idNumber.trim() !== ''
  ) && this.data.phoneNumber.trim() !== '' && this.data.phoneNumberValid;
  
  this.setData({
    allInputsFilled: allFilled,
  });
},

  confirmOrder() {
    if (!this.data.allInputsFilled) {
      wx.showToast({
        title: '请填写所有必填信息',
        icon: 'none'
      });
      return;
    }
      // 将数据转化为 URL 编码的字符串
  const audienceListString = encodeURIComponent(JSON.stringify(this.data.audienceList));
  const selectedDate = encodeURIComponent(this.data.selectedDate);
  const selectedTime = encodeURIComponent(this.data.selectedTime);
  const phoneNumber = encodeURIComponent(this.data.phoneNumber);
  ;
  wx.navigateTo({
    url: `/pages/choose_two_pavilion/choose_two_pavilion?audienceList=${audienceListString}&selectedDate=${selectedDate}&selectedTime=${selectedTime}&phoneNumber=${phoneNumber}`,
  });  
  }
});
