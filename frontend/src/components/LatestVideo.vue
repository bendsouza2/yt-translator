<template>
  <div class="background-container">
    <div class="top-content">
      <h1>Spanish Word of the Day</h1>
      <h2 v-if="video.upload_date">{{ video.upload_date }}</h2>
    </div>

    <div v-if="video.video_id" class="video-container">
      <iframe
        :src="`https://www.youtube.com/embed/${video.video_id}`"
        width="315"
        height="560"
        frameborder="0"
        allowfullscreen
      ></iframe>

      <div :class="['flip-button', { flipped }]" @click="flipButton">
        <div class="front">Word of the Day!</div>
        <div class="back">{{ video.word }}</div>
      </div>

      <div class="sentence-container">
        <div class="sentence-title">
          <strong>Example Usage</strong>
        </div>
        <div 
        :class="['sentence spanish-sentence', {hovered: revealed.sentenceSpanish }]"
        @click="revealSentence('sentenceSpanish')">

        <div v-if="!revealed.sentenceSpanish" class="front">See an example in Spanish</div>
        <div v-if="revealed.sentenceSpanish" class="back">{{ video.sentence }}</div>
        </div>
        <div
          :class="['sentence english-sentence', { hovered: revealed.sentenceEnglish }]"
          @click="revealSentence('sentenceEnglish')"
        >
          <div v-if="!revealed.sentenceEnglish" class="front">Reveal the English translation</div>
          <div v-if="revealed.sentenceEnglish" class="back">{{ video.translated_sentence }}</div>
        </div>
      </div>
    </div>
    <p v-else>Loading videos...</p>
  </div>
</template>



<script setup>

import { ref, reactive, onMounted } from "vue";
import axios from "axios";

const video = reactive({
  video_id: "",
  title: "",
  word: "",
  sentence: "",
  translated_sentence: "",
  upload_date: "",
});

const flipped = ref(false);
const revealed = reactive({
  sentenceSpanish: false,
  sentenceEnglish: false,
})

async function fetchVideos() {
  try {
    const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
    const response = await axios.get(`${apiBaseUrl}today/videos/latest/`);

    if (response.data) {
      video.video_id = response.data.video_id || "";
      video.title = response.data.title || "";
      video.word = response.data.word || "";
      video.sentence = response.data.sentence || "";
      video.translated_sentence = response.data.translated_sentence || "";
      video.upload_date = formatDate(new Date(response.data.upload_date)) || "";
    } else {
      console.error("Error: No data received from API.");
    }
  } catch (error) {
    console.error("Error fetching video details:", error);
  }
}

function flipButton() {
  flipped.value = !flipped.value;
}

function revealSentence(sentenceName) {
  revealed[sentenceName] = !revealed[sentenceName];
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
