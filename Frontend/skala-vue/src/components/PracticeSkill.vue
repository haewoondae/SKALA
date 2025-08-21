<template>
  <div> 
    <label>🏃 기술 연습</label>
    <button @click="practiceSkill(1)">걷기 (-1kg)</button>
    <button @click="practiceSkill(2)">달리기 (-2kg)</button>
  </div>
</template>

<script setup>
// 부모에게 보낼 이벤트 정의
const emit = defineEmits(['practice'])

// 기술 연습 함수
const practiceSkill = (amount) => {
  // 부모에게 'practice' 이벤트와 함께 감소할 체중량 전달
  emit('practice', amount)
}
</script>
