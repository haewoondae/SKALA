<template>

    <div> {{ JSON.stringify($props) }}</div>

</template>

<script setup>
import {ref, reactive, isReactive} from 'vue'

function toJsonString(value) {

    let anything = value

    if (isRef(value)) {
        anything = unref(value)
    }

    if (isReactive(value)) {
        anything = toRaw(value)
    }

    return JSON.stringify(anything)
}
const primitive = 123
const obj = { name: 'John', age: 30 }
const arr = [1, 2, 3]
const r1 = ref({ city: 'Seoul' })
const r2 = reactive({ job: 'Developer' })

console.log(toJsonString(num), toJsonString(obj), toJsonString(arr), toJsonString(r1), toJsonString(r2))

</script>