<template>
  <div class="settings-container">
    <h2>系统设置</h2>
    
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="奖项类型配置" name="category">
        <el-card class="category-card">
          <div class="card-header">
            <span>奖项类型列表</span>
            <el-button type="success" @click="showCategoryDialog = true">
              <el-icon><Plus /></el-icon>
              添加类型
            </el-button>
          </div>
          
          <el-table :data="categories" stripe style="width: 100%" v-loading="categoryLoading">
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="name" label="一级分类" width="180" />
            <el-table-column prop="sub_category" label="二级分类" width="180" />
            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
            <el-table-column prop="created_at" label="创建时间" width="120" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button type="text" @click="handleCategoryEdit(row)">编辑</el-button>
                <el-button type="text" style="color: #f56c6c;" @click="handleCategoryDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
            v-model:current-page="categoryPagination.page"
            v-model:page-size="categoryPagination.page_size"
            :page-sizes="[10, 20, 50]"
            :total="categoryPagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadCategories"
            @current-change="loadCategories"
            class="pagination"
          />
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="成果知识库管理" name="knowledge">
        <el-card class="knowledge-card">
          <div class="card-header">
            <span>成果知识库列表</span>
          </div>

          <el-form :model="knowledgeFilter" inline style="margin-bottom: 16px;">
            <el-form-item label="成果标题">
              <el-input v-model="knowledgeFilter.title" placeholder="请输入成果标题" clearable style="width: 200px" />
            </el-form-item>
            <el-form-item label="学生姓名">
              <el-input v-model="knowledgeFilter.student_name" placeholder="请输入学生姓名" clearable style="width: 150px" />
            </el-form-item>
            <el-form-item label="一级分类">
              <el-select v-model="knowledgeFilter.category_level1" placeholder="请选择分类" clearable style="width: 150px">
                <el-option label="创新创业" value="创新创业" />
                <el-option label="学科竞赛" value="学科竞赛" />
                <el-option label="学术论文" value="学术论文" />
                <el-option label="专利" value="专利" />
                <el-option label="科技奖励" value="科技奖励" />
                <el-option label="社会实践" value="社会实践" />
              </el-select>
            </el-form-item>
            <el-form-item label="级别">
              <el-select v-model="knowledgeFilter.level" placeholder="请选择级别" clearable style="width: 120px">
                <el-option label="国家级" value="国家级" />
                <el-option label="省级" value="省级" />
                <el-option label="校级" value="校级" />
                <el-option label="院级" value="院级" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadKnowledge">搜索</el-button>
              <el-button @click="resetKnowledgeFilter">重置</el-button>
              <el-button type="success" :icon="Download" :loading="knowledgeExporting" @click="handleExport">导出</el-button>
            </el-form-item>
          </el-form>
          
          <el-table :data="knowledgeList" stripe style="width: 100%" v-loading="knowledgeLoading">
            <el-table-column label="选择" width="55" align="center" class-name="select-col">
              <template #default="{ row }">
                <el-checkbox
                  :model-value="knowledgeSelected.has(row.id)"
                  @change="(val) => toggleKnowledgeSelect(row.id, val)"
                  @click.stop
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
                <el-button type="text" @click="handleKnowledgeDetail(row)">详情</el-button>
                <el-button type="text" @click="handleKnowledgeEdit(row)">编辑</el-button>
                <el-button type="text" style="color: #f56c6c;" @click="handleKnowledgeDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
            v-model:current-page="knowledgePagination.page"
            v-model:page-size="knowledgePagination.page_size"
            :page-sizes="[10, 20, 50]"
            :total="knowledgePagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadKnowledge"
            @current-change="loadKnowledge"
            class="pagination"
          />
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showCategoryDialog" :title="isCategoryEditing ? '编辑奖项类型' : '添加奖项类型'" width="500px">
      <el-form ref="categoryFormRef" :model="categoryForm" :rules="categoryRules" label-width="100px">
        <el-form-item label="一级分类" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入一级分类名称" />
        </el-form-item>
        <el-form-item label="二级分类">
          <el-input v-model="categoryForm.sub_category" placeholder="请输入二级分类名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="categoryForm.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCategoryDialog = false">取消</el-button>
        <el-button type="primary" :loading="categorySaving" @click="handleCategorySave">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showKnowledgeDialog" title="编辑成果" width="600px" :close-on-click-modal="false">
      <el-form ref="knowledgeFormRef" :model="knowledgeForm" :rules="knowledgeEditRules" label-width="100px">
        <el-form-item label="成果标题" prop="title">
          <el-input v-model="knowledgeForm.title" placeholder="请输入成果标题" />
        </el-form-item>
        <el-form-item label="一级分类" prop="category_level1">
          <el-select v-model="knowledgeForm.category_level1" placeholder="请选择分类" style="width: 100%;">
            <el-option label="创新创业" value="创新创业" />
            <el-option label="学科竞赛" value="学科竞赛" />
            <el-option label="学术论文" value="学术论文" />
            <el-option label="专利" value="专利" />
            <el-option label="科技奖励" value="科技奖励" />
            <el-option label="社会实践" value="社会实践" />
          </el-select>
        </el-form-item>
        <el-form-item label="二级细分">
          <el-select v-model="knowledgeForm.category_level2" placeholder="请选择细分" style="width: 100%;">
            <el-option label="国家级" value="国家级" />
            <el-option label="省级" value="省级" />
            <el-option label="校级" value="校级" />
            <el-option label="院级" value="院级" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="knowledgeForm.level" placeholder="请选择级别" style="width: 100%;">
            <el-option label="国家级" value="国家级" />
            <el-option label="省级" value="省级" />
            <el-option label="校级" value="校级" />
            <el-option label="院级" value="院级" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="knowledgeForm.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="证明材料">
          <el-input v-model="knowledgeForm.proof_material" placeholder="证明材料路径（多个用逗号分隔）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showKnowledgeDialog = false">取消</el-button>
        <el-button type="primary" :loading="knowledgeSaving" @click="handleKnowledgeSave">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showKnowledgeDetailDialog" title="成果详情" width="600px" :close-on-click-modal="false">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="成果标题">{{ knowledgeDetailData.title }}</el-descriptions-item>
        <el-descriptions-item label="一级分类">{{ getMainCategoryLabel(knowledgeDetailData.category_level1) }}</el-descriptions-item>
        <el-descriptions-item label="二级细分">{{ getSubCategoryLabel(knowledgeDetailData.category_level2) || '-' }}</el-descriptions-item>
        <el-descriptions-item label="级别">{{ getLevelLabel(knowledgeDetailData.level) }}</el-descriptions-item>
        <el-descriptions-item label="学生姓名">{{ knowledgeDetailData.student_name }}</el-descriptions-item>
        <el-descriptions-item label="班级">{{ knowledgeDetailData.class_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ knowledgeDetailData.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="证明材料">
          <div v-if="knowledgeDetailData.proof_material" class="proof-files">
            <a v-for="(file, index) in knowledgeDetailData.proof_material.split(',')" :key="index" :href="file" target="_blank">
              {{ file }}
            </a>
          </div>
          <span v-else>无</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">{{ knowledgeDetailData.status === 'approved' ? '已通过' : knowledgeDetailData.status }}</el-descriptions-item>
        <el-descriptions-item label="审核人">{{ knowledgeDetailData.auditor_name || '无' }}</el-descriptions-item>
        <el-descriptions-item label="审核意见">{{ knowledgeDetailData.audit_comment || '无' }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ knowledgeDetailData.submitted_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ knowledgeDetailData.reviewed_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="录入知识库时间">{{ knowledgeDetailData.created_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ knowledgeDetailData.updated_at || '-' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button type="success" :icon="Download" :loading="knowledgeDetailExporting" @click="handleExportOne">导出</el-button>
        <el-button @click="showKnowledgeDetailDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download } from '@element-plus/icons-vue'
import { settingsApi, knowledgeBaseApi } from '@/api'
import { getMainCategoryLabel, getSubCategoryLabel, getLevelLabel } from '@/utils/constants'

const activeTab = ref('category')

const categoryLoading = ref(false)
const categorySaving = ref(false)
const categories = ref([])
const showCategoryDialog = ref(false)
const categoryFormRef = ref(null)
const isCategoryEditing = ref(false)
const categoryEditId = ref(null)

const knowledgeLoading = ref(false)
const knowledgeSaving = ref(false)
const knowledgeExporting = ref(false)
const knowledgeDetailExporting = ref(false)
const knowledgeList = ref([])
const knowledgeSelected = ref(new Set())
const showKnowledgeDialog = ref(false)
const showKnowledgeDetailDialog = ref(false)
const knowledgeFormRef = ref(null)
const isKnowledgeEditing = ref(false)
const knowledgeEditId = ref(null)
const knowledgeDetailData = ref({})

const categoryPagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const knowledgePagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const categoryForm = ref({
  name: '',
  sub_category: '',
  description: ''
})

const categoryRules = {
  name: [
    { required: true, message: '请输入一级分类名称', trigger: 'blur' }
  ]
}

const knowledgeFilter = reactive({
  title: '',
  student_name: '',
  category_level1: '',
  category_level2: '',
  level: ''
})

const knowledgeForm = reactive({
  title: '',
  category_level1: '',
  category_level2: '',
  level: '',
  description: '',
  proof_material: ''
})

const knowledgeEditRules = {
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

const loadCategories = async () => {
  categoryLoading.value = true
  try {
    const params = {
      page: categoryPagination.value.page,
      page_size: categoryPagination.value.page_size
    }
    
    const res = await settingsApi.listCategories(params)
    categories.value = res.categories || []
    categoryPagination.value.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载奖项类型失败:', error)
    ElMessage.error('加载奖项类型失败')
  } finally {
    categoryLoading.value = false
  }
}

const loadKnowledge = async () => {
  knowledgeLoading.value = true
  try {
    const params = {
      page: knowledgePagination.value.page,
      page_size: knowledgePagination.value.page_size,
      ...knowledgeFilter
    }
    
    const res = await knowledgeBaseApi.list(params)
    knowledgeList.value = res.knowledge_base || []
    knowledgePagination.value.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载知识库失败:', error)
    ElMessage.error('加载知识库失败')
  } finally {
    knowledgeLoading.value = false
  }
}

const handleTabChange = (tab) => {
  if (tab === 'knowledge') {
    loadKnowledge()
  }
}

const resetKnowledgeFilter = () => {
  knowledgeFilter.title = ''
  knowledgeFilter.student_name = ''
  knowledgeFilter.category_level1 = ''
  knowledgeFilter.category_level2 = ''
  knowledgeFilter.level = ''
  knowledgePagination.value.page = 1
  knowledgeSelected.value = new Set()
  loadKnowledge()
}

const toggleKnowledgeSelect = (id, checked) => {
  const next = new Set(knowledgeSelected.value)
  if (checked) next.add(id)
  else next.delete(id)
  knowledgeSelected.value = next
}

const handleCategoryEdit = (row) => {
  isCategoryEditing.value = true
  categoryEditId.value = row.id
  categoryForm.value = {
    name: row.name,
    sub_category: row.sub_category || '',
    description: row.description || ''
  }
  showCategoryDialog.value = true
}

const handleCategoryDelete = (row) => {
  ElMessageBox.confirm('确定删除该奖项类型吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await settingsApi.deleteCategory(row.id)
      ElMessage.success('删除成功')
      loadCategories()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  })
}

const handleCategorySave = async () => {
  if (!categoryFormRef.value) return
  
  try {
    await categoryFormRef.value.validate()
    categorySaving.value = true
    
    if (isCategoryEditing.value) {
      await settingsApi.updateCategory(categoryEditId.value, categoryForm.value)
      ElMessage.success('奖项类型更新成功')
    } else {
      await settingsApi.createCategory(categoryForm.value)
      ElMessage.success('奖项类型添加成功')
    }
    
    showCategoryDialog.value = false
    categoryForm.value = {
      name: '',
      sub_category: '',
      description: ''
    }
    isCategoryEditing.value = false
    categoryEditId.value = null
    loadCategories()
  } catch (error) {
    if (error !== false) {
      console.error('保存失败:', error)
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    categorySaving.value = false
  }
}

const handleKnowledgeDetail = async (row) => {
  try {
    const res = await knowledgeBaseApi.get(row.id)
    knowledgeDetailData.value = res.knowledge || row
    showKnowledgeDetailDialog.value = true
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败')
  }
}

const handleKnowledgeEdit = (row) => {
  isKnowledgeEditing.value = true
  knowledgeEditId.value = row.id
  knowledgeForm.title = row.title
  knowledgeForm.category_level1 = row.category_level1
  knowledgeForm.category_level2 = row.category_level2 || ''
  knowledgeForm.level = row.level
  knowledgeForm.description = row.description || ''
  knowledgeForm.proof_material = row.proof_material || ''
  showKnowledgeDialog.value = true
}

const handleKnowledgeDelete = (row) => {
  ElMessageBox.confirm('确定删除该知识库记录吗？删除后将同时删除备份文件，此操作不可恢复。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await knowledgeBaseApi.delete(row.id)
      ElMessage.success('删除成功')
      loadKnowledge()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  })
}

const handleKnowledgeSave = async () => {
  if (!knowledgeFormRef.value) return
  
  try {
    await knowledgeFormRef.value.validate()
    knowledgeSaving.value = true
    
    const data = {
      title: knowledgeForm.title,
      category_level1: knowledgeForm.category_level1,
      category_level2: knowledgeForm.category_level2,
      level: knowledgeForm.level,
      description: knowledgeForm.description,
      proof_material: knowledgeForm.proof_material
    }
    
    await knowledgeBaseApi.update(knowledgeEditId.value, data)
    ElMessage.success('知识库记录更新成功')
    
    showKnowledgeDialog.value = false
    knowledgeForm.title = ''
    knowledgeForm.category_level1 = ''
    knowledgeForm.category_level2 = ''
    knowledgeForm.level = ''
    knowledgeForm.description = ''
    knowledgeForm.proof_material = ''
    isKnowledgeEditing.value = false
    knowledgeEditId.value = null
    loadKnowledge()
  } catch (error) {
    if (error !== false) {
      console.error('保存失败:', error)
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    knowledgeSaving.value = false
  }
}

const handleExport = async () => {
  const selectedIds = [...knowledgeSelected.value]
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

  knowledgeExporting.value = true
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
    knowledgeSelected.value = new Set()
  } catch (error) {
    console.error('导出失败:', error)
  } finally {
    knowledgeExporting.value = false
  }
}

const handleExportOne = async () => {
  const item = knowledgeDetailData.value
  if (!item || !item.id) {
    ElMessage.warning('未找到可导出的成果')
    return
  }
  knowledgeDetailExporting.value = true
  try {
    const blob = await knowledgeBaseApi.exportOne(item.id)
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
    // 文件名：成果_<成果标题>_<学生姓名>.pdf（去除文件名非法字符）
    const safeTitle = (item.title || '').replace(/[\\/:*?"<>|]/g, '_').trim() || '-'
    const safeName = (item.student_name || '').replace(/[\\/:*?"<>|]/g, '_').trim() || '-'
    link.download = `成果_${safeTitle}_${safeName}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('成果导出成功')
  } catch (error) {
    console.error('导出失败:', error)
  } finally {
    knowledgeDetailExporting.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.settings-container {
  padding: 0;
}

h2 {
  margin-bottom: 20px;
  color: #222;
  font-size: 22px;
  font-weight: 600;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #222;
}

.category-card,
.knowledge-card {
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-card) {
  border-radius: 12px;
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

:deep(.el-tabs__header) {
  margin-bottom: 20px;
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: rgba(0, 0, 0, 0.05);
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
</style>