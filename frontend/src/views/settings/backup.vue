<template>
  <div class="backup-page">
    <div class="page-card">
      <div class="page-header">
        <div class="header-left">
          <h3>数据备份</h3>
          <span class="desc">数据库中所有数据，自动生成备份文件，保留最近 30 天</span>
        </div>
        <el-button type="primary" :icon="Refresh" :loading="creating" @click="handleCreate">
          立即备份
        </el-button>
      </div>

      <!-- 备份列表 -->
      <el-table v-loading="loading" :data="backups" border stripe style="width: 100%">
        <el-table-column label="序号" type="index" width="60" align="center" />
        <el-table-column prop="filename" label="文件名" min-width="220" />
        <el-table-column prop="size_display" label="大小" width="100" align="center" />
        <el-table-column prop="backup_time" label="备份时间" width="170" />
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <el-button link type="primary" :icon="Download" @click="handleDownload(row)">
              下载
            </el-button>
            <el-button link type="danger" :icon="Delete" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && backups.length === 0" description="暂无备份文件，点击右上角“立即备份”" />

      <!-- 使用说明 -->
      <div class="help-box">
        <h4><el-icon><InfoFilled /></el-icon> 使用说明</h4>
        <ul>
          <li><b>自动备份</b>：系统任务计划程序每天凌晨 2 点自动执行 <code>backup/backup.py</code> 生成备份。</li>
          <li><b>自动清理</b>：每次备份后自动删除 30 天前的备份文件。</li>
          <li><b>手动备份</b>：点击右上角“立即备份”生成当天备份。</li>
          <li><b>还原数据</b>：下载备份文件后使用 <code>mysql -u root -p 数据库名 &lt; 备份文件.sql</code> 还原。</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Download, Delete, InfoFilled } from '@element-plus/icons-vue'
import { backupApi } from '@/api'

const loading = ref(false)
const creating = ref(false)
const backups = ref([])

const fetchList = async () => {
  loading.value = true
  try {
    const res = await backupApi.list()
    if (res && res.data) {
      backups.value = res.data || []
    }
  } catch (e) {
    // 错误由拦截器统一提示
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  creating.value = true
  try {
    const res = await backupApi.create()
    if (res && res.code === 200) {
      ElMessage.success(res.message || '备份成功')
      await fetchList()
    }
  } catch (e) {
    // 错误由拦截器统一提示
  } finally {
    creating.value = false
  }
}

const handleDownload = (row) => {
  backupApi.download(row.filename).then((blob) => {
    // 创建临时链接触发下载
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = row.filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  })
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定删除备份文件「${row.filename}」吗？删除后不可恢复。`,
    '删除提示',
    { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' }
  ).then(async () => {
    try {
      const res = await backupApi.delete(row.filename)
      if (res && res.code === 200) {
        ElMessage.success('删除成功')
        await fetchList()
      }
    } catch (e) {
      // 错误由拦截器统一提示
    }
  }).catch(() => {})
}

onMounted(fetchList)
</script>

<style scoped>
.backup-page {
  padding: 4px;
}

.page-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(22, 119, 255, 0.08);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.page-header h3 {
  margin: 0;
  font-size: 18px;
  color: #1f2d3d;
}

.page-header .desc {
  display: block;
  margin-top: 4px;
  font-size: 13px;
  color: #909399;
}

.help-box {
  margin-top: 22px;
  padding: 14px 18px;
  background: #f6f9fe;
  border-radius: 8px;
  border: 1px solid #e3edfb;
}

.help-box h4 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #1677ff;
  display: flex;
  align-items: center;
  gap: 6px;
}

.help-box ul {
  margin: 0;
  padding-left: 18px;
  color: #555;
  line-height: 1.9;
  font-size: 13px;
}

.help-box code {
  background: #eef1f5;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 12px;
  color: #c7254e;
}
</style>