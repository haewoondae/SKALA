<template>
    <h1 class="bgOrange" :class="color">스타일 클래스 바인딩</h1>
    <div>
        <button @click="changeColor('red')">빨강</button>
        <button @click="changeColor('blue')">파랑</button>
    </div>

</template>

<script setup>
import { ref } from 'vue'

const color = ref('') //let 으로 선언해도 상관없음 하지만 다른 곳에서 color을 사용하면 오류 발생가능

function changeColor(param) {
    color.value = param
    // color=
}

</script>

<style>
.red {
    color: red;
}

.blue {
    color: blue;
}   

.bgOrange {
    background-color: orange;
}
</style>