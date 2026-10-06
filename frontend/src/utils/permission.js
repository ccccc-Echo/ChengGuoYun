import { getUserInfo } from './auth'

const permissions = {
  hasPermission(code) {
    const userInfo = getUserInfo()
    if (!userInfo) return false
    
    if (userInfo.role === 'admin') {
      return true
    }
    
    const teacherPermissions = userInfo.permissions || []
    return teacherPermissions.includes(code)
  },

  hasAnyPermission(codes) {
    if (!Array.isArray(codes)) {
      return this.hasPermission(codes)
    }
    return codes.some(code => this.hasPermission(code))
  },

  setPermissions(permList) {
    const userInfo = getUserInfo()
    if (userInfo) {
      userInfo.permissions = permList
      localStorage.setItem('user', JSON.stringify(userInfo))
    }
  }
}

export default permissions