<!-- UploadTimer.vue -->
<template>
    <div class="timer-wrapper">
      <div class="english-text-container">
        <span 
          v-for="(word, index) in englishWords" 
          :key="`en-${index}`"
          :class="{ 'visible': visibleEnglishWords[index] }"
          class="animated-word"
        >
          {{ word }}
        </span>
      </div>
      <div class="countdown-timer">
        <div class="timer-display">
          <div class="digit-group">
            <!-- Hours -->
            <div class="digit-container" v-for="(digit, index) in timerDigits.slice(0, 2)" :key="`h${index}`">
              <div class="digit" :class="{ 'spinning': isSpinning }">
                <div class="digit-prev">{{ getPrevDigit(digit) }}</div>
                <div class="digit-current">{{ digit }}</div>
                <div class="digit-next">{{ getNextDigit(digit) }}</div>
              </div>
            </div>
            <span class="separator">:</span>
            
            <!-- Minutes -->
            <div class="digit-container" v-for="(digit, index) in timerDigits.slice(2, 4)" :key="`m${index}`">
              <div class="digit" :class="{ 'spinning': isSpinning }">
                <div class="digit-prev">{{ getPrevDigit(digit) }}</div>
                <div class="digit-current">{{ digit }}</div>
                <div class="digit-next">{{ getNextDigit(digit) }}</div>
              </div>
            </div>
            <span class="separator">:</span>
            
            <!-- Seconds -->
            <div class="digit-container" v-for="(digit, index) in timerDigits.slice(4, 6)" :key="`s${index}`">
              <div class="digit" :class="{ 'spinning': isSpinning }">
                <div class="digit-prev">{{ getPrevDigit(digit) }}</div>
                <div class="digit-current">{{ digit }}</div>
                <div class="digit-next">{{ getNextDigit(digit) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="spanish-text-container">
        <span 
          v-for="(word, index) in spanishWords" 
          :key="`es-${index}`"
          :class="{ 'visible': visibleSpanishWords[index] }"
          class="animated-word"
        >
          {{ word }}
        </span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, computed } from "vue";
  
  const props = defineProps({
    isSpanish: {
      type: Boolean,
      default: false
    }
  });
  
  const emit = defineEmits(['timerComplete']);
  
  const countdown = ref({
    hours: 0,
    minutes: 0,
    seconds: 0
  });
  
  const isSpinning = ref(true);
  const englishWords = ref(['Next', 'word', 'in:']);
  const spanishWords = ref(['Hasta', 'la', 'próxima', 'palabara']);
  const visibleEnglishWords = ref(Array(englishWords.value.length).fill(false));
  const visibleSpanishWords = ref(Array(spanishWords.value.length).fill(false));
  const isAnimatingEnglish = ref(true);
  
  let interval;
  
  const timerDigits = computed(() => {
    const hours = String(countdown.value.hours).padStart(2, '0');
    const minutes = String(countdown.value.minutes).padStart(2, '0');
    const seconds = String(countdown.value.seconds).padStart(2, '0');
    return [...hours, ...minutes, ...seconds];
  });
  
  function getNextNoon() {
    const now = new Date();
    const nextNoon = new Date();
    nextNoon.setHours(12, 0, 0, 0);
    if (now >= nextNoon) {
      nextNoon.setDate(nextNoon.getDate() + 1);
    }
    return nextNoon;
  }
  
  function getPrevDigit(digit) {
    return digit === '0' ? '9' : String(Number(digit) - 1);
  }
  
  function getNextDigit(digit) {
    return digit === '9' ? '0' : String(Number(digit) + 1);
  }
  
  function getTargetCountdown() {
    const now = new Date().getTime();
    const nextUpload = getNextNoon().getTime();
    const timeDistance = nextUpload - now;
  
    return {
      hours: Math.floor(timeDistance / (1000 * 60 * 60)),
      minutes: Math.floor((timeDistance % (1000 * 60 * 60)) / (1000 * 60)),
      seconds: Math.floor((timeDistance % (1000 * 60)) / 1000),
    };
  }
  
  async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  function startSpinningAnimation(targetCountdown) {
    const duration = 1200;
    const steps = 10;
    const stepDuration = duration / steps;
    
    let currentStep = 0;
    const spinInterval = setInterval(() => {
      currentStep++;
      
      countdown.value = {
        hours: Math.floor((targetCountdown.hours * currentStep) / steps),
        minutes: Math.floor((targetCountdown.minutes * currentStep) / steps),
        seconds: Math.floor((targetCountdown.seconds * currentStep) / steps),
      };
  
      if (currentStep >= steps) {
        clearInterval(spinInterval);
        isSpinning.value = false;
        interval = setInterval(updateCountdown, 1000);
      }
    }, stepDuration);
  }
  
  function updateCountdown() {
    const targetCountdown = getTargetCountdown();
    
    if (isSpinning.value) {
      startSpinningAnimation(targetCountdown);
    } else {
      countdown.value = targetCountdown;
      
      if (targetCountdown.hours === 0 && 
          targetCountdown.minutes === 0 && 
          targetCountdown.seconds === 0) {
        clearInterval(interval);
        isSpinning.value = true;
        emit('timerComplete');
      }
    }
  }
  
  async function animateText() {
    while (true) {
      if (isAnimatingEnglish.value) {
        visibleSpanishWords.value = Array(spanishWords.value.length).fill(false);
        
        for (let i = 0; i < englishWords.value.length; i++) {
          visibleEnglishWords.value[i] = true;
          await sleep(300);
        }
        
        await sleep(2000);
        visibleEnglishWords.value = Array(englishWords.value.length).fill(false);
      } else {
        visibleEnglishWords.value = Array(englishWords.value.length).fill(false);
        
        for (let i = 0; i < spanishWords.value.length; i++) {
          visibleSpanishWords.value[i] = true;
          await sleep(300);
        }
        
        await sleep(2000);
        visibleSpanishWords.value = Array(spanishWords.value.length).fill(false);
      }
      
      isAnimatingEnglish.value = !isAnimatingEnglish.value;
      await sleep(500);
    }
  }
  
  onMounted(() => {
    updateCountdown();
    animateText();
  });
  
  onUnmounted(() => {
    if (interval) {
      clearInterval(interval);
    }
  });
  </script>
  
<style scoped>
.countdown-timer {
    font-family: Arial, sans-serif;
    color: #ffffff;
    text-align: center;
    padding: 10px;
    font-size: clamp(16px, 5vw, 30px);
}

.english-text-container {
    justify-content: center;
    color: #ffffff;
    font-size: clamp(20px, 5vw, 20px);
    font-family: Arial, sans-serif;
    padding-bottom: 20px;
    display: flex;
    gap: 8px;
}

.spanish-text-container {
    justify-content: center;
    color: #ff8f33;
    font-size: clamp(20px, 5vw, 20px);
    font-family: Arial, sans-serif;
    padding-top: 20px;
    display: flex;
    gap: 8px;
}

.animated-word {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s ease-out, transform 0.3s ease-out;
}

.animated-word.visible {
    opacity: 1;
    transform: translateY(0);
}

.background-container {
    background-image: linear-gradient(to right, #3b3933 , rgb(66, 46, 1));
    background-size: cover;
    min-height: 100vh;
    width: 100%;
    margin: 0;
    padding: 0;
    display: flex; 
    justify-content: center;
}

.timer-display {
    display: flex;
    justify-content: center;
    perspective: 400px;
}

.digit-group {
    display: flex;
    align-items: center;
}

.digit-container {
    width: 1em;
    height: 1.2em;
    position: relative;
    margin: 0 1px;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
}

.digit {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.3s ease-out;
}

.digit.spinning {
    animation: spinDigit 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.digit-prev,
.digit-current,
.digit-next {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.digit-prev {
    transform: rotateX(90deg) translateZ(0.6em);
}

.digit-current {
    transform: rotateX(0deg) translateZ(0.6em);
}

.digit-next {
    transform: rotateX(-90deg) translateZ(0.6em);
}

.separator {
    margin: 0 0.2em;
    font-weight: bold;
}

@keyframes spinDigit {
    0% {
        transform: rotateX(0deg);
    }
    100% {
        transform: rotateX(-360deg);
    }
}
</style>