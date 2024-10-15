// 导入模块、包提供的类
import WxRequest from 'mina-request'
// 导入封装的本地存储操作模块
import { getStorage, clearStorage } from './storage'
// 导入封装的增强 API
import { toast, modal } from './extendApi'

// 对类进行实例化
const instance = new WxRequest({
  baseURL: 'https://gmall-prod.atguigu.cn/mall-api',
  timeout: 15000
})

// 添加请求拦截器 (在请求发送之前对请求参数进行新增或者修改)
instance.interceptors.request = (config) => {
  // 在实际开发中，有一些接口需要使用访问令牌 token
  // 访问令牌 token 通常是存储到本地
  // 需要先从本地获取到存储的 token
  const token = getStorage('token')

  // 如果本地存在 token，这时候就需要在请求头中添加 token 字段
  if (token) {
    config.header['token'] = token
  }

  // 在发送请求之前做些什么
  return config
}

// 添加响应拦截器 (在服务器响应数据以后，对返回的数据进行逻辑处理)
instance.interceptors.response = async (response) => {
  // 从 response 对象中解构两个数据
  const { isSuccess, data } = response

  // response 服务器响应的数据，只不过数据被 wx.request 进行了一层包装
  // console.log(response)

  // response.config 封装的包里面提供的 config 属性，是请求的参数信息
  // 可以使用请求参数进行代码的调试

  // response.data 服务器真正响应的数据

  // response.isSuccess 判断代码执行了哪一个回调函数
  // isSuccess = true，说明代码执行了 wx.request 方法的 success 回调函数
  // isSuccess = false，说明代码执行了 wx.request 方法的 fail 回调函数

  // 如果 isSuccess = false，说明网络出现了问题
  if (!isSuccess) {
    toast({
      title: '网络异常请重试',
      icon: 'error'
    })

    return Promise.reject(response)
  }

  // 如果 isSuccess = true，说明代码执行到了 success 回调函数
  // 需要开发者对返回的参数进行逻辑判断
  // 需要对后端返回的业务状态码进行判断
  // 业务状态码 === 200，接口调用成功，服务器成功返回了数据
  // 业务状态码 === 208，没有 token 或者 token 失效，需要让用户重新进行登录
  // 业务状态码既不等于 200，也不等于 208，说明出现了其他异常，需要给用户统一进行提示
  switch (data.code) {
    case 200:
      // 接口调用成功，服务器成功返回了数据，只需要将数据简化以后返回即可
      return data

    case 208:
      const res = await modal({
        content: '鉴权失败，请重新登录',
        showCancel: false
      })

      if (res) {
        // 既然用户需要重新进行登录，就需要把之前用户存储的信息(过期的 token) 进行清除
        clearStorage()

        wx.navigateTo({
          url: '/pages/login/login'
        })
      }

      return Promise.reject(response)

    default:
      toast({
        title: '程序出现异常，请联系客服或稍后重试！'
      })
      return Promise.reject(response)
  }

  // return response
}

// 导出实例
export default instance
