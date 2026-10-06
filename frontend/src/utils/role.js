// 角色码归一化：兼容 teachers.role 里存的「中文角色」与「角色码」两种形态
const ROLE_ALIAS = {
  '系统管理员': 'admin',
  '院系负责人': 'head',
  '辅导员': 'advisor',
  '教务管理员': 'teaching_admin',
  '教师': 'faculty',
  '学生': 'student'
}

const ROLE_CODE_TO_NAME = {
  admin: '系统管理员',
  head: '院系负责人',
  advisor: '辅导员',
  faculty: '教师',
  teaching_admin: '教务管理员',
  teacher: '教师',
  student: '学生'
}

// 把任意角色值（中文名或角色码）统一为角色码；无法识别的原样返回
export function normalizeRole(role) {
  if (!role) return role
  return ROLE_ALIAS[role] || role
}

// 角色码 -> 中文显示名，便于自定义场景直接取展示名
export function roleCodeToName(role) {
  const code = normalizeRole(role)
  return ROLE_CODE_TO_NAME[code] || code || '未知'
}