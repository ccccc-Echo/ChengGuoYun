import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { getToken, getRefreshToken, setToken, clearAuth } from '@/utils/auth'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 单独实例用于刷新 token，避免与业务拦截器互相触发
const refreshAxios = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 单飞：并发 401 只发起一次刷新，全部请求复用同一个 refresh Promise
let refreshPromise = null

// 登出去重：同一会话的多个并发 401 只弹一次提示、只跳一次登录
let loggedOut = false
let logoutTimer = null
function handleForceLogout() {
  if (loggedOut) return
  loggedOut = true
  clearAuth()
  ElMessage.error('登录已过期，请重新登录')
  router.replace('/login')
  clearTimeout(logoutTimer)
  logoutTimer = setTimeout(() => { loggedOut = false }, 5000)
}

function refreshAccessToken() {
  const refreshToken = getRefreshToken()
  if (!refreshToken) return Promise.reject(new Error('no refresh_token'))
  return refreshAxios.post('/auth/refresh', { refresh_token: refreshToken }).then(res => res.data.access_token)
}

// 返回单飞后的刷新 Promise；成功时返回新 token，失败时 rejection 给所有调用方
function ensureRefreshed() {
  if (!refreshPromise) {
    refreshPromise = refreshAccessToken()
      .then(newToken => {
        setToken(newToken)
        return newToken
      })
      .finally(() => {
        refreshPromise = null
      })
  }
  return refreshPromise
}

service.interceptors.request.use(
  config => {
    const token = getToken()
    console.log('=== 请求拦截器 ===')
    console.log('token:', token ? token.substring(0, 20) + '...' : null)
    console.log('请求URL:', config.url)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('Authorization头已添加')
    } else {
      console.log('未找到token')
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    return response.data
  },
  async error => {
    if (error.response) {
      const status = error.response.status
      // 登录接口的错误由登录页自行按状态码提示（避免密码错误/用户名不存在被误判为“登录已过期”）
      const isLogin = error.config?.url?.includes('/auth/login')
      if (isLogin) {
        return Promise.reject(error)
      }
      if (status === 401) {
        // 登录接口自身的 401（密码错误/锁定）由登录页自行提示，不触发刷新
        if (error.config?.url?.includes('/auth/login')) {
          return Promise.reject(error)
        }
        // 已重试过仍 401 → access 与 refresh 均失效，统一登出（去重，只提示/跳转一次）
        if (error.config._retry) {
          handleForceLogout()
          return Promise.reject(error)
        }
        error.config._retry = true
        try {
          const newToken = await ensureRefreshed()
          error.config.headers.Authorization = `Bearer ${newToken}`
          return service(error.config)
        } catch (refreshError) {
          handleForceLogout()
          return Promise.reject(refreshError)
        }
      }
      let data = error.response.data
      // 文件下载（blob）接口的错误响应也是 Blob，需读取真实 JSON 错误信息
      if (data instanceof Blob) {
        try {
          const text = await data.text()
          data = JSON.parse(text)
        } catch (e) {
          data = null
        }
      }
      // 优先使用后端返回的统一 message，缺失时按状态码给默认提示
      const backendMsg = data?.message || data?.error
      const statusMsgMap = {
        400: '请求参数错误',
        403: '无权限访问',
        404: '请求的资源不存在',
        422: '请求参数错误',
        500: '服务器内部错误，请稍后重试'
      }
      // 500/404/422 属“需统一提示”的场景，优先用固定友好文案；
      // 其余状态优先采用后端返回的具体信息（如“用户名已存在”）
      const preferFixed = [500, 404, 422].includes(status)
      const message = preferFixed
        ? (statusMsgMap[status] || backendMsg || '操作失败')
        : (backendMsg || statusMsgMap[status] || '操作失败')
      ElMessage({
        message: message,
        type: 'error',
        duration: 3000
      })
    } else {
      ElMessage({
        message: error.message || '网络错误',
        type: 'error',
        duration: 3000
      })
    }
    return Promise.reject(error)
  }
)

export default service