<template>
  <div>
    <h3>Tab Two</h3>
    <p>다른 탭입니다.</p>
  </div>
</template>

<script setup>
import { onMounted, onActivated } from "vue";

// 생명주기 훅
onMounted(() => {
  console.log("TabTwo Mounted");
});

onActivated(() => {
  console.log("TabTwo Activated");
});
</script>