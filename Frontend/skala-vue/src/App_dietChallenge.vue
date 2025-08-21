<template>
  <div>
    <h2>홍길동의 BMI 상태</h2>
    
    <!-- 현재 상태 표시 -->
    <p>현재 체중: {{ weight }}kg</p>
    <p>현재 키: {{ height }}cm</p>
    <p>BMI: {{ bmi }} ({{ bmiStatus }})</p>
    
    <!-- 자식 컴포넌트들 -->
    <EatFood @eat="handleEat" />
    <PracticeSkill @practice="handlePractice" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import EatFood from './components/EatFood.vue'
import PracticeSkill from './components/PracticeSkill.vue'

// 홍길동의 기본 정보
const height = ref(170) // 170cm
const weight = ref(60)  // 60kg

// BMI 계산 (computed로 자동 계산)
const bmi = computed(() => {
  const heightInMeters = height.value / 100
  return Math.round((weight.value / (heightInMeters * heightInMeters)) * 10) / 10
})

// BMI 상태 판정
const bmiStatus = ref('정상')

// watch로 BMI 값 변화를 감시하여 상태 업데이트
watch(bmi, (newBmi) => {
  if (newBmi < 18.5) {
    bmiStatus.value = '저체중'
  } else if (newBmi < 23.0) {
    bmiStatus.value = '정상'
  } else if (newBmi < 25.0) {
    bmiStatus.value = '과체중 - 다이어트 하세요'
  } else {
    bmiStatus.value = '비만 - 다이어트 하세요'
  }
})

// 자식 컴포넌트에서 온 이벤트 처리 함수들
const handleEat = (amount) => {
  weight.value += amount
}

const handlePractice = (amount) => {
  weight.value -= amount
}
</script>