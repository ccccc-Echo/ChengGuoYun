<template>
  <div class="comp-page">
    <!-- 标题行 -->
    <div class="page-head">
      <div class="page-title-group">
        <h2 class="page-title">竞赛广场</h2>
        <span class="page-sub">共 {{ totalCount }} 项赛事</span>
      </div>
      <el-button link @click="$router.push('/student/home')">
        <el-icon class="btn-icon"><ArrowLeft /></el-icon>
        返回首页
      </el-button>
    </div>

    <!-- 搜索区 -->
    <div class="search-panel">
      <div class="search-row">
        <el-input
          v-model="keyword"
          placeholder="搜索竞赛名称，如：数学建模、挑战杯…"
          clearable
          size="large"
          class="search-input"
          @keyup.enter="doSearch"
          @clear="doSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="month" placeholder="月份" clearable class="search-select">
          <el-option v-for="m in months" :key="m" :label="m" :value="m" />
        </el-select>
        <el-select v-model="category" placeholder="分类" clearable class="search-select">
          <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
        </el-select>
        <el-button type="primary" size="large" @click="doSearch">
          <el-icon class="btn-icon"><Search /></el-icon>
          查询
        </el-button>
        <el-button size="large" @click="resetFilters">重置</el-button>
        <el-button
          size="large"
          :type="viewMode === 'mine' ? 'warning' : 'default'"
          plain
          class="mine-btn"
          @click="toggleView"
        >
          <el-icon class="btn-icon"><Star /></el-icon>
          我的比赛
        </el-button>
      </div>

      <!-- 生效的筛选条件 -->
      <div v-if="activeChips.length" class="chips-row">
        <span class="chips-label">当前筛选</span>
        <el-tag
          v-for="chip in activeChips"
          :key="chip.key"
          closable
          type="info"
          effect="plain"
          size="small"
          @close="removeChip(chip.key)"
        >
          {{ chip.label }}
        </el-tag>
        <el-button link type="primary" size="small" class="chips-clear" @click="resetFilters">清空全部</el-button>
      </div>
    </div>

    <!-- 我的比赛视图 -->
    <div v-if="viewMode === 'mine'" class="mine-view">
      <div class="section-head">
        <h3 class="section-title">我的比赛</h3>
        <span class="section-sub">共 {{ myFavorites.length }} 项</span>
      </div>
      <div v-if="myFavorites.length" class="comp-list">
        <div v-for="item in myFavorites" :key="item.id" class="comp-row">
          <div class="row-main">
            <div class="row-name" :title="item.competition.name">{{ item.competition.name }}</div>
            <div class="row-meta">
              {{ item.competition.category }} · {{ item.competition.month }}
              · 报名 {{ item.competition.sign_start || '待定' }} ~ {{ item.competition.sign_end || '待定' }}
            </div>
          </div>
          <div class="row-actions">
            <el-button size="small" type="danger" plain @click="toggleFavorite(item.competition)">取消想参加</el-button>
            <el-button size="small" @click="handleSignUp(item.competition)">报名</el-button>
          </div>
        </div>
      </div>
      <el-empty v-else description="还没有想参加的比赛，去列表里挑一挑吧" />
    </div>

    <!-- 结果列表 -->
    <template v-else>
      <div class="section-head">
        <h3 class="section-title">全部竞赛</h3>
        <span class="section-sub">{{ competitions.length }} 条结果{{ summaryText }}</span>
      </div>
      <div v-loading="loading" class="comp-list">
        <div
          v-for="item in competitions"
          :key="item.id"
          class="comp-row"
          :class="{ favorited: isFavorite(item.id) }"
        >
          <div class="row-main">
            <div class="row-title-line">
              <div class="row-name" :title="item.name">{{ item.name }}</div>
              <span v-if="isSameCategoryFav(item)" class="row-tip">同类推荐</span>
            </div>
            <div class="row-meta">
              {{ item.category }} · {{ item.month }}
              · 报名 {{ item.sign_start || '待定' }} ~ {{ item.sign_end || '待定' }}
            </div>
          </div>
          <div class="row-right">
            <span class="row-status" :class="'st-' + signStatus(item).type">{{ signStatus(item).text }}</span>
            <div class="row-actions">
              <el-button
                size="small"
                :type="isFavorite(item.id) ? 'success' : 'primary'"
                plain
                @click="toggleFavorite(item)"
              >
                {{ isFavorite(item.id) ? '已想参加' : '想参加' }}
              </el-button>
              <el-button size="small" @click="handleSignUp(item)">报名</el-button>
            </div>
          </div>
        </div>
      </div>
      <el-empty v-if="!loading && !competitions.length" description="暂无符合条件的比赛，试试调整筛选条件" />
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Star, ArrowLeft } from '@element-plus/icons-vue'
import { competitionApi } from '@/api'

const route = useRoute()
const router = useRouter()

const viewMode = ref('list')
const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

/* ---------- 筛选 ---------- */
const keyword = ref(route.query.keyword || '')
const month = ref(route.query.month || '')
const category = ref(route.query.category || '')
const categories = ref([])
const competitions = ref([])
const loading = ref(false)
const totalCount = ref(84)

const activeChips = computed(() => {
  const chips = []
  if (keyword.value) chips.push({ key: 'keyword', label: `关键词：${keyword.value}` })
  if (month.value) chips.push({ key: 'month', label: `月份：${month.value}` })
  if (category.value) chips.push({ key: 'category', label: `分类：${category.value}` })
  return chips
})

const summaryText = computed(() => {
  const parts = []
  if (month.value) parts.push(` ${month.value}`)
  if (category.value) parts.push(` ${category.value}`)
  if (keyword.value) parts.push(` “${keyword.value}”`)
  return parts.length ? `（${parts.join('，')}）` : ''
})

/* 同步 URL，便于刷新保留条件 */
const syncQuery = () => {
  const q = {}
  if (keyword.value) q.keyword = keyword.value
  if (month.value) q.month = month.value
  if (category.value) q.category = category.value
  router.replace({ path: '/student/competitions', query: q })
}

const doSearch = () => {
  syncQuery()
}

const resetFilters = () => {
  keyword.value = ''
  month.value = ''
  category.value = ''
  syncQuery()
}

const removeChip = (key) => {
  if (key === 'keyword') keyword.value = ''
  if (key === 'month') month.value = ''
  if (key === 'category') category.value = ''
  doSearch()
}

const searchCompetitions = async () => {
  loading.value = true
  try {
    const res = await competitionApi.list({
      month: month.value,
      category: category.value,
      keyword: keyword.value
    })
    competitions.value = res.competitions || []
    if (res.total) totalCount.value = res.total
  } catch (error) {
    console.error('获取竞赛列表失败:', error)
    ElMessage.error(error?.message || '获取竞赛列表失败')
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const res = await competitionApi.categories()
    categories.value = res.categories || []
  } catch (error) {
    console.error('获取竞赛分类失败:', error)
  }
}

/* 路由参数变化（如从首页跳转带关键词）时重新加载 */
watch(
  () => route.query,
  (q) => {
    keyword.value = q.keyword || ''
    month.value = q.month || ''
    category.value = q.category || ''
    searchCompetitions()
  }
)

/* ---------- 状态 ---------- */
const parseDate = (str) => {
  if (!str) return null
  const m = String(str).match(/(\d{4})[.\-\/年](\d{1,2})[.\-\/月](\d{1,2})/)
  if (!m) return null
  const d = new Date(+m[1], +m[2] - 1, +m[3])
  return isNaN(d) ? null : d
}

const signStatus = (item) => {
  const end = parseDate(item.sign_end)
  if (!end) return { type: 'info', text: '报名中' }
  const days = Math.ceil((end - new Date()) / 86400000)
  if (days < 0) return { type: 'end', text: '已结束' }
  if (days <= 15) return { type: 'soon', text: `仅剩${days}天` }
  return { type: 'hot', text: '报名中' }
}

/* ---------- 收藏（想参加 / 我的比赛） ---------- */
const myFavorites = ref([])
const favoriteIdSet = ref(new Set())

const isFavorite = (id) => favoriteIdSet.value.has(id)

const isSameCategoryFav = (item) => {
  if (isFavorite(item.id)) return false
  for (const id of favoriteIdSet.value) {
    const c = competitions.value.find((x) => x.id === id)
    if (c && c.category === item.category) return true
  }
  return false
}

const refreshFavIds = async () => {
  try {
    const res = await competitionApi.myFavorites()
    myFavorites.value = res.favorites || []
    favoriteIdSet.value = new Set((res.favorites || []).map((f) => f.competition_id))
  } catch (error) {
    console.error('获取我的比赛失败:', error)
  }
}

const toggleFavorite = async (item) => {
  const existed = isFavorite(item.id)
  try {
    if (existed) {
      await competitionApi.removeFavorite(item.id)
      ElMessage.success('已取消「想参加」')
    } else {
      await competitionApi.addFavorite(item.id)
      ElMessage.success('已加入「我的比赛」')
    }
    await refreshFavIds()
  } catch (error) {
    ElMessage.error(error?.message || '操作失败')
  }
}

const toggleView = () => {
  viewMode.value = viewMode.value === 'mine' ? 'list' : 'mine'
  if (viewMode.value === 'mine') refreshFavIds()
}

const handleSignUp = (item) => {
  ElMessage.info('报名网站开发中，敬请期待')
}

onMounted(() => {
  loadCategories()
  searchCompetitions()
  refreshFavIds()
})
</script>

<style scoped>
.comp-page {
  max-width: 1080px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 40px;
}

/* 标题行 */
.page-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title-group {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: #303133;
  margin: 0;
}

.page-sub {
  font-size: 13px;
  color: #909399;
}

/* 搜索区 */
.search-panel {
  background: #fff;
  border-radius: 8px;
  padding: 14px 16px;
  border: 1px solid #e4e7ed;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 220px;
}

.search-select {
  width: 130px;
}

.mine-btn {
  margin-left: auto;
}

/* 筛选 chips */
.chips-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}

.chips-label {
  font-size: 12px;
  color: #909399;
}

.chips-clear {
  margin-left: auto;
}

/* 区块标题 */
.section-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.section-sub {
  font-size: 12px;
  color: #909399;
}

/* 单列行式列表 */
.comp-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comp-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  padding: 14px 18px;
  transition: border-color 0.2s ease;
}

.comp-row:hover {
  border-color: #c6e2ff;
}

.comp-row.favorited {
  border-color: #a7e3c9;
  background: #f8fffc;
}

.row-main {
  flex: 1;
  min-width: 0;
}

.row-title-line {
  display: flex;
  align-items: center;
  gap: 8px;
}

.row-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-tip {
  flex-shrink: 0;
  font-size: 12px;
  color: #7b5ce7;
}

.row-meta {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-right {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.row-status {
  font-size: 13px;
  min-width: 60px;
  text-align: right;
}

.st-hot,
.st-info {
  color: #409eff;
}

.st-soon {
  color: #d48806;
}

.st-end {
  color: #c0c4cc;
}

.row-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  margin-right: 4px;
}

@media (max-width: 768px) {
  .comp-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .row-right {
    width: 100%;
    justify-content: space-between;
  }

  .mine-btn {
    margin-left: 0;
  }
}
</style>
