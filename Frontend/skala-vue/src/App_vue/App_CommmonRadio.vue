<template>
  <div>
    <!-- 성별 선택 라디오 버튼 -->
    <CommonRadio :options="genderOptions" v-model="gender" />

    <!-- 학교 선택 라디오 버튼 -->
    <CommonRadio :options="schoolOptions" v-model="school" disabled />

    <!-- 입력값 출력 버튼 -->
    <button class="btn btn-primary" @click="showInput">보이기</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CommonRadio from "./components/Done/CommonRadio.vue";

// 성별 데이터
const gender = ref("m");
const genderOptions = ref([
  { label: "남", value: "m" },
  { label: "여", value: "f" },
]);

// 학교 데이터
const school = ref("03");
const schoolOptions = ref([
  { label: "초등학교", value: "01" },
  { label: "중학교", value: "02" },
  { label: "고등학교", value: "03" },
  { label: "대학교", value: "04" },
]);

// 입력값 출력 함수
function showInput() {
  console.log("Gender:", gender.value);
  console.log("School:", school.value);
}
</script>