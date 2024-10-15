// 执行 extendApi.js 文件，将方法挂载到 wx 全局对象身上
import './utils/extendApi'

App({
  // globalData 是指全局共享的数据
  globalData: {
  },

  onShow() {
    // 获取当前小程序的账号信息
    // const accountInfo = wx.getAccountInfoSync()
    // 通过小程序的账号信息，就能获取小程序版本
    // console.log(accountInfo.miniProgram.envVersion)
  }
})
