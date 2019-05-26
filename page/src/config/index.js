import axios from 'axios'

import router from '../router'

let host = 'http://127.0.0.1:5000'

// http request 拦截器
axios.interceptors.request.use(
  config => {
    config.baseURL = host
    return config
  },
  err => {
    return Promise.reject(err)
  })

// http response 拦截器
axios.interceptors.response.use(
  undefined,
  error => {
    let res = error.response
    switch (res.status) {
      case 401:
        // 返回 401 清除token信息并跳转到登录页面
        // store.commit(types.LOGOUT);
        router.replace({
          path: '/console/home/login',
          query: {
            redirect: router.currentRoute.fullPath
          }
        })
        break
      case 403:
        console.log('您没有该操作权限')
        break
      case 500:
        console.log('服务器错误')
        break
    }
    return Promise.reject(error.response.data) // 返回接口返回的错误信息
  })
