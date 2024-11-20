<template>
  <div id="app">
    <VideoDetails class="big-title"/>
  </div>
</template>

<script>
import VideoDetails from "./components/LatestVideo.vue";

export default {
  components: {
    VideoDetails,
  },
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
