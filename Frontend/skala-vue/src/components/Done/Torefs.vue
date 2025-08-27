<template>
  <div>이름 : {{ user.name }}</div>
  <div>나이 : {{ user.age }}</div>

  <hr />

  <!-- 사용자 정보 입력 -->
  <input v-model="name" />
  <input v-model="age" />
</template>

<script setup>
import { reactive, toRef, toRefs } from "vue";

// 사용자 정보 객체
const user = reactive({
  name: "홍길동",
  age: 25,
});

const {name, age} = toRefs(user);

//만약 toRef를 사용하고 싶다면
// const name = toRef(user, 'name');
// const age = toRef(user, 'age');
</script>