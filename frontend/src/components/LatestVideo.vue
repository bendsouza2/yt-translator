<template>
  <div class="background-container">
    <div class="top-content">
      <h1>Spanish Word of the Day</h1>
      <h2 v-if="currentVideo.upload_time">{{ currentVideo.upload_time }}</h2>
    </div>

    <div class="carousel-container">
      <button 
        class="nav-button prev" 
        @click="previousVideo" 
        :disabled="currentIndex === videos.length - 1"
        v-show="currentIndex < videos.length - 1"
      >
        ‹
      </button>

      <div class="videos-container" ref="videosContainer">
        <div 
          v-for="(video, index) in videos" 
          :key="video.video_id"
          :class="['video-wrapper', {
            'current': index === currentIndex,
            'prev': index === currentIndex + 1, // Older videos (higher index) appear left
            'next': index === currentIndex - 1  // Newer videos (lower index) appear right
          }]"
        >
        <div class="video-content">
            <!-- Added overlay div for non-current videos -->
            <div 
              v-if="index !== currentIndex" 
              class="video-overlay"
              aria-hidden="true"
            ></div>
            
            <iframe
              :src="`https://www.youtube.com/embed/${video.video_id}?rel=0`"
              width="315"
              height="560"
              frameborder="0"
              allowfullscreen
            ></iframe>

            <!-- Interactive elements only shown for current video -->
            <div 
              v-if="index === currentIndex" 
              class="interactive-elements"
            >
              <div 
                :class="['flip-button', { flipped: flippedStates[index] }]" 
                @click="flipButton(index)"
              >
                <div class="front">Word of the Day!</div>
                <div class="back">{{ video.word }}</div>
              </div>

              <div class="sentence-container">
                <div class="sentence-title">
                  <strong>Example Usage</strong>
                </div>
                <div 
                  :class="['sentence spanish-sentence', { hovered: revealedStates[index]?.sentenceSpanish }]"
                  @click="revealSentence(index, 'sentenceSpanish')"
                >
                  <div v-if="!revealedStates[index]?.sentenceSpanish" class="front">See an example in Spanish</div>
                  <div v-if="revealedStates[index]?.sentenceSpanish" class="back">{{ video.sentence }}</div>
                </div>
                <div
                  :class="['sentence english-sentence', { hovered: revealedStates[index]?.sentenceEnglish }]"
                  @click="revealSentence(index, 'sentenceEnglish')"
                >
                  <div v-if="!revealedStates[index]?.sentenceEnglish" class="front">Reveal the English translation</div>
                  <div v-if="revealedStates[index]?.sentenceEnglish" class="back">{{ video.translated_sentence }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button 
        class="nav-button next" 
        @click="nextVideo" 
        :disabled="currentIndex === 0"
        v-show="currentIndex > 0"
      >
        ›
      </button>
    </div>
    <p v-if="loading">Loading videos...</p>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import axios from "axios";

const videos = ref([]);
const currentIndex = ref(0);
const loading = ref(true);
const flippedStates = ref({});
const revealedStates = ref({});

const currentVideo = computed(() => {
  return videos.value[currentIndex.value] || {};
});

async function fetchVideos() {
  try {
    const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
    const response = await axios.get(`${apiBaseUrl}today/videos/paginated-videos/`, {
      params: {
        limit: 7,
        page_num: 1
      }
    });

    if (response.data?.videos) {
      videos.value = response.data.videos.map(video => ({
        ...video,
        upload_time: formatDate(new Date(video.upload_time))
      }));
      
      videos.value.forEach((_, index) => {
        flippedStates.value[index] = false;
        revealedStates.value[index] = {
          sentenceSpanish: false,
          sentenceEnglish: false
        };
      });
    }
  } catch (error) {
    console.error("Error fetching videos:", error);
  } finally {
    loading.value = false;
  }
}

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

function formatDate(date) {
  const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  const formattedDate = new Intl.DateTimeFormat("en-GB", options).format(date);
  const day = date.getDate();

  const ordinalSuffix = (n) => {
    const s = ["th", "st", "nd", "rd"];
    const v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  };

  const dayWithOrdinal = ordinalSuffix(day);
  return formattedDate.replace(/\d+/, dayWithOrdinal);
}

onMounted(fetchVideos);
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.videos-container {
  display: flex;
  position: relative;
  width: 315px;
  height: 900px;
  overflow: visible;
}

.video-wrapper {
  position: absolute;
  width: 100%;
  transition: all 0.5s ease;
  opacity: 0;
  transform: translateX(100%); /* Default position is off-screen to the right */
}

.video-wrapper.current {
  opacity: 1;
  transform: translateX(0);
  z-index: 2;
}

.video-wrapper.prev {
  opacity: 0.2;
  transform: translateX(-90%); /* Older videos appear to the left */
  z-index: 1;
}

.video-wrapper.next {
  opacity: 0.2;
  transform: translateX(90%); /* Newer videos appear to the right */
  z-index: 1;
}

.nav-button {
  position: absolute;
  top: 280px; /* Centered with the video - adjusted from 50% */
  background: rgba(229, 160, 13, 0.8);
  border: none;
  color: white;
  padding: 20px 15px;
  cursor: pointer;
  border-radius: 25px;
  font-size: 24px;
  z-index: 3;
  transition: all 0.3s ease;
}

.nav-button:hover {
  background: rgba(229, 160, 13, 1);
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-button.prev {
  left: 10px;
}

.nav-button.next {
  right: 10px;
}

.interactive-elements {
  margin-top: 10px;
  min-height: 300px
}

.video-content {
  position: relative; /* Added to contain the overlay */
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 560px; /* Same as video height */
  background: transparent;
  z-index: 10; /* Ensure it's above the iframe but below the navigation buttons */
  cursor: default;
}

.background-container {
  background-image: linear-gradient(to right, #3b3933 , rgb(66, 46, 1));
  background-size: cover;
  padding: 20px;
  height: 100%;
  width: 100%;
}

.top-content {
  /* background: #333; */
  color: #ffffff;              
  padding: 20px;              
  margin-bottom: 20px;        
  /* border-radius: 10px;  */
  text-align: center;         
  width: 100%;                
  box-sizing: border-box;     
  border-bottom: 1px solid #E5A00D;
}

.top-content h1, .top-content h2 {
  margin: 0;                  
  font-size: 24px;             
  font-weight: bold;           
}

.top-content h1 {
  color: #E5A00D;
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

.sentence-container {
  background: #333;
  color: #f4d689;
  border-radius: 15px;
  padding: 0px 0px 10px;
  margin-top: 20px;
  min-width: 315px;
}

.sentence-title {
  background: #2d2d2d;
  position: relative;
  color: white;
  padding: 10px;
  font-size: 18px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.sentence {
  background: #333;
  color: white;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
}

.spanish-sentence {
  border-bottom: 5px solid #3d3d3d;
  cursor: pointer;
  transition: background 0.3s ease;
}

.spanish-sentence:hover {
  background: #E5A00D;
  color: #333;
}

.english-sentence {
  background: #333;
  color: white;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.english-sentence:hover {
  background: #E5A00D;
  color: #333;
}

.reveal-sentence .front,
.reveal-sentence .back {
  position: absolute;
  display: flex;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  justify-content: center;
  text-align: center;
  align-items: center;
  font-weight: bold;
  font-size: clamp(16px, 5vw, 30px);
  line-height: 20px;
  border-radius: 50px;
}

.reveal-sentence .front {
  background: black;
  color: rgb(137, 128, 128);
  transition: all 0.5s ease-out;
}

.reveal-sentence .back {
  background: #333;
  color: white;
  font-size: smaller;
  text-wrap-style: pretty;
  transform: translateX(100%);
  transition: transform 1s ease-out;
  backface-visibility: hidden;
}

.reveal-sentence.revealed .front {
  background: transparent;
  color: transparent;
}

.reveal-sentence.revealed .back {
  transform: translateX(0%);
}

.example-usage {
  width: 300px;
  height: 90px;
  display: flex;
  position: relative;
  margin-top: 5px;
  overflow: hidden;
  padding-left: 10px;
  padding-right: 10px;
  background: #333;
  color: #f4d689;
  border-radius: 50px;
  text-align: center;
  align-items: center;
  justify-content: center;
}

.flip-button {
  width: 315px;
  height: 50px;
  background: #E5A00D;
  color: white;
  font-size: 16px;
  text-align: center;
  line-height: 50px;
  cursor: pointer;
  display: inline-block;
  perspective: 1000px; 
  border: none; 
  border-radius: 50px; 
  outline: none; 
  transform-style: preserve-3d;
  transition: transform 0.5s ease-in-out;
  margin-top: 10px;
}

.flip-button button {
  display: block;
  backface-visibility: hidden;
}

.flip-button .front {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #E5A00D;
  color: white;
  text-align: center;
  line-height: 50px;
  border-radius: 50px;
  color: #333;
  font-weight: bold;
}

.flip-button .back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #333;
  color: #E5A00D;
  text-align: center;
  line-height: 50px;
  transform: rotateY(180deg);
  backface-visibility: hidden;
  border-radius: 50px;
  font-weight: bold;
}

.flip-button.flipped {
  transform: rotateY(180deg);
}

.flip-button .front:hover {
  display: ruby-text-container;
}
</style>