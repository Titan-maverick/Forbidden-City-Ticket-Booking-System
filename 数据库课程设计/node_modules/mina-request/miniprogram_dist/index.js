class WxRequest {
  // 定义实例属性，用来设置默认请求参数
  defaults = {
    baseURL: '', // 请求基准地址
    url: '', // 接口的请求路径
    data: null, // 请求参数
    method: 'GET', // 默认的请求方法
    // 请求头
    header: {
      'Content-type': 'application/json' // 设置数据的交互格式
    },
    timeout: 60000, // 默认的超时时长，小程序默认的超时时长是 1 分钟
    isLoading: true // 控制是否使用默认的 loading，默认值是 true 表示使用默认的 loading
  }

  // 定义拦截器对象
  interceptors = {
    // 请求拦截器
    request: (config) => config,

    // 响应拦截器
    response: (response) => response
  }

  // 定义数组队列，用来存储请求队列、存储请求标识
  queue = []

  // constructor 用于创建和初始化类的属性以及方法
  constructor(params = {}) {
    // 注意：需要传入的参数，覆盖默认的参数，因此传入的参数需要放到最后
    this.defaults = Object.assign({}, this.defaults, params)
  }

  /**
   * @description request 实例方法发送网络请求，接收一个对象类型的参数
   * @param {*} options 属性值和 wx.request() 方法调用时传递的参数保持一致
   * @returns Promise
   */
  request(options) {
    // 如果有新的请求，就清除上一次的定时器
    this.timerId && clearTimeout(this.timerId)

    // 合并完整的请求地址
    options.url = this.defaults.baseURL + options.url

    // 合并请求参数：调用实例方法时传入的覆盖默认的以及实例配置的
    options = { ...this.defaults, ...options }

    // 控制 loading 的显示与隐藏
    if (options.isLoading && options.method !== 'UPLOAD') {
      this.queue.length === 0 && wx.showLoading()
      this.queue.push('request')
    }

    // 在请求发送之前，调用请求拦截器，新增和修改请求参数
    // 请求拦截器内部，会将新增和修改以后的参数返回
    options = this.interceptors.request(options)

    // 需要使用 Promise 封装 wx.request，处理异步请求
    return new Promise((resolve, reject) => {
      // 如果 method 等于 UPLOAD 说明需要调用 wx.uploadFile() 方法
      // 否则调用的是 wx.request() 方法
      if (options.method === 'UPLOAD') {
        wx.uploadFile({
          ...options,

          success: (res) => {
            // 需要将服务器返回的 JSON 字符串 通过 JSON.parse 转成对象
            res.data = JSON.parse(res.data)

            // 合并参数
            const mergeRes = Object.assign({}, res, {
              config: options,
              isSuccess: true
            })

            resolve(this.interceptors.response(mergeRes))
          },

          fail: (err) => {
            // 合并参数
            const mergeErr = Object.assign({}, err, {
              config: options,
              isSuccess: false
            })

            reject(this.interceptors.response(mergeErr))
          }
        })
      } else {
        wx.request({
          ...options,

          // 当接口调用成功时会触发 success 回调函数
          success: (res) => {
            // 合并请求参数，方便进行代码调试
            // 追加 isSuccess 属性，是为了标识响应拦截器是 success 调用还是 fail 调用
            const mergeRes = Object.assign({}, res, {
              config: options,
              isSuccess: true
            })
            resolve(this.interceptors.response(mergeRes))
          },

          // 当接口调用失败时会触发 fail 回调函数
          fail: (err) => {
            // 合并请求参数，方便进行代码调试
            // 追加 isSuccess 属性，是为了标识响应拦截器是 success 调用还是 fail 调用
            const mergeErr = Object.assign({}, err, {
              config: options,
              isSuccess: false
            })
            reject(this.interceptors.response(mergeErr))
          },

          // 接口调用结束的回调函数（调用成功、失败都会执行）
          complete: () => {
            // 如果需要显示 loading ，那么就需要控制 loading 的隐藏
            if (options.isLoading) {
              // 在每一个请求结束以后，都会执行 complete 回调函数
              // 每次从 queue 队列中删除一个标识
              this.queue.pop()

              // 解决并发请求，loading 闪烁问题
              this.queue.length === 0 && this.queue.push('request')

              //解决并发请求，loading 闪烁问题
              this.timerId = setTimeout(() => {
                this.queue.pop()

                this.queue.length === 0 && wx.hideLoading()

                clearTimeout(this.timerId)
              }, 1)
            }
          }
        })
      }
    })
  }

  /**
   * @description 封装 GET 实例方法
   * @param {*} url 请求地址
   * @param {*} data 请求参数
   * @param {*} config 其他请求配置项
   * @returns Promise
   */
  get(url, data = {}, config = {}) {
    // 需要调用 request 请求方法发送请求，只需要组织好参数，传递给 request 请求方法即可
    // 当调用 get 方法时，需要将 request 方法的返回值 return 出去
    return this.request(Object.assign({ url, data, method: 'GET' }, config))
  }

  /**
   * @description 封装 DELETE 实例方法
   * @param {*} url 请求地址
   * @param {*} data 请求参数
   * @param {*} config 其他请求配置项
   * @returns Promise
   */
  delete(url, data = {}, config = {}) {
    return this.request(Object.assign({ url, data, method: 'DELETE' }, config))
  }

  /**
   * @description 封装 POST 实例方法
   * @param {*} url 请求地址
   * @param {*} data 请求参数
   * @param {*} config 其他请求配置项
   * @returns Promise
   */
  post(url, data = {}, config = {}) {
    return this.request(Object.assign({ url, data, method: 'POST' }, config))
  }

  /**
   * @description 封封装 PUT 实例方法
   * @param {*} url 请求地址
   * @param {*} data 请求参数
   * @param {*} config 其他请求配置项
   * @returns Promise
   */
  put(url, data = {}, config = {}) {
    return this.request(Object.assign({ url, data, method: 'PUT' }, config))
  }

  /**
   * @description 处理并发请求
   * @param  {...promise} promise 传入的每一项需要是 Promise
   * @returns Promise
   */
  all(...promise) {
    // 那么展开运算符会将传入的参数转成数组
    return Promise.all(promise)
  }

  /**
   * @description upload 实例方法，用来对 wx.uploadFile 进行封装
   * @param {*} url 文件的上传地址、接口地址
   * @param {*} filePath 要上传的文件资源路径
   * @param {*} name 文件对应的 key
   * @param {*} config 其他配置项
   */
  upload(url, filePath, name = 'file', config = {}) {
    return this.request(
      Object.assign({ url, filePath, name, method: 'UPLOAD' }, config)
    )
  }
}

export default WxRequest
