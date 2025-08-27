<template>
  <div>
    <!-- 탭 선택 버튼 -->
    <button @click="selectTab(TabOne)">Tab 1</button>
    <button @click="selectTab(TabTwo)">Tab 2</button>

    <!-- 선택된 탭 컴포넌트 렌더링 -->
    <KeepAlive>
      <component :is="currentTab" />
    </KeepAlive>
  </div>
</template>

<script setup>
import { ref, markRaw } from "vue";
import TabOne from "./components/TabOne.vue";
import TabTwo from "./components/TabTwo.vue";

// 현재 선택된 탭
const currentTab = ref(markRaw(TabOne));

// 탭 선택 함수
const selectTab = (tab) => {
  currentTab.value = markRaw(tab);
};
</script>