<template>
  <div class="background-container">
    <TopContent
      :is-spanish="isSpanish"
      :translations="translations"
      :current-video="currentVideo"
      @toggle-language="toggleLang" 
    />
    <VideoCarousel
      :videos="videos"
      :current-index="currentIndex"
      :is-spanish="isSpanish"
      :translations="translations"
      :flipped-states="flippedStates"
      :revealed-states="revealedStates"
      @next-video="nextVideo"
      @previous-video="previousVideo"
      @flip-button="flipButton"
      @reveal-sentence="revealSentence"
    />
    <p v-if="loading">Loading videos...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import TopContent from "./TopContent.vue";
import VideoCarousel from "./VideoCarousel.vue";
import { useVideoManager } from "../composables/useVideoManager";
import { useLanguageTranslation } from "../composables/useLanguageTranslation";

const videos = ref([]);
const currentIndex = ref(0);
const loading = ref(true);
const flippedStates = ref({});
const revealedStates = ref({});
const isSpanish = ref(false);

const translations = {
  title: {
    en: "Spanish Word of the Day",
    es: "Palabra Del Día"
  },
  flipButton: {
    en: "Word of the Day!",
    es: "Palabra del Día!"
  },
  seeSentence: {
    en: "See an example in Spanish",
    es: "Ver un ejemplo en español"
  },
  revealTranslation: {
    en: "Reveal the English translation",
    es: "Ver la traducción al inglés"
  },
  switchLanguage: {
    en: "Switch to Spanish",
    es: "Cambiar al inglés"
  },
  exampleUsage: {
    en: "Example Usage",
    es: "Ejemplo de Uso"
  }
};

const { fetchVideos } = useVideoManager(videos, loading, flippedStates, revealedStates);
const { toggleLanguage, translateDate } = useLanguageTranslation();

const currentVideo = computed(() => {
  return videos.value[currentIndex.value] || {};
});

function nextVideo() {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
}

function previousVideo() {
  if (currentIndex.value < videos.value.length - 1) {
    currentIndex.value++;
  }
}

function flipButton(index) {
  flippedStates.value[index] = !flippedStates.value[index];
}

function revealSentence(index, sentenceName) {
  if (!revealedStates.value[index]) {
    revealedStates.value[index] = {};
  }
  revealedStates.value[index][sentenceName] = !revealedStates.value[index][sentenceName];
}

function toggleLang() {
  toggleLanguage(isSpanish); 
}

onMounted(fetchVideos);
</script>

<style scoped>
.background-container {
  background-image: linear-gradient(to right, #3b3933, rgb(66, 46, 1));
  background-size: cover;
  padding: 20px;
  height: 100%;
  width: 100%;
}

.top-content {
  color: #ffffff;
  padding: 20px;
  margin-bottom: 20px;
  text-align: center;
  width: 100vw;
  box-sizing: border-box;
  border-bottom: 1px solid #6f6f6f;
  background-color: rgba(45, 45, 45, 0.5);
  background-size: cover;
  position: relative;
  margin-left: -50vw;
  margin-right: -50vw;
  margin-top: -20px;
}

.top-content h1,
.top-content h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.top-content h1 {
  color: #E5A00D;
  margin-bottom: 5px;
}

.top-content h2 {
  color: #807f7c;
  margin-bottom: 5px;
}

.video-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 20px;
}

.video-container iframe {
  max-width: 100%;
  height: 560px;
  max-height: 100%;
  border-radius: 10px;
  margin: 0 auto;
}

@keyframes animate {
  0% {
    filter: hue-rotate(0deg);
  }
  50% {
    filter: hue-rotate(360deg);
  }
  100% {
    filter: hue-rotate(0deg);
  }
}
</style>