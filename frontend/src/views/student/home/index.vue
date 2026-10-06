<template>
  <div class="student-home">
    <!-- 标签切换（朴素分段控件） -->
    <div class="tab-bar">
      <div class="tab-item" :class="{ active: activeTab === 'class' }" @click="switchTab('class')">第二课堂</div>
      <div class="tab-item" :class="{ active: activeTab === 'resume' }" @click="switchTab('resume')">AI简历</div>
    </div>

    <!-- ============ 第二课堂 ============ -->
    <template v-if="activeTab === 'class'">
      <!-- 搜索栏 -->
      <div class="filter-card">
        <el-input
          v-model="keyword"
          placeholder="搜索竞赛名称，如：数学建模、挑战杯…"
          clearable
          size="large"
          class="filter-input"
          @keyup.enter="goSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="month" placeholder="月份" clearable class="filter-select">
          <el-option v-for="m in months" :key="m" :label="m" :value="m" />
        </el-select>
        <el-select v-model="category" placeholder="分类" clearable class="filter-select">
          <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
        </el-select>
        <el-button type="primary" size="large" @click="goSearch">
          <el-icon class="btn-icon"><Search /></el-icon>
          查询
        </el-button>
        <el-button size="large" @click="resetFilters">重置</el-button>
      </div>

      <!-- 广告牌（单张轮播） -->
      <div v-if="recommendList.length" class="banner-stage">
        <transition name="banner-fade" mode="out-in">
          <div :key="bannerIndex % recommendList.length" class="banner-card">
            <div class="banner-content">
              <div class="banner-tag">{{ recommendList[bannerIndex % recommendList.length].category }}</div>
              <div class="banner-title">{{ recommendList[bannerIndex % recommendList.length].name }}</div>
              <div class="banner-sub">
                报名 {{ recommendList[bannerIndex % recommendList.length].sign_start || '待定' }}
                ~ {{ recommendList[bannerIndex % recommendList.length].sign_end || '待定' }}
              </div>
              <el-button size="small" class="banner-btn" @click="goSearchWith(recommendList[bannerIndex % recommendList.length].name)">
                去报名
              </el-button>
            </div>
          </div>
        </transition>
        <div class="banner-dots">
          <span
            v-for="(b, i) in recommendList"
            :key="b.id"
            class="banner-dot"
            :class="{ on: i === bannerIndex % recommendList.length }"
            @click="bannerIndex = i"
          ></span>
        </div>
      </div>

      <!-- 热搜榜 -->
      <div class="hot-card">
        <div class="hot-header">
          <span class="hot-title">热搜榜</span>
          <span class="hot-sub">点击热词去发现比赛</span>
        </div>
        <div class="hot-list">
          <div v-for="(item, index) in hotList" :key="item.id" class="hot-item" @click="goSearchWith(item.name)">
            <span class="hot-rank" :class="'rank-' + (index + 1)">{{ index + 1 }}</span>
            <span class="hot-name" :title="item.name">{{ item.name }}</span>
            <span class="hot-heat">{{ item.heat ? item.heat + ' 热度' : '报名中' }}</span>
          </div>
        </div>
      </div>
    </template>

    <!-- ============ AI 简历 ============ -->
    <template v-else>
      <div class="resume-panel">
        <div class="resume-panel-head">
          <div class="panel-title">
            <el-icon class="panel-icon"><MagicStick /></el-icon>
            <span>AI 简历生成</span>
          </div>
          <span class="panel-sub">基于你提交的成果自动撰写，勾选即可生成</span>
        </div>

        <!-- 步骤 1：勾选成果 -->
        <div class="resume-step-title">
          <span class="step-num">1</span> 勾选要写入简历的成果
          <span class="step-count">已选 {{ selectedIds.length }} 项</span>
        </div>
        <div v-loading="achLoading" class="ach-list">
          <label
            v-for="a in achievements"
            :key="a.id"
            class="ach-item"
            :class="{ checked: selectedIds.includes(a.id) }"
          >
            <el-checkbox
              :model-value="selectedIds.includes(a.id)"
              class="ach-check"
              @change="toggleSelect(a.id)"
            />
            <div class="ach-info">
              <div class="ach-title">{{ a.title }}</div>
              <div class="ach-meta">
                <span>{{ a.main_category }}</span>
                <span v-if="a.level">{{ a.level }}</span>
                <span v-if="a.achieved_date">{{ a.achieved_date }}</span>
              </div>
            </div>
          </label>
          <el-empty
            v-if="!achLoading && !achievements.length"
            description="暂无成果记录，请先到「录入成果」添加"
            :image-size="80"
          />
        </div>

        <!-- 步骤 2：补充说明 -->
        <div class="resume-step-title">
          <span class="step-num">2</span> 补充说明（可选）
        </div>
        <el-input
          v-model="extra"
          type="textarea"
          :rows="extraExpanded ? 4 : 2"
          class="resume-extra"
          placeholder="如：目标岗位、想突出的方向、自我评价要点…"
          @focus="extraExpanded = true"
        />

        <!-- 步骤 3：生成 -->
        <div class="resume-submit">
          <el-button
            type="primary"
            size="large"
            :loading="generating"
            :disabled="!selectedIds.length"
            @click="handleResume"
          >
            <el-icon v-if="!generating" class="btn-icon"><MagicStick /></el-icon>
            {{ generating ? 'AI 撰写中…' : '生成简历' }}
          </el-button>
          <p v-if="!selectedIds.length" class="resume-hint">请至少勾选一项成果后再生成</p>
        </div>

        <!-- 生成结果 -->
        <div v-if="resumeResult" class="resume-result">
          <div class="resume-result-header">
            <span class="resume-result-title">生成结果</span>
            <div class="resume-result-actions">
              <el-button link type="primary" :loading="exporting" @click="downloadResume">导出 Word</el-button>
              <el-button link type="primary" @click="copyResume">复制</el-button>
            </div>
          </div>
          <pre class="resume-text">{{ resumeResult }}</pre>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, MagicStick } from '@element-plus/icons-vue'
import { aiApi, competitionApi, achievementsApi } from '@/api'

const router = useRouter()
const activeTab = ref('class')

/* ---------- 第二课堂：搜索跳转 ---------- */
const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
const categories = ref([])
const keyword = ref('')
const month = ref('')
const category = ref('')

const goSearch = () => {
  const q = {}
  if (keyword.value) q.keyword = keyword.value
  if (month.value) q.month = month.value
  if (category.value) q.category = category.value
  router.push({ path: '/student/competitions', query: q })
}

const goSearchWith = (word) => {
  router.push({ path: '/student/competitions', query: { keyword: word } })
}

const resetFilters = () => {
  keyword.value = ''
  month.value = ''
  category.value = ''
}

const loadCategories = async () => {
  try {
    const res = await competitionApi.categories()
    categories.value = res.categories || []
  } catch (error) {
    console.error('获取竞赛分类失败:', error)
  }
}

/* ---------- 第二课堂：广告牌推荐 + 热搜 ---------- */
const recommendList = ref([])
const hotList = ref([])
const bannerIndex = ref(0)
let bannerTimer = null

const startBanner = () => {
  stopBanner()
  bannerTimer = setInterval(() => {
    if (recommendList.value.length) bannerIndex.value += 1
  }, 3600)
}
const stopBanner = () => {
  if (bannerTimer) {
    clearInterval(bannerTimer)
    bannerTimer = null
  }
}

const loadRecommend = async () => {
  try {
    const res = await competitionApi.recommend()
    recommendList.value = res.competitions || []
    startBanner()
  } catch (error) {
    console.error('获取推荐比赛失败:', error)
  }
}

const loadHot = async () => {
  try {
    const res = await competitionApi.hot()
    hotList.value = res.competitions || []
  } catch (error) {
    console.error('获取热搜失败:', error)
  }
}

/* ---------- AI 简历：成果勾选 ---------- */
const achievements = ref([])
const selectedIds = ref([])
const achLoading = ref(false)
const extra = ref('')
const extraExpanded = ref(false)
const generating = ref(false)
const resumeResult = ref('')
const exporting = ref(false)

const loadAchievements = async () => {
  achLoading.value = true
  try {
    const res = await achievementsApi.list({})
    achievements.value = res.achievements || []
  } catch (error) {
    console.error('获取成果失败:', error)
    ElMessage.error(error?.message || '获取成果失败')
  } finally {
    achLoading.value = false
  }
}

const toggleSelect = (id) => {
  const idx = selectedIds.value.indexOf(id)
  if (idx >= 0) selectedIds.value.splice(idx, 1)
  else selectedIds.value.push(id)
}

const handleResume = async () => {
  if (!selectedIds.value.length) {
    ElMessage.warning('请至少勾选一项成果')
    return
  }
  generating.value = true
  resumeResult.value = ''
  try {
    const res = await aiApi.resume({
      achievement_ids: selectedIds.value,
      extra: extra.value
    })
    resumeResult.value = res.resume || ''
    if (!resumeResult.value) {
      ElMessage.error('生成结果为空，请重试')
    }
  } catch (error) {
    console.error('简历生成失败:', error)
    ElMessage.error(error?.message || '简历生成失败，请确认 Ollama 服务已启动')
  } finally {
    generating.value = false
  }
}

const copyResume = async () => {
  try {
    await navigator.clipboard.writeText(resumeResult.value)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const downloadResume = async () => {
  if (!resumeResult.value) return
  exporting.value = true
  try {
    const blob = await aiApi.exportResume({ resume: resumeResult.value })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = '我的简历.docx'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    ElMessage.success('已导出 Word 文档')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error(error?.message || '导出失败')
  } finally {
    exporting.value = false
  }
}

const switchTab = (tab) => {
  activeTab.value = tab
}

onMounted(() => {
  loadCategories()
  loadRecommend()
  loadHot()
  loadAchievements()
})
</script>

<style scoped>
.student-home {
  max-width: 1080px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 40px;
}

/* 标签切换（朴素分段控件） */
.tab-bar {
  display: flex;
  justify-content: center;
}

.tab-bar {
  background: #f0f2f5;
  border-radius: 6px;
  padding: 3px;
  gap: 4px;
  width: fit-content;
  margin: 0 auto;
}

.tab-item {
  padding: 8px 32px;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s ease, color 0.2s ease;
}

.tab-item:hover {
  color: #303133;
}

.tab-item.active {
  background: #fff;
  color: #409eff;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* 搜索栏 */
.filter-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff;
  border-radius: 8px;
  padding: 14px 16px;
  border: 1px solid #e4e7ed;
  flex-wrap: wrap;
}

.filter-select {
  width: 130px;
}

.filter-input {
  flex: 1;
  min-width: 200px;
}

/* 广告牌 */
.banner-stage {
  position: relative;
  overflow: hidden;
}

.banner-card {
  height: 150px;
  border-radius: 8px;
  background: #2f80ed;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(47, 128, 237, 0.25);
}

.banner-content {
  padding: 22px 28px;
  color: #fff;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.banner-tag {
  font-size: 12px;
  color: #fff;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 4px;
  padding: 1px 8px;
  width: fit-content;
}

.banner-title {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.4;
}

.banner-sub {
  font-size: 12px;
  opacity: 0.9;
}

.banner-btn {
  margin-top: 4px;
  width: fit-content;
  background: #fff;
  color: #2f80ed;
  border: none;
}

.banner-dots {
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 6px;
}

.banner-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.2s ease;
}

.banner-dot.on {
  background: #fff;
  width: 18px;
  border-radius: 4px;
}

.banner-fade-enter-active,
.banner-fade-leave-active {
  transition: opacity 0.4s ease;
}

.banner-fade-enter-from,
.banner-fade-leave-to {
  opacity: 0;
}

/* 热搜榜 */
.hot-card {
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.hot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f2f5;
}

.hot-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.hot-sub {
  font-size: 12px;
  color: #909399;
}

.hot-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.hot-item:hover {
  background: #f5f7fa;
}

.hot-rank {
  width: 18px;
  font-size: 14px;
  font-weight: 700;
  color: #909399;
  text-align: center;
  flex-shrink: 0;
}

.hot-rank.rank-1 {
  color: #e6a23c;
}

.hot-rank.rank-2 {
  color: #909399;
}

.hot-rank.rank-3 {
  color: #b88230;
}

.hot-name {
  flex: 1;
  font-size: 14px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hot-heat {
  font-size: 12px;
  color: #909399;
  flex-shrink: 0;
}

/* ============ AI 简历 ============ */
.resume-panel {
  background: #fff;
  border-radius: 8px;
  padding: 22px 24px;
  border: 1px solid #e4e7ed;
}

.resume-panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid #f0f2f5;
  margin-bottom: 18px;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.panel-icon {
  color: #409eff;
}

.panel-sub {
  font-size: 12px;
  color: #909399;
}

.resume-step-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.step-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.step-count {
  margin-left: auto;
  font-size: 12px;
  color: #409eff;
  font-weight: 500;
}

.ach-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 22px;
  min-height: 60px;
}

.ach-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.ach-item:hover {
  border-color: #c0c4cc;
}

.ach-item.checked {
  border-color: #409eff;
  background: #f5faff;
}

.ach-check {
  margin-top: 2px;
}

.ach-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.ach-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #909399;
  flex-wrap: wrap;
}

.resume-extra {
  margin-bottom: 18px;
}

.resume-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #b88230;
}

/* 生成结果 */
.resume-result {
  margin-top: 18px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  overflow: hidden;
}

.resume-result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.resume-result-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.resume-result-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.resume-text {
  max-height: 480px;
  overflow-y: auto;
  padding: 16px;
  margin: 0;
  font-size: 13.5px;
  line-height: 1.75;
  color: #303133;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
}

.btn-icon {
  margin-right: 4px;
}

@media (max-width: 768px) {
  .ach-list {
    grid-template-columns: 1fr;
  }
}
</style>
