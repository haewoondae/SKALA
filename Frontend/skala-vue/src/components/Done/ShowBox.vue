<template>
  <!-- v-if , v-show 활용 개발자 도구에서 확인했을때 나타나는게 다름 -->

  <!-- 버튼을 클릭하면 div의 보임 여부가 토글됩니다. -->
  <button @click="changeVisible">토글</button>

  <!-- template 으로 묶어서 하면 조건에 따라 여러 개의 엘리먼트를 묶어서 나타내는 것을 선택할 수 있음. -->
  <template v-if="isVisible">
    <div>보입니다2.</div>
    <p>나도 보여야해</p>
  </template>
  <div v-else>안보입니다2.</div> <!-- if, else 는 같은 태그에서 선언되지 않아도 되지만 같은 레벨에 있어야함 -->



  <!-- if else 문법은 둘중에 하나만 나타남 -->
  <div v-if="isVisible">보입니다.</div>
  <div v-else>안보입니다.</div>

  <!-- show 의 경우 element는 항상 남아있음 -->
  <div v-show="isVisible">이것도 보입니다.</div>

  <p>메시지: {{ message }}</p>
</template>


<script setup>
import { ref } from 'vue'

//기본값으로 보이도록
const isVisible = ref(true)

const message = ref('안녕하세요')


//토글 함수
function changeVisible() {
  isVisible.value = !isVisible.value
}
</script>