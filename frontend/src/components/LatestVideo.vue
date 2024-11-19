<template>
  <div class="background-container">
    <h1> {{ video.upload_date }}</h1>
    <div v-if="video" class="video-container">
        <h2>{{ video.title }}</h2>
        <iframe
          :src="`https://www.youtube.com/embed/${video.video_id}`"
          width="315"
          height="560"
          frameborder="0"
          allowfullscreen
        ></iframe>
          <div :class="['flip-button', { flipped: flipped }]" @click="flipButton">
            <div class="front">Word of the Day!</div>
            <div class="back">{{ video.word }}</div> 
          </div>

        <p><strong>Example Usage:</strong> <span class="sentence">{{ video.sentence }}</span></p>
        
          <div :class="['reveal-sentence', {revealed: revealed}]" @click="revealSentence">
            <div class="front">Click to reveal the English translation</div>
            <div class="back">{{ video.translated_sentence }}</div>
          </div>
        
        <p><strong>Upload Date:</strong> {{ video.upload_date }}</p>
      </div>
    <p v-else>Loading videos...</p>
  </div>
</template>
t
<script>
import axios from "axios";

export default {
  data() {
    return {
      video: [],
      currentDate: new Date().toLocaleDateString(),
      flipped: false,
      revealed: false,
    };
  },
  created() {
    this.fetchVideos();
  },
  methods: {
    async fetchVideos() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}today/api/videos/latest/`)
        this.video = {
            ...response.data,
            upload_date: this.formatDate( new Date(response.data.upload_date) )
        }
            ; 
      } catch (error) {
        console.error("Error fetching video details:", error);
      }
    },
    flipButton() {
        this.flipped = !this.flipped;
    },
    revealSentence() {
        this.revealed = !this.revealed;
    },
    formatDate(date) {
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
    },
  },
};
</script>

<style scoped>
.background-container {
  background-image: linear-gradient(to right, #3b3933 , rgb(66, 46, 1));
  background-size: cover;
  padding: 20px;
  box-sizing: border-box;

}

.video-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 20px;
    animation: animate;
    /* margin-left: auto; */
    /* margin-right: auto; */
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

.word {
    color: black;
    font-weight: bold;
}

.word-button {
    padding: 15px 36px 17px;
    color: #FFF;
    background: #E5A00D;
    outline: 0;
    border: 0;
    opacity: 1;
    line-height: 1;
    -o-transition: all .3s ease;
    transition: all .3s ease;
    cursor: pointer;
    background: #f2a500; 
    opacity: 0.8;
    border-radius: 50px;
    
}

.sentence {
    text-overflow: clip;
}

.flip-button {
  width: 150px;
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

.reveal-sentence {
  width: 300px;
  height: 50px;
  position: relative;
  margin-top: 20px;
  display: inline-block;
  cursor: pointer;
  overflow: hidden;
}

.reveal-sentence .front,
.reveal-sentence .back {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  text-align: center;
  font-weight: bold;
  line-height: 50px;
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

</style>
