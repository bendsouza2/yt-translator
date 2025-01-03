<template>
    <div class="background-container">
    <div class="countdown-timer">
      <p>Next video upload in:</p>
      <p>
        {{ countdown.hours }} hours, {{ countdown.minutes }} minutes, {{ countdown.seconds }} seconds
      </p>
    </div>
</div>
</template>
  
<script setup lang="ts">
/* eslint-disable */
import { ref, onMounted, onUnmounted } from "vue";
  
/**
 * Calculates the next occurrence of noon (12pm UTC).
 * @returns {Date} - A Date object representing the next noon.
 */
function getNextNoon() {
    const now = new Date();
    const nextNoon = new Date();
  
    nextNoon.setHours(12, 0, 0, 0); 
    if (now >= nextNoon) {
      nextNoon.setDate(nextNoon.getDate() + 1); 
    }
    return nextNoon;
  }
  
const countdown = ref({
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

// eslint-disable-next-line
let interval: ReturnType<typeof setInterval> | undefined = undefined;
  
/**
 * Get a countdown to the next upload time (12pm UTC).
 * @param {Function} callback - A function to handle the countdown values.
 */
function updateCountdown() {
    const now = new Date().getTime();
    const nextUpload = getNextNoon().getTime();
  
    const timeDistance = nextUpload - now;
    if (timeDistance <= 0) {
      clearInterval(interval); 
      countdown.value = { hours: 0, minutes: 0, seconds: 0 };
      return;
    }
  
    countdown.value.hours = Math.floor(
      (timeDistance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    countdown.value.minutes = Math.floor(
      (timeDistance % (1000 * 60 * 60)) / (1000 * 60)
    );
    countdown.value.seconds = Math.floor((timeDistance % (1000 * 60)) / 1000);
  }
  

onMounted(() => {
    updateCountdown(); 
    interval = setInterval(updateCountdown, 1000); 
  });
  
  onUnmounted(() => {
  if (interval !== undefined) {
    clearInterval(interval);
  }
});
</script>
  
<style scoped>
.countdown-timer {
    font-family: Arial, sans-serif;
    color: #444;
    text-align: center;
    padding: 10px;
}

.background-container {
  background-image: linear-gradient(to right, #3b3933 , rgb(66, 46, 1));
  background-size: cover;
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
  