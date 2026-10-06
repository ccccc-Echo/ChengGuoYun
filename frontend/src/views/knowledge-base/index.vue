<template>
  <div class="knowledge-base-container">
    <div class="page-header">
      <h2>成果知识库管理</h2>
    </div>

    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="成果标题">
          <el-input v-model="filterForm.title" placeholder="请输入成果标题" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="学生姓名">
          <el-input v-model="filterForm.student_name" placeholder="请输入学生姓名" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="一级分类">
          <el-select v-model="filterForm.category_level1" placeholder="请选择分类" clearable style="width: 150px">
            <el-option v-for="(label, value) in mainCategoryMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item label="二级细分">
          <el-select v-model="filterForm.category_level2" placeholder="请选择细分" clearable style="width: 150px">
            <el-option v-for="(label, value) in subCategoryMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="filterForm.level" placeholder="请选择级别" clearable style="width: 120px">
            <el-option v-for="(label, value) in levelMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadKnowledgeBase">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
          <el-button type="success" :icon="Download" :loading="exporting" @click="handleExport">导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table :data="knowledgeList" stripe style="width: 100%" v-loading="loading"
          @row-mouse-enter="(row) => hoverId = row.id"
          @row-mouse-leave="(row) => hoverId === row.id && (hoverId = null)">
        <el-table-column label="选择" width="50" align="center" class-name="select-col">
          <template #default="{ row }">
            <el-checkbox
              :model-value="selected.has(row.id)"
              @change="(val) => toggleSelect(row.id, val)"
              @click.stop
              :style="{ visibility: selected.has(row.id) || hoverId === row.id ? 'visible' : 'hidden' }"
            />
          </template>
        </el-table-column>
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="title" label="成果标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="student_name" label="学生姓名" width="120" />
        <el-table-column prop="class_name" label="班级" width="150" />
        <el-table-column label="一级分类" width="120">
          <template #default="{ row }">{{ getMainCategoryLabel(row.category_level1) }}</template>
        </el-table-column>
        <el-table-column label="二级细分" width="120">
          <template #default="{ row }">{{ getSubCategoryLabel(row.category_level2) || '-' }}</template>
        </el-table-column>
        <el-table-column label="级别" width="100">
          <template #default="{ row }">{{ getLevelLabel(row.level) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag type="success">{{ row.status === 'approved' ? '已通过' : row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="auditor_name" label="审核人" width="120" />
        <el-table-column prop="created_at" label="录入时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="text" @click="handleDetail(row)">详情</el-button>
            <el-button type="text" @click="handleEdit(row)">编辑</el-button>
            <el-button type="text" style="color: #f56c6c;" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadKnowledgeBase"
        @current-change="loadKnowledgeBase"
        class="pagination"
      />
    </el-card>

    <el-dialog v-model="showDetailDialog" title="成果详情" width="600px" :close-on-click-modal="false">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="成果标题">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="一级分类">{{ getMainCategoryLabel(detailData.category_level1) }}</el-descriptions-item>
        <el-descriptions-item label="二级细分">{{ getSubCategoryLabel(detailData.category_level2) || '-' }}</el-descriptions-item>
        <el-descriptions-item label="级别">{{ getLevelLabel(detailData.level) }}</el-descriptions-item>
        <el-descriptions-item label="学生姓名">{{ detailData.student_name }}</el-descriptions-item>
        <el-descriptions-item label="班级">{{ detailData.class_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ detailData.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="证明材料">
          <div v-if="detailData.proof_material" class="proof-files">
            <a v-for="(file, index) in detailData.proof_material.split(',')" :key="index" :href="file" target="_blank">
              {{ file }}
            </a>
          </div>
          <span v-else>无</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">{{ detailData.status === 'approved' ? '已通过' : detailData.status }}</el-descriptions-item>
        <el-descriptions-item label="审核人">{{ detailData.auditor_name || '无' }}</el-descriptions-item>
        <el-descriptions-item label="审核意见">{{ detailData.audit_comment || '无' }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ detailData.submitted_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ detailData.reviewed_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="录入知识库时间">{{ detailData.created_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailData.updated_at || '-' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditDialog" title="编辑成果" width="600px" :close-on-click-modal="false">
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="100px">
        <el-form-item label="成果标题" prop="title">
          <el-input v-model="editForm.title" placeholder="请输入成果标题" />
        </el-form-item>
        <el-form-item label="一级分类" prop="category_level1">
          <el-select v-model="editForm.category_level1" placeholder="请选择分类" style="width: 100%;">
            <el-option v-for="(label, value) in mainCategoryMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item label="二级细分">
          <el-select v-model="editForm.category_level2" placeholder="请选择细分" style="width: 100%;">
            <el-option v-for="(label, value) in subCategoryMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="editForm.level" placeholder="请选择级别" style="width: 100%;">
            <el-option v-for="(label, value) in levelMap" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="证明材料">
          <el-input v-model="editForm.proof_material" placeholder="证明材料路径（多个用逗号分隔）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSaveEdit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import { knowledgeBaseApi } from '@/api'
import { getMainCategoryLabel, getSubCategoryLabel, getLevelLabel, mainCategoryMap, subCategoryMap, levelMap } from '@/utils/constants'

const loading = ref(false)
const saving = ref(false)
const exporting = ref(false)
const knowledgeList = ref([])
const selected = ref(new Set())
const hoverId = ref(null)
const showDetailDialog = ref(false)
const showEditDialog = ref(false)
const editFormRef = ref(null)
const detailData = ref({})

const editForm = reactive({
  title: '',
  category_level1: '',
  category_level2: '',
  level: '',
  description: '',
  proof_material: ''
})

const editRules = {
  title: [
    { required: true, message: '请输入成果标题', trigger: 'blur' }
  ],
  category_level1: [
    { required: true, message: '请选择一级分类', trigger: 'change' }
  ],
  level: [
    { required: true, message: '请选择级别', trigger: 'change' }
  ]
}

const filterForm = reactive({
  title: '',
  student_name: '',
  category_level1: '',
  category_level2: '',
  level: ''
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})



const loadKnowledgeBase = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...filterForm
    }
    
    const res = await knowledgeBaseApi.list(params)
    knowledgeList.value = res.knowledge_base || []
    pagination.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载知识库失败:', error)
    ElMessage.error('加载知识库失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.title = ''
  filterForm.student_name = ''
  filterForm.category_level1 = ''
  filterForm.category_level2 = ''
  filterForm.level = ''
  pagination.page = 1
  clearSelection()
  loadKnowledgeBase()
}

const toggleSelect = (id, checked) => {
  const next = new Set(selected.value)
  if (checked) next.add(id)
  else next.delete(id)
  selected.value = next
}

const clearSelection = () => {
  selected.value = new Set()
}

const handleDetail = async (row) => {
  try {
    const res = await knowledgeBaseApi.get(row.id)
    detailData.value = res.knowledge || row
    showDetailDialog.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败')
  }
}

const handleEdit = (row) => {
  editForm.title = row.title
  editForm.category_level1 = row.category_level1
  editForm.category_level2 = row.category_level2 || ''
  editForm.level = row.level
  editForm.description = row.description || ''
  editForm.proof_material = row.proof_material || ''
  editForm.id = row.id
  showEditDialog.value = true
}

const handleSaveEdit = async () => {
  if (!editFormRef.value) return
  
  try {
    await editFormRef.value.validate()
    saving.value = true
    
    const data = {
      title: editForm.title,
      category_level1: editForm.category_level1,
      category_level2: editForm.category_level2,
      level: editForm.level,
      description: editForm.description,
      proof_material: editForm.proof_material
    }
    
    await knowledgeBaseApi.update(editForm.id, data)
    ElMessage.success('编辑成功')
    showEditDialog.value = false
    loadKnowledgeBase()
  } catch (error) {
    if (error !== false) {
      console.error('保存失败:', error)
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该知识库记录吗？删除后将同时删除备份文件，此操作不可恢复。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await knowledgeBaseApi.delete(row.id)
      ElMessage.success('删除成功')
      loadKnowledgeBase()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  })
}

const handleExport = async () => {
  const selectedIds = [...selected.value]
  const hasSelected = selectedIds.length > 0
  const msg = hasSelected
    ? `已勾选 ${selectedIds.length} 条成果，确认只导出选中成果吗？`
    : '未勾选任何成果，确认导出当前知识库中所有成果吗？'
  try {
    await ElMessageBox.confirm(msg, '导出确认', {
      confirmButtonText: '确认导出',
      cancelButtonText: '取消',
      type: 'info'
    })
  } catch {
    return
  }

  exporting.value = true
  try {
    const blob = await knowledgeBaseApi.export(hasSelected ? selectedIds : null)
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
    link.download = `成果知识库汇总_${dateStr}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('知识库导出成功')
    clearSelection()
  } catch (error) {
    console.error('导出失败:', error)
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  loadKnowledgeBase()
})
</script>

<style scoped>
.knowledge-base-container {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #222;
}

.filter-card,
.table-card {
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.proof-files {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.proof-files a {
  color: #1677ff;
  text-decoration: underline;
  word-break: break-all;
}

:deep(.el-card__header) {
  padding: 18px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

:deep(.el-card__body) {
  padding: 20px 24px;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background: rgba(64, 149, 229, 0.03);
  color: #666;
  font-weight: 500;
  font-size: 13px;
}

:deep(.el-table tr:hover > td) {
  background: rgba(64, 149, 229, 0.03);
}

:deep(.el-descriptions) {
  margin-top: 10px;
}
</style>
