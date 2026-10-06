<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, shallowRef } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  height: {
    type: String,
    default: '300px'
  }
})

const chartRef = ref(null)
const chartInstance = shallowRef(null)

const initChart = () => {
  if (!chartRef.value) return
  
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
  
  chartInstance.value = echarts.init(chartRef.value)
  
  const indicator = props.chartData?.indicator || []
  const seriesData = props.chartData?.series || []
  
  const validatedSeries = seriesData.map(s => {
    if (s.value && indicator.length > 0) {
      const values = [...s.value]
      while (values.length < indicator.length) {
        values.push(0)
      }
      return { ...s, value: values.slice(0, indicator.length) }
    }
    return s
  })
  
  const option = {
    tooltip: {},
    legend: {
      data: props.chartData?.legend || [],
      bottom: 0
    },
    radar: {
      indicator: indicator,
      center: ['50%', '50%'],
      radius: '65%'
    },
    series: [
      {
        type: 'radar',
        data: validatedSeries
      }
    ]
  }
  
  chartInstance.value.setOption(option)
}

const handleResize = () => {
  if (chartInstance.value) {
    chartInstance.value.resize()
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
})

watch(() => props.chartData, () => {
  initChart()
}, { deep: true })

defineExpose({
  resize: handleResize
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: v-bind(height);
}
</style>
