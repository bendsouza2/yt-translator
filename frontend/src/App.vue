<template>
  <div id="app">
    <router-view class="big-title"/>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.big-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
</style>