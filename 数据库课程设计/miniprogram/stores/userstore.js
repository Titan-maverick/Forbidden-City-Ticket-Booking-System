// observable 创建被监测的对象，对象中的属性会被转换为响应式数据
// action 函数用来显式的定义 action 方法
import { observable, action } from 'mobx-miniprogram'
import { getStorage } from '../utils/storage'

export const userStore = observable({
  // 定义响应式数据

  // token 身份令牌
  token: getStorage('token') || '',

  // 用户信息
  userInfo: getStorage('userInfo') || {},

  // 定义 action
  // setToken 用来修改、更新 token
  setToken: action(function (token) {
    // 在调用 setToken 方法时，需要传入 token 数据进行赋值
    this.token = token
  }),
})
