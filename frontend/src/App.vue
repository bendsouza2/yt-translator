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
.big-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
</style>
