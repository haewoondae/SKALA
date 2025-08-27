<template>
	<div>
		<p>{{ 1 + 2 }}</p>
		<p>{{ message + ' !' }}</p>
		<p>{{ price * quantity }}</p>
		<p>{{ isLogin ? ' ' : ' ' }}</p>
	</div>
</template>


<script setup>
const message = ' '
const price = 5000
const quantity = 3
const isLogin = true
</script>