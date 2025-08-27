<template>
  <div>
    <h3>Tab One</h3>
    <input v-model="text" placeholder="텍스트를 입력하세요" />
    <p>입력한 텍스트: {{ text }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, onDeactivated } from "vue";

// 반응형 데이터
const text = ref("");

// 생명주기 훅
onMounted(() => {
  console.log("TabOne Mounted");
});

onActivated(() => {
  console.log("TabOne Activated");
});

onDeactivated(() => {
  console.log("TabOne Deactivated");
});
</script>