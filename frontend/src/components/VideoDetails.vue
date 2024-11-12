<template>
  <div>
    <h1>Video Details</h1>
    <div v-if="videos.length">
      <div v-for="video in videos" :key="video.video_id" class="video-detail">
        <h2>{{ video.title }}</h2>
        <iframe
          :src="`https://www.youtube.com/embed/${video.video_id}`"
          width="315"
          height="560"
          frameborder="0"
          allowfullscreen
        ></iframe>
        <p>{{ video.description }}</p>
        <p><strong>Word:</strong> {{ video.word }}</p>
        <p><strong>Sentence:</strong> {{ video.sentence }}</p>
        <p><strong>Translation:</strong> {{ video.translated_sentence }}</p>
        <p><strong>Upload Date:</strong> {{ video.upload_date }}</p>
      </div>
    </div>
    <p v-else>Loading videos...</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      videos: [],
    };
  },
  created() {
    this.fetchVideos();
  },
  methods: {
    async fetchVideos() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}today/api/videos/`)
        this.videos = response.data; 
      } catch (error) {
        console.error("Error fetching video details:", error);
      }
    },
  },
};
</script>

<style scoped>
.video-detail {
  margin-bottom: 20px;
}
</style>
