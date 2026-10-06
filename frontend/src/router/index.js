import { createRouter, createWebHistory } from 'vue-router'
import { getToken, getUserInfo } from '@/utils/auth'
import { normalizeRole } from '@/utils/role'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue')
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/forgot-password/index.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/register/index.vue'),
    redirect: '/register/identity',
    children: [
      {
        path: 'identity',
        name: 'RegisterIdentity',
        component: () => import('@/views/register/identity.vue')
      },
      {
        path: 'student',
        name: 'RegisterStudent',
        component: () => import('@/views/register/student.vue')
      },
      {
        path: 'teacher',
        name: 'RegisterTeacher',
        component: () => import('@/views/register/teacher.vue')
      }
    ]
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/layout/index.vue'),
    redirect: '/home/index',
    meta: { title: '首页' },
    children: [
      {
        path: 'index',
        name: 'HomeIndex',
        component: () => import('@/views/home/index.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'courses',
        name: 'JoinCourses',
        component: () => import('@/views/courses/JoinCourses.vue'),
        meta: { title: '加入课程' }
      },
    ]
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard/index',
    meta: { title: '仪表盘' },
    children: [
      {
        path: 'index',
        name: 'DashboardIndex',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', hidden: true }
      },
      {
        path: 'achievements',
        name: 'Achievements',
        component: () => import('@/views/achievements/index.vue'),
        meta: { title: '成果管理' }
      },
      {
        path: 'achievements/add',
        name: 'AchievementAdd',
        component: () => import('@/views/achievements/add.vue'),
        meta: { title: '录入成果' }
      },
      {
        path: 'classes',
        name: 'Classes',
        component: () => import('@/views/classes/index.vue'),
        meta: { title: '课程管理' }
      },
      {
        path: 'students',
        name: 'Students',
        component: () => import('@/views/students/index.vue'),
        meta: { title: '学生管理' }
      },
      {
        path: 'team-management',
        name: 'TeamManagement',
        component: () => import('@/views/teams/index.vue'),
        meta: { title: '团队管理' }
      },
      {
          path: 'teachers',
          name: 'Teachers',
          component: () => import('@/views/teacher/index.vue'),
          meta: { title: '教师管理', permission: 'teacher:add' }
        },
        {
          path: 'permission',
          name: 'Permission',
          component: () => import('@/views/permission/Permission.vue'),
          meta: { title: '权限管理' }
        },
        {
          path: 'stats',
          name: 'Stats',
          component: () => import('@/views/stats/index.vue'),
          meta: { title: '统计报表' }
        },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: { title: '系统设置' }
      },
      {
        path: 'logs',
        name: 'SystemLogs',
        component: () => import('@/views/settings/logs.vue'),
        meta: { title: '系统日志' }
      },
      {
        path: 'backup',
        name: 'DataBackup',
        component: () => import('@/views/settings/backup.vue'),
        meta: { title: '数据备份' }
      },
      {
          path: 'profile',
          name: 'Profile',
          component: () => import('@/views/teacher/profile/index.vue'),
          meta: { title: '个人中心' }
        },
        {
          path: 'courses',
          name: 'MyClasses',
          component: () => import('@/views/courses/MyClasses.vue'),
          meta: { title: '我的课程' }
        },
        {
          path: 'export',
          name: 'TeacherExport',
          component: () => import('@/views/teacher/export/index.vue'),
          meta: { title: '导出获奖证书' }
        },
        {
          path: 'courses/:id',
          name: 'CourseDetail',
          component: () => import('@/views/courses/CourseDetail.vue'),
          meta: { title: '课程详情' }
        }
      ]
  },
  {
    path: '/home/search',
    name: 'HomeSearch',
    component: () => import('@/views/search/index.vue'),
    meta: { title: '搜索结果' }
  },
  {
    path: '/home/detail/:id',
    name: 'HomeDetail',
    component: () => import('@/views/home/DetailPage.vue'),
    meta: { title: '成果详情' }
  },
  {
    path: '/student',
    name: 'Student',
    component: () => import('@/layouts/StudentLayout.vue'),
    redirect: '/student/home',
    meta: { title: '首页' },
    children: [
      {
        path: 'home',
        name: 'StudentHome',
        component: () => import('@/views/student/home/index.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'competitions',
        name: 'StudentCompetitions',
        component: () => import('@/views/student/competitions/index.vue'),
        meta: { title: '竞赛广场' }
      },
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/student/dashboard/index.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'achievement',
        name: 'StudentAchievement',
        component: () => import('@/views/student/achievement/index.vue'),
        meta: { title: '个人成果' }
      },
      {
        path: 'submit',
        name: 'StudentSubmit',
        component: () => import('@/views/student/submit/index.vue'),
        meta: { title: '录入成果' }
      },
      {
        path: 'courses',
        name: 'StudentCourses',
        component: () => import('@/views/student/courses/index.vue'),
        meta: { title: '加入课程' }
      },
      {
        path: 'center',
        name: 'StudentCenter',
        component: () => import('@/views/student/center/index.vue'),
        meta: { title: '个人中心' }
      },
      {
        path: 'export/certificates',
        name: 'StudentExportCertificates',
        component: () => import('@/views/student/export/Certificates.vue'),
        meta: { title: '导出获奖证书汇总' }
      }
    ]
  },
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = getToken()
  
  if (to.path === '/login' || to.path.startsWith('/register') || to.path === '/forgot-password') {
    if (token) {
      const userInfo = getUserInfo()
      if (userInfo?.role === 'student') {
        next('/student/dashboard')
      } else {
        next('/dashboard')
      }
    } else {
      next()
    }
  } else {
    if (!token) {
      next('/login')
    } else {
      const userInfo = getUserInfo()
      
      if (to.path.startsWith('/student')) {
        if (userInfo?.role !== 'student') {
          next('/dashboard')
          return
        }
      }
      
      if (userInfo?.role === 'student' && to.path.startsWith('/dashboard')) {
        const pathMap = {
          '/dashboard': '/student/dashboard',
          '/dashboard/index': '/student/dashboard',
          '/dashboard/achievements': '/student/achievement',
          '/dashboard/achievements/add': '/student/submit',
          '/dashboard/profile': '/student/center',
          '/home': '/student/dashboard',
          '/home/index': '/student/dashboard',
          '/home/courses': '/student/courses'
        }
        const redirectPath = pathMap[to.path]
        if (redirectPath) {
          next(redirectPath)
          return
        }
      }
      
      if (to.path.startsWith('/home')) {
        if (userInfo?.role !== 'student') {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/home/search') {
        if (userInfo?.role !== 'student') {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/teachers') {
        const role = userInfo?.role === 'teacher' ? userInfo?.teacher_role : userInfo?.role
        const hasPermission = userInfo?.permissions?.includes('teacher:add') || userInfo?.permissions?.includes('teacher:edit')
        if (!['admin', 'head'].includes(role) && !hasPermission) {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/settings' || to.path === '/dashboard/logs' || to.path === '/dashboard/backup') {
        if (userInfo?.role !== 'admin') {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/permission') {
        if (userInfo?.role !== 'admin') {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/classes') {
        const role = userInfo?.role === 'teacher' ? userInfo?.teacher_role : userInfo?.role
        const hasPermission = userInfo?.permissions?.includes('course:create') || userInfo?.permissions?.includes('course:edit') || userInfo?.permissions?.includes('course:delete')
        if (!['admin', 'head', 'advisor', 'teaching_admin'].includes(role) && !hasPermission) {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/students') {
        const role = userInfo?.role === 'teacher' ? userInfo?.teacher_role : userInfo?.role
        const hasPermission = userInfo?.permissions?.includes('student:add') || userInfo?.permissions?.includes('student:delete') || userInfo?.permissions?.includes('student:reset_pwd')
        if (!['admin', 'head', 'advisor', 'faculty', 'teaching_admin'].includes(role) && !hasPermission) {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/team-management') {
        const role = userInfo?.role === 'teacher' ? userInfo?.teacher_role : userInfo?.role
        const hasPermission = userInfo?.permissions?.includes('team:create') || userInfo?.permissions?.includes('team:delete') || userInfo?.permissions?.includes('team:remove_member')
        if (!['admin', 'head', 'advisor', 'faculty', 'teaching_admin'].includes(role) && !hasPermission) {
          next('/dashboard')
          return
        }
      }
      
      if (to.path === '/dashboard/profile') {
        // 教师缺 teacher_role 或存的是中文角色时都归一化后校验，避免被误拦截
        const role = userInfo?.role === 'teacher'
          ? (normalizeRole(userInfo?.teacher_role) || 'teacher')
          : normalizeRole(userInfo?.role)
        if (!['teacher', 'head', 'advisor', 'faculty', 'student', 'teaching_admin'].includes(role)) {
          next('/dashboard')
          return
        }
      }
      
      next()
    }
  }
})

export default router