<template>
  <!-- 400x400 크기의 박스 영역 -->
  <div 
    @mousemove="handleMouseMove"
    style="width: 400px; height: 400px; border: 1px solid black; background-color: lightgray;"
  >
    마우스를 이 박스 위에 올려보세요!
  </div>
  
  <!-- 마우스 좌표를 표시할 p 태그 -->
  <p>마우스 좌표: X = {{ mouseX }}, Y = {{ mouseY }}</p>
</template>

<script setup>
// Vue 3의 반응형 데이터를 위한 ref 임포트
import { ref } from 'vue'

// 마우스 X 좌표를 저장할 반응형 변수 (초기값 0)
const mouseX = ref(0)

// 마우스 Y 좌표를 저장할 반응형 변수 (초기값 0)
const mouseY = ref(0)

// 마우스 움직임을 처리하는 함수
const handleMouseMove = (event) => {
  // 이벤트 객체에서 마우스의 현재 좌표를 가져와서
  // 반응형 변수에 저장 (화면에 자동으로 업데이트됨)
  mouseX.value = event.offsetX  // 박스 내에서의 X 좌표
  mouseY.value = event.offsetY  // 박스 내에서의 Y 좌표
}
</script>
