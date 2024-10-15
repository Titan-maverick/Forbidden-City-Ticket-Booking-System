// pages/info/info.js

import { ComponentWithStore } from 'mobx-miniprogram-bindings'
import { userStore } from '@/stores/userstore'

Page({
  // 页面的初始数据
  data: {
    phoneNumber: '待完善',  // 默认值
    is_login: false,   // 标志是否登录
    isPopupVisible: false,
    isRectifyVisible: false,
    phoneNumber_input: '',
    phoneNumberValid: false,
    isphoneVisible: false,
    currentName: '',
    currentIdCard: '',
    currentIndex: '',
    selectedIdTypeIndex: 0, // 默认选择第一个证件类型
    idTypes: ['身份证', '港澳居民往来内地通行证', '外国人永久居留身份证', '护照', '台湾居民来往大陆通行证', '港澳居民居住证'], // 证件类型列表
    isFormValid: false, // 控制按钮是否可用
    frequent_visitors: {}, // 存储常用观众信息
  },
  
  onLoad() {
    this.store = userStore; // 声明 store
    try {
      // 从本地存储中同步获取 token
      const token = wx.getStorageSync('token');
      if (token) {
        const phoneNumber = wx.getStorageSync('phoneNumber');
        console.log('phoneNumber', phoneNumber)
        const frequent_visitors = wx.getStorageSync('frequent_visitors');
        console.log('frequent_visitors', frequent_visitors)
          this.setData({
            is_login: true,
            frequent_visitors: frequent_visitors,
          });
          if(phoneNumber){
            this.setData({
              phoneNumber: phoneNumber,
            });
          }
      } else {
        this.setData({
          is_login: false
        });
      }
    } catch (e) {
      // 获取 token 失败，可能是存储中没有 token
      console.error('获取 token 失败', e);
      this.setData({
        is_login: false
      });
    }
  },
  
// 获取用户的 openid
toLogin() {
  wx.login({
    success: res => {
      if (res.code) {
          // 将 code发送到后端
          wx.request({
            url: 'https://bass-epic-mentally.ngrok-free.app/login/',
            method: 'POST',
            header: {
              'Content-Type': 'application/json', // 设置为 JSON 格式
            },
            data: {
              code: res.code,
            },
            success: (response) => {
              if (response.statusCode === 200) {
                const frequent_visitors = response.data.frequent_visitors[0];
                const token = response.data.token;
                const phone_number = response.data.phone_number
                const ticket_types = response.data.ticket_types
                // 将 token 存储到 this.store
                this.store.token = token;
              // 将数据保存到缓存
              wx.setStorageSync('token', token);
              wx.setStorageSync('phoneNumber', phone_number);
              wx.setStorageSync('frequent_visitors', frequent_visitors);
              wx.setStorageSync('ticket_types', ticket_types);
              console.log('frequent_visitors', frequent_visitors)
                this.setData({
                  is_login: true,
                  frequent_visitors: frequent_visitors, // 更新
                });
                if(phone_number){
                  this.setData({
                    phoneNumber: phone_number,
                  });
                }
              }
            },
            fail: () => {
              wx.showToast({
                title: '登录失败',
                icon: 'none'
              });
            }
          });
        } 
      else {
         console.log('登录失败！' + res.errMsg);
      }
    }
  });
},



inputPhoneNumber(e) {
  if (!this.data.is_login) {
    wx.showToast({
      title: '请先登录',
      icon: 'none'
    });
    return;
  }
      const { encryptedData, iv } = e.detail;  // 直接从 e.detail 获取
    //个人开发者无法调用
      // if (!encryptedData || !iv) {
      //   wx.showToast({
      //     title: '获取手机号失败',
      //     icon: 'none'
      //   });
      //   return;
      // }
    
      // 发送请求到后端解密手机号
      // wx.request({
      //   url: 'https://你的后端/decrypt-phone/',  // 替换为实际的后端地址
      //   method: 'POST',
      //   data: {
      //     encryptedData: encryptedData,
      //     iv: iv
      //   },
      //   success: (res) => {
      //     if (res.statusCode === 200) {
      //       const phoneNumber = res.data.phoneNumber;  // 从响应中获取手机号
      //       this.setData({
      //         phoneNumber: phoneNumber
      //       });
      //       wx.showToast({
      //         title: '手机号获取成功',
      //         icon: 'success'
      //       });
      //     } else {
      //       wx.showToast({
      //         title: res.data.error || '手机号获取失败',
      //         icon: 'none'
      //       });
      //     }
      //   },

      //   fail: () => {
      //     wx.showToast({
      //       title: '网络错误',
      //       icon: 'none'
      //     });
      //   }
      // });
      this.setData({
        isphoneVisible: true,
      });
    },


    handleAddFavorite() {
      if (!this.data.is_login) {
        wx.showToast({
          title: '请先登录',
          icon: 'none'
        });
        return;
      }
      this.setData({
        isPopupVisible: true,
      });
    },
  
    handleClosePopup() {
      this.setData({
        currentName: '',
        currentIdCard: '',
        isFormValid: false,
        isPopupVisible: false, // 隐藏浮窗
        isRectifyVisible: false,
        isphoneVisible: false,
      });
    },
    
    handleNameInput(e) {
      this.setData({
        currentName: e.detail.value
      });
      this.checkFormValidity();
    },

    // 校验身份证号码
validateIdCard(idCard) {
  const regex = /^(?:\d{15}|\d{17}[\dxX])$/; // 验证15位和18位身份证号的正则表达式
  if (!regex.test(idCard)) {
    return false; // 格式不正确
  }

  // 进行18位身份证的校验
  if (idCard.length === 18) {
    const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
    const checkDigits = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
    const sum = idCard.slice(0, 17).split('').reduce((acc, num, i) => acc + num * weights[i], 0);
    const checkDigit = checkDigits[sum % 11];

    return checkDigit === idCard.charAt(17).toUpperCase(); // 检查校验位
  }

  return true; // 15位身份证号格式正确
},

handleIdCardInput(e) {
  this.setData({
    isFormValid: false,
  });
  const idCard = e.detail.value;
  const isValid = this.validateIdCard(idCard); // 调用验证函数

  if (!isValid) {
    wx.showToast({
      title: '身份证号码无效，请检查！',
      icon: 'none', // 图标类型为none，不显示图标
      duration: 300 // 显示时间
    });
  } else {
    // 如果验证通过，可以继续进行其他逻辑
    this.setData({
      currentIdCard: idCard,
      isFormValid: true, // 这里根据实际情况设置有效性
    });
  }
},

checkFormValidity() {
  const { currentName, currentIdCard } = this.data;
  const isValid = currentName.trim() !== '' && currentIdCard.trim() !== '' && this.validateIdCard(currentIdCard);
  
  this.setData({
    isFormValid: isValid,
  });
},


handleIdTypeChange(e) {
      this.setData({
        selectedIdTypeIndex: e.detail.value // 更新选择的证件类型索引
      });
    },
   
// 获取常用观众按钮上的信息
editVisitor(e) {
      const index = e.currentTarget.dataset.index;

        this.setData({
          currentName: this.data.frequent_visitors[`name_${(index)}`],
          currentIdCard: this.data.frequent_visitors[`id_card_${(index)}`],
          selectedIdTypeIndex: this.data.frequent_visitors[`id_type_${(index)}`],
          isRectifyVisible: true,
          currentIndex: index, // 保存当前索引
        });
    },

      // 处理手机号码输入
handlePhoneInput(e) {
  const phoneNumber_input = e.detail.value;
  const phoneNumberRegex = /^1[3-9]\d{9}$/; // 中国手机号码的正则表达式
  
  const isValid = phoneNumberRegex.test(phoneNumber_input);
  
  this.setData({
    phoneNumber_input: phoneNumber_input,
    phoneNumberValid: isValid
  });
},  

async phoneSave(){
  const phoneNumber_input = this.data.phoneNumber_input;
  const phoneNumberValid = this.data.phoneNumberValid;
  const token = this.store.token; // 从 store 中获取 token
  // 发送更新请求到后端
  if(phoneNumberValid){
  try {
    const response = await new Promise((resolve, reject) => {
        wx.request({
            url: 'https://bass-epic-mentally.ngrok-free.app/update-phone/',
            method: 'POST',
            header: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            data: {
              phoneNumber: phoneNumber_input,
            },
            success: (res) => {
                resolve(res); // 请求成功，返回响应
            },
            fail: (err) => {
                reject(err); // 请求失败，返回错误
            }
        });
    });
      
if (response.statusCode === 200) {
  wx.showToast({ title: '信息已保存', icon: 'success' });
  this.setData({
    phoneNumber: phoneNumber_input,
    isphoneVisible: false,
  });
  // 更新缓存
  wx.setStorageSync('phoneNumber', phoneNumber_input);
} else {
  wx.showToast({ title: '保存失败', icon: 'none' });
}
} catch (error) {
console.error('Request failed:', error);
wx.showToast({ title: '网络错误', icon: 'none' });
  }
}
},

// 新增常用保存
async handleSave() {
      this.setData({
        isFormValid: false,
      });
      const { currentName, currentIdCard, frequent_visitors, selectedIdTypeIndex} = this.data;
      const token = this.store.token; // 从 store 中获取 token
      if (!currentName || !currentIdCard) {
        wx.showToast({
          title: '请填写完整信息',
          icon: 'none'
        });
        return;
      }
        // 发送更新请求到后端
            try {
              const response = await new Promise((resolve, reject) => {
                  wx.request({
                      url: 'https://bass-epic-mentally.ngrok-free.app/add-visitor/',
                      method: 'POST',
                      header: {
                          'Content-Type': 'application/json',
                          'Authorization': `Bearer ${token}`
                      },
                      data: {
                          name: currentName,
                          idCard: currentIdCard,
                          selectedIdTypeIndex: selectedIdTypeIndex,
                      },
                      success: (res) => {
                          resolve(res); // 请求成功，返回响应
                      },
                      fail: (err) => {
                          reject(err); // 请求失败，返回错误
                      }
                  });
              });
                
          if (response.statusCode === 200) {
            const currentIndex = response.data.index;
            if (currentIndex!= 0) {
              this.setData({
                [`frequent_visitors.name_${currentIndex}`]: currentName,
                [`frequent_visitors.id_card_${currentIndex}`]: currentIdCard,
                selectedIdTypeIndex: 0,
            });
              wx.showToast({ title: '信息已保存', icon: 'success' });
            }
            else{
              wx.showToast({ title: '最多添加5位', icon: 'none' });
            }
            this.setData({
              currentName: '',
              currentIdCard: '',
              isPopupVisible: false,
              frequent_visitors: frequent_visitors // 更新
            });
            wx.setStorageSync('frequent_visitors', this.data.frequent_visitors);
        } else {
            wx.showToast({ title: '保存失败', icon: 'none' });
        }
    } catch (error) {
        console.error('Request failed:', error);
        wx.showToast({ title: '网络错误', icon: 'none' });
    }
  },
    

// 修改常用观众
async Rectify() {
      const { currentName, currentIdCard, currentIndex, frequent_visitors, selectedIdTypeIndex} = this.data;
      const token = this.store.token; // 从 store 中获取 token
  
      // 发送更新请求到后端
      try {
          const response = await new Promise((resolve, reject) => {
              wx.request({
                  url: 'https://bass-epic-mentally.ngrok-free.app/update-visitor/',
                  method: 'POST',
                  header: {
                      'Content-Type': 'application/json',
                      'Authorization': `Bearer ${token}`
                  },
                  data: {
                      name: currentName,
                      idCard: currentIdCard,
                      index: currentIndex,
                      selectedIdTypeIndex: selectedIdTypeIndex,
                  },
                  success: (res) => {
                      resolve(res); // 请求成功，返回响应
                  },
                  fail: (err) => {
                      reject(err); // 请求失败，返回错误
                  }
              });
          });
  
          if (response.statusCode === 200) {
              wx.showToast({ title: '信息已保存', icon: 'success' });
              this.setData({
                  [`frequent_visitors.name_${currentIndex}`]: currentName,
                  [`frequent_visitors.id_card_${currentIndex}`]: currentIdCard,
                  [`frequent_visitors.id_type_${currentIndex}`]: selectedIdTypeIndex,
                  isRectifyVisible: false,
              });
              wx.setStorageSync('frequent_visitors', this.data.frequent_visitors);
          } else {
              wx.showToast({ title: '保存失败', icon: 'none' });
          }
      } catch (error) {
          console.error('Request failed:', error);
          wx.showToast({ title: '网络错误', icon: 'none' });
      }
  },


// 删除常用观众
  async handleDelete() {
    const {currentIndex, selectedIdTypeIndex} = this.data;
    const token = this.store.token; // 从 store 中获取 token

    // 发送更新请求到后端
    try {
        const response = await new Promise((resolve, reject) => {
            wx.request({
                url: 'https://bass-epic-mentally.ngrok-free.app/delete-visitor/',
                method: 'POST',
                header: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                data: {
                    index: currentIndex,
                    selectedIdTypeIndex: selectedIdTypeIndex,
                },
                success: (res) => {
                    resolve(res); // 请求成功，返回响应
                },
                fail: (err) => {
                    reject(err); // 请求失败，返回错误
                }
            });
        });
        if (response.statusCode === 200) {
          const frequent_visitors = response.data.frequent_visitors[0];
          this.setData({
            isRectifyVisible: false,
            frequent_visitors: frequent_visitors, // 更新
            currentIdCard: '',
            currentName: '',
            selectedIdTypeIndex: 0,
        });
            wx.showToast({ title: '已成功删除', icon: 'success' });
            wx.setStorageSync('frequent_visitors', this.data.frequent_visitors);
        } else {
            wx.showToast({ title: '删除失败', icon: 'none' });
        }
    } catch (error) {
        console.error('Request failed:', error);
        wx.showToast({ title: '网络错误', icon: 'none' });
    }
},
})
