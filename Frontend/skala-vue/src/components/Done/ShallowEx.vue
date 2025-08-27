<template>
  <!-- 사용자 정보 출력 -->
  <div>이름 : {{ userRef.name }}</div>
  <div>주소.도시 : {{ userRef.address.city }}</div>

  <hr />

  <!-- 이름 변경 입력 및 버튼 -->
  <input v-model="name" placeholder="새 이름 입력" />
  <button @click="updateName">이름 변경</button>

  <!-- 도시 변경 입력 및 버튼 -->
  <input v-model="city" placeholder="새 도시 입력" />
  <button @click="updateCity">도시 변경</button>
</template>

<script setup>
import { shallowReactive, ref } from "vue";

// 입력 필드 값 관리
const name = ref("");
const city = ref("");

// 사용자 정보 객체 (shallowReactive 사용)
const userRef = shallowReactive({
  name: "홍길동",
  address: {
    city: "서울",
    zip: "12345", // 우편번호
  },
});

// 이름 변경 함수
function updateName() {
  userRef.name = name.value;
}

// 도시 변경 함수
function updateCity() {
  userRef.address.city = city.value;
}
</script>