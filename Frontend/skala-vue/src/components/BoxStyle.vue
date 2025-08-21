<template>
  <div>
    <label>
      색상:
      <input v-model="colorInput" placeholder="예: red, blue, green" />
    </label>
    <label>
      사이즈(px):
      <input v-model.number="sizeInput" type="number" placeholder="예: 16, 24" />
    </label>
    <button @click="applyStyle">적용</button>
    <div class="box" :style="boxStyle">
      스타일이 적용되는 박스입니다.
    </div>
  </div>
</template>
<script setup>
import { ref, reactive } from 'vue'
// 사용자 입력값
const colorInput = ref('')
const sizeInput = ref('')
// 박스 스타일 객체
const boxStyle = reactive({
  'background-color': '#F0F0F0',
  padding: '20px',
  border: '1px solid #ccc',
  color: 'black',
  width: '160px',
  height: '160px',
  'border-radius': '10px'
})
// 스타일 적용 함수
function applyStyle() {
  if (colorInput.value) {
    boxStyle.backgroundColor = colorInput.value
  }
  if (sizeInput.value) {
    boxStyle.width = sizeInput.value + 'px'
    boxStyle.height = sizeInput.value + 'px'
  }
}
</script>
<style scoped>
.box {
  margin-top: 20px;
}
</style>