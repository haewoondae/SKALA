<template>
  <div>
    <h2>BMI 계산기</h2>

    <!-- 키 입력 -->
    <div>
      <label for="height">키(cm): </label>
      <input 
        id="height"
        type="number" 
        v-model.number="height" 
        placeholder="키를 입력하세요"
      />
    </div>

    <!-- 체중 입력 -->
    <div>
      <label for="weight">체중(kg): </label>
      <input 
        id="weight"
        type="number" 
        v-model.number="weight" 
        placeholder="체중을 입력하세요"
      />
    </div>

    <!-- BMI 결과 표시 -->
    <div>
      <p>BMI 지수: {{ bmi }}</p>
      <p>판정: {{ bmiStatus }}</p>
    </div>
  </div>
</template>

<script setup>
// Vue 3의 반응형 데이터와 계산된 속성 임포트
import { ref, computed, watch } from 'vue'

// 키와 체중 반응형 데이터
const height = ref(170)  // 초기값: 170cm
const weight = ref(60)   // 초기값: 60kg

// BMI 계산 (computed로 자동 계산)
// BMI = 체중(kg) / (키(m) * 키(m))
const bmi = computed(() => {
  if (height.value > 0 && weight.value > 0) {
    const heightInMeters = height.value / 100 // 키를 미터로 변환
    return Math.round((weight.value / (heightInMeters * heightInMeters)) * 10) / 10 // 소수점 첫째자리까지 표시
  }
  return 0 // 유효하지 않은 값일 경우 0 반환
})

// BMI 상태 판정
const bmiStatus = ref('정상')

// BMI 값 변화를 감시하여 상태 업데이트
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
</script>
