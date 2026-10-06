const TokenKey = 'token'
const RefreshTokenKey = 'refresh_token'
const UserKey = 'userInfo'
// 兼容旧版键名（登录信息曾存于 'user'），一次改名后旧会话仍能读到角色
const LegacyUserKey = 'user'

// 读取时优先 sessionStorage（本次会话），再回落到 localStorage（勾选“记住我”的持久化）
function readStorage(key) {
  return sessionStorage.getItem(key) || localStorage.getItem(key)
}

// 按“是否记住我”选择写入的存储域：
//   remember===true  -> localStorage（持久化）
//   remember===false -> sessionStorage（关闭浏览器即清除）
//   remember 未传     -> 沿用该 key 已存在的存储域（刷新 token 时不改变登录方式），全新则默认 localStorage
// 写入前会清除另一存储域的同 key 旧值，避免跨域残留导致读到过期 session
function writeStorage(key, value, remember) {
  const sessionHas = sessionStorage.getItem(key) !== null
  const localHas = localStorage.getItem(key) !== null
  let target
  if (remember === true) {
    target = localStorage
  } else if (remember === false) {
    target = sessionStorage
  } else {
    target = sessionHas ? sessionStorage : localHas ? localStorage : localStorage
  }
  // 清除非目标域的同 key，再写入
  const other = target === localStorage ? sessionStorage : localStorage
  other.removeItem(key)
  return target.setItem(key, value)
}

function removeStorage(key) {
  sessionStorage.removeItem(key)
  localStorage.removeItem(key)
}

export function getToken() {
  return readStorage(TokenKey)
}

export function setToken(token, remember) {
  return writeStorage(TokenKey, token, remember)
}

export function removeToken() {
  removeStorage(TokenKey)
}

export function getRefreshToken() {
  return readStorage(RefreshTokenKey)
}

export function setRefreshToken(token, remember) {
  return writeStorage(RefreshTokenKey, token, remember)
}

export function removeRefreshToken() {
  removeStorage(RefreshTokenKey)
}

export function clearAuth() {
  ;[TokenKey, RefreshTokenKey, UserKey, LegacyUserKey].forEach(removeStorage)
}

export function getUserInfo() {
  let info = readStorage(UserKey)
  if (!info) info = readStorage(LegacyUserKey)
  return info ? JSON.parse(info) : null
}

export function setUserInfo(info, remember) {
  return writeStorage(UserKey, JSON.stringify(info), remember)
}

export function removeUserInfo() {
  removeStorage(UserKey)
  removeStorage(LegacyUserKey)
}