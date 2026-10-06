import request from '@/utils/request'

export const authApi = {
  login(data) {
    return request({
      url: '/auth/login/',
      method: 'post',
      data
    })
  },
  getMe() {
    return request({
      url: '/auth/me/',
      method: 'get'
    })
  },
  register(data) {
    return request({
      url: '/auth/register/',
      method: 'post',
      data
    })
  },
  normalRegister(data) {
    return request({
      url: '/register/normal',
      method: 'post',
      data
    })
  },
  phoneRegister(data) {
    return request({
      url: '/register/phone',
      method: 'post',
      data
    })
  },
  checkUsername(username) {
    return request({
      url: '/check/username',
      method: 'get',
      params: { username }
    })
  },
  sendSms(data) {
    return request({
      url: '/sms/send',
      method: 'post',
      data
    })
  },
  getProfile() {
    return request({
      url: '/auth/profile/',
      method: 'get'
    })
  },
  updateProfile(data) {
    return request({
      url: '/auth/profile/',
      method: 'put',
      data
    })
  },
  changePassword(data) {
    return request({
      url: '/auth/change-password/',
      method: 'post',
      data
    })
  },
  getTeachers(params) {
    return request({
      url: '/auth/teachers/',
      method: 'get',
      params
    })
  }
}

export const achievementsApi = {
  list(params) {
    return request({
      url: '/achievements/',
      method: 'get',
      params
    })
  },
  create(data) {
    return request({
      url: '/achievements/',
      method: 'post',
      data
    })
  },
  get(id) {
    return request({
      url: `/achievements/${id}`,
      method: 'get'
    })
  },
  update(id, data) {
    return request({
      url: `/achievements/${id}`,
      method: 'put',
      data
    })
  },
  audit(id, data) {
    return request({
      url: `/achievements/${id}/audit`,
      method: 'put',
      data
    })
  },
  delete(id) {
    return request({
      url: `/achievements/${id}`,
      method: 'delete'
    })
  },
  getReviewers() {
    return request({
      url: '/achievements/reviewers',
      method: 'get'
    })
  },
  getTeachers() {
    return request({
      url: '/achievements/teachers',
      method: 'get'
    })
  }
}

export const statsApi = {
  dashboard() {
    return request({
      url: '/stats/dashboard/',
      method: 'get'
    })
  },
  classStats(params) {
    return request({
      url: '/stats/class/',
      method: 'get',
      params
    })
  },
  schoolStats() {
    return request({
      url: '/stats/school/',
      method: 'get'
    })
  },
  screenStats() {
    return request({
      url: '/stats/screen/',
      method: 'get'
    })
  },
  trendStats(params) {
    return request({
      url: '/stats/trend/',
      method: 'get',
      params
    })
  }
}

export const studentsApi = {
  list(params) {
    return request({
      url: '/students/',
      method: 'get',
      params
    })
  },
  create(data) {
    return request({
      url: '/students/',
      method: 'post',
      data
    })
  },
  get(id) {
    return request({
      url: `/students/${id}`,
      method: 'get'
    })
  },
  update(id, data) {
    return request({
      url: `/students/${id}`,
      method: 'put',
      data
    })
  },
  delete(id) {
    return request({
      url: `/students/${id}`,
      method: 'delete'
    })
  },
  resetPassword(id, data) {
    return request({
      url: `/students/${id}/reset-password`,
      method: 'put',
      data
    })
  }
}

export const coursesApi = {
  list(params) {
    return request({
      url: '/courses/',
      method: 'get',
      params
    })
  },
  create(data) {
    return request({
      url: '/courses/',
      method: 'post',
      data
    })
  },
  get(id) {
    return request({
      url: `/courses/${id}`,
      method: 'get'
    })
  },
  update(id, data) {
    return request({
      url: `/courses/${id}`,
      method: 'put',
      data
    })
  },
  delete(id) {
    return request({
      url: `/courses/${id}`,
      method: 'delete'
    })
  },
  lock(id, data) {
    return request({
      url: `/courses/${id}/lock`,
      method: 'put',
      data
    })
  },
  my(params) {
    return request({
      url: '/courses/my',
      method: 'get',
      params
    })
  },
  available(params) {
    return request({
      url: '/courses/available',
      method: 'get',
      params
    })
  },
  students(id) {
    return request({
      url: `/courses/${id}/students`,
      method: 'get'
    })
  }
}

export const teacherApi = {
  statistics() {
    return request({
      url: '/teachers/statistics',
      method: 'get'
    })
  },
  list(params) {
    return request({
      url: '/teachers/',
      method: 'get',
      params
    })
  },
  create(data) {
    return request({
      url: '/teachers/',
      method: 'post',
      data
    })
  },
  get(id) {
    return request({
      url: `/teachers/${id}`,
      method: 'get'
    })
  },
  update(id, data) {
    return request({
      url: `/teachers/${id}`,
      method: 'put',
      data
    })
  },
  delete(id) {
    return request({
      url: `/teachers/${id}`,
      method: 'delete'
    })
  },
  approve(id) {
    return request({
      url: `/teachers/${id}/approve`,
      method: 'put'
    })
  },
  unlock(id) {
    return request({
      url: `/teachers/${id}/unlock`,
      method: 'put'
    })
  }
}

export const permissionApi = {
  getRoles() {
    return request({
      url: '/roles/',
      method: 'get'
    })
  },
  createRole(data) {
    return request({
      url: '/roles/',
      method: 'post',
      data
    })
  },
  deleteRole(id) {
    return request({
      url: `/roles/${id}`,
      method: 'delete'
    })
  },
  getPermissions(id) {
    return request({
      url: `/roles/${id}/permissions`,
      method: 'get'
    })
  },
  updatePermissions(id, data) {
    return request({
      url: `/roles/${id}/permissions`,
      method: 'put',
      data
    })
  },
  getAllPermissions() {
    return request({
      url: '/roles/permissions/all',
      method: 'get'
    })
  }
}

export const teamApi = {
  list(params) {
    return request({
      url: '/teams/',
      method: 'get',
      params
    })
  },
  create(data) {
    return request({
      url: '/teams/',
      method: 'post',
      data
    })
  },
  delete(id) {
    return request({
      url: `/teams/${id}`,
      method: 'delete'
    })
  },
  getMembers(id) {
    return request({
      url: `/teams/${id}/members`,
      method: 'get'
    })
  },
  removeMember(teamId, memberId) {
    return request({
      url: `/teams/${teamId}/members/${memberId}`,
      method: 'delete'
    })
  },
  join(data) {
    return request({
      url: '/teams/join',
      method: 'post',
      data
    })
  },
  leave(id) {
    return request({
      url: `/teams/${id}/leave`,
      method: 'post'
    })
  }
}

export const knowledgeBaseApi = {
  list(params) {
    return request({
      url: '/knowledge-base/',
      method: 'get',
      params
    })
  },
  get(id) {
    return request({
      url: `/knowledge-base/${id}`,
      method: 'get'
    })
  },
  update(id, data) {
    return request({
      url: `/knowledge-base/${id}`,
      method: 'put',
      data
    })
  },
  delete(id) {
    return request({
      url: `/knowledge-base/${id}`,
      method: 'delete'
    })
  },
  export(ids) {
    return request({
      url: '/knowledge-base/export',
      method: 'post',
      data: ids && ids.length ? { id: ids } : {},
      responseType: 'blob',
      timeout: 120000
    })
  },
  exportOne(id) {
    return request({
      url: `/knowledge-base/export/${id}`,
      method: 'get',
      responseType: 'blob',
      timeout: 120000
    })
  }
}

export const settingsApi = {
  listCategories(params) {
    return request({
      url: '/settings/categories/',
      method: 'get',
      params
    })
  },
  createCategory(data) {
    return request({
      url: '/settings/categories/',
      method: 'post',
      data
    })
  },
  updateCategory(id, data) {
    return request({
      url: `/settings/categories/${id}`,
      method: 'put',
      data
    })
  },
  deleteCategory(id) {
    return request({
      url: `/settings/categories/${id}`,
      method: 'delete'
    })
  },
  listKnowledge(params) {
    return request({
      url: '/settings/knowledge/',
      method: 'get',
      params
    })
  },
  createKnowledge(data) {
    return request({
      url: '/settings/knowledge/',
      method: 'post',
      data
    })
  },
  updateKnowledge(id, data) {
    return request({
      url: `/settings/knowledge/${id}`,
      method: 'put',
      data
    })
  },
  deleteKnowledge(id) {
    return request({
      url: `/settings/knowledge/${id}`,
      method: 'delete'
    })
  }
}

export const exportApi = {
  // 导出获奖证书汇总 PDF（返回二进制流）
  certificates(data) {
    return request({
      url: '/student/export/certificates',
      method: 'post',
      data,
      responseType: 'blob'
    })
  }
}

// 教师端：导出所带学生的获奖证书汇总
export const teacherExportApi = {
  // 奖项类型一级分类（含中文名与存储码）
  listAwardTypes() {
    return request({
      url: '/teacher/export/award-types',
      method: 'get'
    })
  },
  // 列出教师所带班级的全部学生（支持按审核时间/分类/级别/学号筛选）
  listStudents(params) {
    return request({
      url: '/teacher/export/students',
      method: 'get',
      params
    })
  },
  // 导出指定学生的全部获奖证书汇总 PDF（返回二进制流）
  exportStudentCertificates(studentId) {
    return request({
      url: '/teacher/export/student/certificates',
      method: 'post',
      data: { student_id: studentId },
      responseType: 'blob'
    })
  },
  // 列出指定学生的全部已通过成果（供单项导出弹窗）
  listStudentAchievements(studentId) {
    return request({
      url: `/teacher/export/student/${studentId}/achievements`,
      method: 'get'
    })
  },
  // 导出指定学生的单条成果 PDF（返回二进制流）
  exportStudentAchievement(achievementId) {
    return request({
      url: '/teacher/export/student/achievement',
      method: 'post',
      data: { achievement_id: achievementId },
      responseType: 'blob'
    })
  }
}

// 系统日志
export const logsApi = {
  // 分页查询系统日志，支持日期范围 / 操作类型 / 用户筛选
  list(params) {
    return request({
      url: '/logs/',
      method: 'get',
      params
    })
  }
}

// 数据备份
export const backupApi = {
  // 获取备份列表
  list() {
    return request({
      url: '/backup/list',
      method: 'get'
    })
  },
  // 手动触发备份（可指定日期，用于测试 30 天清理）
  create(data) {
    return request({
      url: '/backup/create',
      method: 'post',
      data
    })
  },
  // 下载备份文件（返回二进制流）
  download(filename) {
    return request({
      url: `/backup/download/${encodeURIComponent(filename)}`,
      method: 'get',
      responseType: 'blob'
    })
  },
  // 删除备份文件
  delete(filename) {
    return request({
      url: `/backup/delete/${encodeURIComponent(filename)}`,
      method: 'delete'
    })
  }
}

// 站内信通知
export const notificationApi = {
  // 获取当前用户消息列表
  list(params) {
    return request({
      url: '/notifications/',
      method: 'get',
      params
    })
  },
  // 获取未读消息数量
  unreadCount() {
    return request({
      url: '/notifications/unread-count',
      method: 'get'
    })
  },
  // 标记单条已读
  markRead(id) {
    return request({
      url: `/notifications/${id}/read`,
      method: 'put'
    })
  },
  // 全部标记已读
  readAll() {
    return request({
      url: '/notifications/read-all',
      method: 'put'
    })
  }
}

// 竞赛信息（第二课堂）
export const competitionApi = {
  // 获取竞赛列表（支持 month/category/keyword 筛选）
  list(params) {
    return request({
      url: '/competitions',
      method: 'get',
      params
    })
  },
  // 获取竞赛分类列表
  categories() {
    return request({
      url: '/competitions/categories',
      method: 'get'
    })
  },
  // 广告牌推荐（随机）
  recommend() {
    return request({
      url: '/competitions/recommend',
      method: 'get',
      params: { limit: 5 }
    })
  },
  // 热搜榜（按热度）
  hot() {
    return request({
      url: '/competitions/hot',
      method: 'get',
      params: { limit: 5 }
    })
  },
  // 收藏比赛（想参加）
  addFavorite(competitionId) {
    return request({
      url: `/competitions/favorites/${competitionId}`,
      method: 'post'
    })
  },
  // 取消收藏
  removeFavorite(competitionId) {
    return request({
      url: `/competitions/favorites/${competitionId}`,
      method: 'delete'
    })
  },
  // 我的比赛列表
  myFavorites() {
    return request({
      url: '/competitions/favorites',
      method: 'get'
    })
  }
}

// AI 简历生成
export const aiApi = {
  // 基于学生勾选的成果调用本地模型生成简历（推理耗时较长，单独放宽超时到 180s）
  resume({ achievement_ids, extra }) {
    return request({
      url: '/ai/resume',
      method: 'post',
      data: { achievement_ids, extra },
      timeout: 180000
    })
  },
  // 把已生成的简历导出为 Word 文档
  exportResume({ resume }) {
    return request({
      url: '/ai/resume/export',
      method: 'post',
      data: { resume },
      responseType: 'blob',
      timeout: 60000
    })
  }
}
