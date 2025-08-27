<template>
  <h1>{{ title }}</h1>

  <!-- 습관 목록 출력 -->
  <div>
    <button v-for="(habit, index) in habits" :key="index" @click="changeWeight(habit.weight)">
      {{ habit.name }} ({{ habit.weight > 0 ? "+" + habit.weight : habit.weight }}kg)
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

// 컴포넌트 props 정의
const props = defineProps({
  title: String,
  habits: Array, // { name: "햄버거", weight: 1 }
});

// 부모 컴포넌트로 이벤트 전달
const emit = defineEmits(["weightChanged"]);
function changeWeight(weight) {
  console.log(weight);
  emit("weightChanged", weight);
}
</script>
