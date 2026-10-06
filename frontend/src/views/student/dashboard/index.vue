<template>
  <div class="student-dashboard-wrapper">
    <StudentDashboard />
  </div>
</template>

<script setup>
import StudentDashboard from '@/views/dashboard/index.vue'
</script>

<style scoped>
.student-dashboard-wrapper {
  width: 100%;
  height: 100%;
}

.student-dashboard-wrapper :deep(.dashboard-container) {
  min-height: calc(100vh - 60px - 48px);
  padding: 16px;
  background: transparent;
}

.student-dashboard-wrapper :deep(.welcome-section) {
  padding: 20px;
  margin-bottom: 16px;
}

.student-dashboard-wrapper :deep(.welcome-text h1) {
  font-size: 20px;
}

.student-dashboard-wrapper :deep(.stat-value) {
  font-size: 28px;
}

.student-dashboard-wrapper :deep(.charts-row),
.student-dashboard-wrapper :deep(.tables-row),
.student-dashboard-wrapper :deep(.stats-row) {
  margin-bottom: 16px;
}
</style>