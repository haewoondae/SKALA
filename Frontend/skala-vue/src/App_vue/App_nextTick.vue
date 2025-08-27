<template>
  <ChildComp>
    <template #bottom>
      <HongsDiet></HongsDiet>
    </template>
  </ChildComp>
</template>

<script setup>
import ChildComp from './components/slot/ChildComp.vue';
import HongsDiet from './components/HongsDiet.vue'

</script> 