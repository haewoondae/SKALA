<template>
  <div class="box" @mousemove="updateCoords" @mouseleave="clearCoords">
  </div>
  <p>마우스 좌표: X: {{ x }}, Y: {{ y }}</p>
</template>
<script setup>
import { ref } from 'vue'
// 좌표값을 반응형 변수로 선언
const x = ref(0)
const y = ref(0)
// 마우스 이동 이벤트 핸들러

function updateCoords(event) {
  //박스 안에 마우스가 위치하면 좌표 반환
    x.value = event.offsetX   // 박스 내부 기준 좌표
    y.value = event.offsetY
}

function clearCoords() {
  x.value = 0
  y.value = 0
}
</script>
<style scoped>
.box {
  width: 400px;
  height: 400px;
  background-color: #F2F2F2;
  border: 1px solid #aaa;
  margin: 0 auto;
}
p {
  text-align: center;
  margin-top: 10px;
}
</style>