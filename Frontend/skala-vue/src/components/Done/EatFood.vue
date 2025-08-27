<template>
  <div> 
    <label>🍔 음식 먹기</label>
    <button @click="eatFood(1)">햄버거 먹기 (+1kg)</button>
    <button @click="eatFood(2)">피자 먹기 (+2kg)</button>
  </div>
</template>

<script setup>
// 부모에게 보낼 이벤트 정의
const emit = defineEmits(['eat'])

// 음식 먹기 함수
const eatFood = (amount) => {
  // 부모에게 'eat' 이벤트와 함께 증가할 체중량 전달
  emit('eat', amount)
}
</script>
