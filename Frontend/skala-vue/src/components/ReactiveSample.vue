<template>
  <div>
    <p>과일 목록: {{ items.join(', ') }}</p>
    <button @click="addFruit">과일 추가</button>
    <hr>
    </hr>

    <p>인물: {{ person.name }} - {{ person.age }} 세</p>
    <button @click="increaseAge">나이 증가</button>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

//아래 3개는 reactive 로 선언할 수 없음 (primitive 하기 때문에)
// const count = ref(0)
// const name = ref('홍길동')
// const isActive = ref(true)

const fruits = ref(['사과', '배'])
const items = reactive(['사과', '배'])
const person = reactive({ name: '홍길동', age: 20 })

function addFruit() {
  // items.push('귤') 대신 아래와 같이 작성
  console.log(fruits, items)
  items.push('귤')
}

function increaseAge() {
  person.age++
}

</script>