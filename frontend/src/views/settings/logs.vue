<template>
  <div class="logs-page">
    <div class="page-card">
      <!-- 筛选区 -->
      <div class="filter-bar">
        <el-form :inline="true" @submit.prevent>
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="filter.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
              style="width: 260px"
            />
          </el-form-item>
          <el-form-item label="操作类型">
            <el-select
              v-model="filter.action_type"
              placeholder="全部"
              clearable
              style="width: 150px"
            >
              <el-option
                v-for="t in actionTypes"
                :key="t"
                :label="actionLabel(t)"
                :value="t"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="用户">
            <el-input
              v-model="filter.username"
              placeholder="用户名"
              clearable
              style="width: 160px"
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
            <el-button :icon="RefreshLeft" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 列表 -->
      <el-table
        v-loading="loading"
        :data="logs"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column prop="created_at" label="时间" width="170" />
        <el-table-column prop="username" label="用户" width="120" />
        <el-table-column prop="role" label="角色" width="90">
          <template #default="{ row }">
            <el-tag size="small" :type="roleTagType(row.role)">{{ roleText(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作类型" width="120">
          <template #default="{ row }">
            {{ actionLabel(row.action_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="action_detail" label="操作详情" min-width="220" show-overflow-tooltip />
        <el-table-column prop="ip_address" label="IP" width="130" />
        <el-table-column label="结果" width="80">
          <template #default="{ row }">
            <el-tag size="small" :type="row.result === 'success' ? 'success' : 'danger'">
              {{ row.result === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          background
          @size-change="handleSearch"
          @current-change="fetchLogs"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Search, RefreshLeft } from '@element-plus/icons-vue'
import { logsApi } from '@/api'

const loading = ref(false)
const logs = ref([])
const actionTypes = ref([])

const filter = reactive({
  dateRange: [],
  action_type: '',
  username: ''
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const ACTION_LABELS = {
  login: '登录',
  add_achievement: '新增成果',
  audit_achievement: '审核成果',
  delete_course: '删除课程',
  update_permission: '修改权限',
  delete_teacher: '删除教师'
}

const actionLabel = (type) => ACTION_LABELS[type] || type || '-'

const roleText = (role) => {
  const map = { admin: '管理员', teacher: '教师', student: '学生' }
  return map[role] || role || '-'
}

const roleTagType = (role) => {
  const map = { admin: 'danger', teacher: 'warning', student: 'primary' }
  return map[role] || 'info'
}

const fetchLogs = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (filter.dateRange && filter.dateRange.length === 2) {
      params.start_date = filter.dateRange[0]
      params.end_date = filter.dateRange[1]
    }
    if (filter.action_type) params.action_type = filter.action_type
    if (filter.username) params.username = filter.username

    const res = await logsApi.list(params)
    if (res && res.data) {
      logs.value = res.data.items || []
      pagination.total = res.data.total || 0
      // 操作类型筛选项来自后端已存在的记录（仅首次加载时刷新）
      if (res.data.action_types && res.data.action_types.length) {
        actionTypes.value = res.data.action_types
      }
    }
  } catch (e) {
    // 错误提示由 axios 拦截器统一处理
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchLogs()
}

const handleReset = () => {
  filter.dateRange = []
  filter.action_type = ''
  filter.username = ''
  handleSearch()
}

onMounted(fetchLogs)
</script>

<style scoped>
.logs-page {
  padding: 4px;
}

.page-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(22, 119, 255, 0.08);
}

.filter-bar {
  margin-bottom: 16px;
}

.filter-bar :deep(.el-form-item) {
  margin-bottom: 12px;
}

.pagination-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>