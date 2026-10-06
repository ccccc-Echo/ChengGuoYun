<template>
  <div class="cert-export-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          <span>返回个人中心</span>
        </button>
        <div class="title-wrap">
          <div class="title-icon">
            <el-icon :size="20"><Trophy /></el-icon>
          </div>
          <div>
            <h1 class="page-title">导出获奖证书汇总</h1>
            <p class="page-subtitle">选择已通过成果，一键生成含证明材料的 PDF 汇总表</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Card -->
    <div class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form" @submit.prevent>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            unlink-panels
            clearable
            style="width: 280px"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filterForm.main_category" placeholder="全部" clearable style="width: 150px">
            <el-option v-for="item in mainCategoryOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="filterForm.level" placeholder="全部" clearable style="width: 130px">
            <el-option v-for="item in levelOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="已通过" value="approved" />
            <el-option label="待审核" value="pending" />
            <el-option label="已驳回" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
          <el-button :icon="Refresh" @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <div class="table-toolbar">
        <div class="toolbar-info">
          共 <b>{{ list.length }}</b> 条成果，已选 <b class="selected-count">{{ selectedRows.length }}</b> 条
        </div>
        <el-button
          type="primary"
          :icon="Download"
          :loading="exporting"
          :disabled="selectedRows.length === 0"
          @click="handleExport"
        >
          导出 PDF
        </el-button>
      </div>

      <el-table
        ref="tableRef"
        :data="list"
        v-loading="loading"
        @selection-change="handleSelectionChange"
        row-key="id"
        empty-text="暂无符合条件的已通过成果"
        style="width: 100%"
      >
        <el-table-column type="selection" width="48" reserve-selection />
        <el-table-column type="index" label="序号" width="64" align="center" />
        <el-table-column prop="title" label="成果标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="一级分类" width="120">
          <template #default="{ row }">{{ getMainCategoryLabel(row.main_category) }}</template>
        </el-table-column>
        <el-table-column label="二级细分" width="120">
          <template #default="{ row }">{{ getSubCategoryLabel(row.sub_category) || '-' }}</template>
        </el-table-column>
        <el-table-column label="级别" width="90">
          <template #default="{ row }">
            <el-tag size="small" effect="plain">{{ getLevelLabel(row.level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="获奖日期" width="120" align="center">
          <template #default="{ row }">{{ row.achieved_date || '-' }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核人" min-width="160">
          <template #default="{ row }">{{ row.auditor_display || row.auditor_name || '-' }}</template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Trophy, Search, Refresh, Download } from '@element-plus/icons-vue'
import { achievementsApi, exportApi } from '@/api'
import {
  mainCategoryMap, levelMap,
  getMainCategoryLabel, getSubCategoryLabel, getLevelLabel
} from '@/utils/constants'

const router = useRouter()
const tableRef = ref(null)

const loading = ref(false)
const exporting = ref(false)
const list = ref([])
const selectedRows = ref([])

const filterForm = reactive({
  dateRange: [],
  main_category: '',
  level: '',
  status: 'approved'
})

const mainCategoryOptions = Object.entries(mainCategoryMap).map(([value, label]) => ({ value, label }))
const levelOptions = Object.entries(levelMap).map(([value, label]) => ({ value, label }))

const statusLabel = (status) => {
  const map = { approved: '已通过', pending: '待审核', rejected: '已驳回' }
  return map[status] || status
}
const statusTagType = (status) => {
  const map = { approved: 'success', pending: 'warning', rejected: 'danger' }
  return map[status] || 'info'
}

const goBack = () => {
  router.push('/student/center')
}

const loadList = async () => {
  loading.value = true
  try {
    const params = {
      page: 1,
      page_size: 1000,
      main_category: filterForm.main_category || undefined,
      level: filterForm.level || undefined,
      status: filterForm.status || undefined,
      include_auditor_team: 'true'
    }
    if (filterForm.dateRange && filterForm.dateRange.length === 2) {
      params.start_date = filterForm.dateRange[0]
      params.end_date = filterForm.dateRange[1]
    }
    const res = await achievementsApi.list(params)
    list.value = res.achievements || []
  } catch (error) {
    console.error('加载成果列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadList()
}

const resetFilter = () => {
  filterForm.dateRange = []
  filterForm.main_category = ''
  filterForm.level = ''
  filterForm.status = 'approved'
  loadList()
}

const handleSelectionChange = (rows) => {
  selectedRows.value = rows
}

const handleExport = async () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请至少选择一项成果')
    return
  }
  exporting.value = true
  try {
    const blob = await exportApi.certificates({
      achievement_ids: selectedRows.value.map(r => r.id)
    })
    // 后端正常返回 PDF 二进制流；若意外返回 JSON（错误），给出提示
    if (blob instanceof Blob && blob.type && blob.type.includes('application/json')) {
      const text = await blob.text()
      const err = JSON.parse(text)
      ElMessage.error(err.error || err.message || '导出失败')
      return
    }
    const url = window.URL.createObjectURL(
      blob instanceof Blob ? blob : new Blob([blob], { type: 'application/pdf' })
    )
    const link = document.createElement('a')
    link.href = url
    const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '')
    link.download = `获奖证书汇总_${dateStr}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success(`已导出 ${selectedRows.value.length} 项成果`)
  } catch (error) {
    console.error('导出失败:', error)
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  loadList()
})
</script>

<style scoped>
.cert-export-page {
  min-height: 100%;
}

/* ============ Page Header ============ */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  background: #fff;
  color: #5a5a6a;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}

.back-btn:hover {
  border-color: #4095e5;
  color: #4095e5;
  background: rgba(64, 149, 229, 0.04);
  transform: translateX(-2px);
}

.title-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
}

.title-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background: linear-gradient(135deg, #4095e5, #5ba8f5);
  box-shadow: 0 6px 16px rgba(64, 149, 229, 0.35);
}

.page-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  letter-spacing: -0.3px;
}

.page-subtitle {
  margin: 4px 0 0;
  font-size: 13px;
  color: #8c8c9a;
}

/* ============ Cards ============ */
.filter-card,
.table-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px 24px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.filter-card {
  border-top: 3px solid transparent;
  background:
    linear-gradient(#fff, #fff) padding-box,
    linear-gradient(90deg, rgba(64, 149, 229, 0.5), rgba(91, 168, 245, 0.1)) border-box;
  border-top: 3px solid transparent;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 8px;
  align-items: center;
}

.filter-form :deep(.el-form-item) {
  margin-bottom: 8px;
  margin-right: 8px;
}

.filter-form :deep(.el-form-item__label) {
  color: #5a5a6a;
  font-weight: 500;
}

/* ============ Table Toolbar ============ */
.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid #f0f1f2;
}

.toolbar-info {
  font-size: 14px;
  color: #8c8c9a;
}

.toolbar-info b {
  color: #4095e5;
  font-weight: 600;
}

.toolbar-info .selected-count {
  color: #e6a23c;
}

/* ============ Table ============ */
:deep(.el-table) {
  border-radius: 10px;
  overflow: hidden;
}

:deep(.el-table th.el-table__cell) {
  background: #f7f8fa;
  color: #5a5a6a;
  font-weight: 600;
  font-size: 13px;
}

:deep(.el-table td.el-table__cell) {
  font-size: 13.5px;
  color: #2a2a3a;
}

:deep(.el-table__row:hover > td.el-table__cell) {
  background: rgba(64, 149, 229, 0.04) !important;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #4095e5;
  border-color: #4095e5;
}

:deep(.el-table-column--selection .cell) {
  padding-left: 10px;
  padding-right: 10px;
}
</style>
