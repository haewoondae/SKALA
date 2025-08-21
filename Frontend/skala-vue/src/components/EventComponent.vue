<template>
    <!-- 클릭하면 좌표가 출력되는 버튼 -->
    <!-- <button @click="doclick"> 클릭하세요 </button>
    <div>{{ message }}</div> -->

    <!-- event 인자의 유무 및 차이 -->
    <button @click="onclick('B1', $event)"> 버튼1 </button>
    <button @click="onclick('B2')"> 버튼2 </button>
    <div>{{ message }}</div>

    <div>       
        <input @click="doInput" @keydown.enter="doInput"></input>
    </div>
    <div> {{ message }}</div>

</template>

<script setup>
import { ref } from 'vue'

const message = ref('')

// 버튼 클릭 시 좌표 및 shift 키 상태 출력
function doclick(event) {
    // 누르는 커서의 좌표 및 shift 키 상태 출력
    console.log(event)
    message.value = [event.clientX, event.clientY, event.shiftKey]
}

// 인자의 유무 확인할 수 있는 함수 
function onclick(button, event) {
    // 버튼 클릭 시 메시지 출력
    //event 인자가 없으면 버튼 이름만 출력
    console.log(button, event)
    if (event) {
        message.value = [button, event.clientX, event.clientY, event.shiftKey]
    }
    else {
        message.value = button
    }
}

// input 태그에서 입력된 값 콘솔에 출력
function doInput(event) {
        console.log(event.target.value)
    }

</script>
