<template>

    <h1>부모 컴포넌트</h1>
    <div>용돈: {{ parentMoney }}</div>

    <label>자식에게 줄 용돈: <input v-model="moneyToChild"></input> </label>
    <button @click="sendMoneyToChild">자식에게 용돈 보내기</button>

    <ChildComp ref="childRef" :moneyFromParent="childMoney" @thanks="onThanks"></ChildComp>

</template>

<script setup>
import { ref } from 'vue';
//ChildComp 는 명칭을 마음대로 변경할 수 있음
import ChildComp from './ChildComp.vue';

const moneyToChild = ref(0);
const childMoney = ref(0);
const parentMoney = ref(10000);
const childRef = ref(null);

function sendMoneyToChild(params) {
    childMoney.value = Number(moneyToChild.value)
    parentMoney.value -= moneyToChild.value

//    childRef.value.takeMoney(childMoney.value);
    childRef.value?.takeMoney(childMoney.value); // ? 붙여서 

    //    moneyToChild.value = 0
    //   setTimeout(() => {
    //     childMoney.value = 0
//   }, 1000);
}

function onThanks(amount) {
  console.log("onThanks", amount);
}
</script>
