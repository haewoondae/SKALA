<template>
    <h1>아들</h1>
    <div>용돈: {{ money }}</div>
</template>


<script setup>
import { ref, watch } from "vue"

const emit = defineEmits(['thanks'])
const props = defineProps({ moneyFromParent: Number })

const money = ref(1000)

// watch(props, () => {
//   console.log("자식", props.moneyFromParent)

//   if (props.moneyFromParent) {
//     money.value += props.moneyFromParent
//     emit('thanks', money.value)
//   }
// })

function takeMoney(moneyFromParent) {
  money.value += moneyFromParent
  emit('thanks', money.value)
}

defineExpose({
    takeMoney
})
</script>






