<template>
  <h1> XSS 예제</h1>
  <input v-model="inputmessage"></input> 
  <button @click="showMessage">눌러</button>
  <div> TEXT 출력: {{ outputmessage }}</div>
  <div> HTML 출력: <p v-html="outputmessage"></p></div>
  <a href="url"> 구글 이동</a>
  
</template>

<script setup>
import { ref } from 'vue'

const inputmessage = ref()
const outputmessage = ref()

function showMessage() {
  outputmessage.value = inputmessage.value
}

const url = 'https://www.google.com'

</script>