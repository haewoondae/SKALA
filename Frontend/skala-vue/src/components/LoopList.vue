<template>

    <ul> <!-- 순서 없는 리스트 -->
        <!-- <li v-for="fruit in fruits">{{ fruit }}</li> -->
        <li v-for="(fruit, index) in fruits" :key="index">{{ index }}: {{ fruit }}</li>    </ul>

    <hr>
    </hr>

    <!-- 과일 추가 입력란 -->
    <input v-model="inputFruit"></input>
    <button @click="addFruit">추가</button>

    

</template>


<script setup>
//vue 의 기능을 사용해서 실시간으로 화면에 나타나게 하기 위해서 ref 를 사용
import { ref } from 'vue'


// 과일 리스트
//const fruits = ['바나나', '사과', '포도'] ref 안쓸때
const fruits = ref(['바나나', '사과', '포도'])

const inputFruit = ref('')

// 과일 추가 함수 , 하지만 이 방법으로는 콘솔이 아닌 화면에서는 추가된 과일이 나타나지 않음
function addFruit() {
  //const inputFruit = document.getElementById('inputFruit') // inputFruit 을 입력 값으로 받아서 저장 (ref 안쓸때)
  console.log(inputFruit.value) // 입력 값 확인
  fruits.value.push(inputFruit.value) // fruits 배열에 추가

  console.log(fruits)           // fruits 배열 확인
}

</script>