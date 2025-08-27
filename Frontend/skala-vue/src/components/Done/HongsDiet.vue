<template>
  <h1>홍길동의 다이어트 챌린지</h1>
  <h4>키: {{ height }}</h4>
  <h4>몸무게: {{ weight }}</h4>
  <div>BMI: {{ bmi.toFixed(2) }}, 판정: {{ bmiMessage }}</div>

  <!-- 다이어트 습관 컴포넌트 -->
  <HongsDietHabit title="음식 먹기" :habits="eatHabits" @weightChanged="addWeight" />
  <HongsDietHabit title="체력 단련" :habits="trainHabits" @weightChanged="addWeight" />
</template>

<script setup>
import { ref, computed, watch } from "vue";
import HongsDietHabit from "./HongsDietHabit.vue";

// 키와 몸무게
const height = ref(170);
const weight = ref(60);

// 다이어트 습관 데이터
const eatHabits = [
  { name: "햄버거", weight: 1 },
  { name: "피자", weight: 2 },
  { name: "떡볶이", weight: 1.5 },
];
const trainHabits = [
  { name: "걷기", weight: -1 },
  { name: "달리기", weight: -2 },
];

// BMI 계산
const bmi = computed(() => weight.value / ((height.value / 100) ** 2));
const bmiMessage = ref("");

// BMI 판정 기준
watch(bmi, (newBmi) => {
  if (newBmi < 18.5) {
    bmiMessage.value = "저체중";
  } else if (newBmi < 23) {
    bmiMessage.value = "정상";
  } else if (newBmi < 25) {
    bmiMessage.value = "과체중";
  } else {
    bmiMessage.value = "비만";
  }
}, { immediate: true });

// 몸무게 변경 함수
function addWeight(w) {
  weight.value += w;
}
</script>