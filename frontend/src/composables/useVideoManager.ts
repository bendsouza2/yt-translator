import axios from 'axios';
import { Ref } from 'vue';

interface Video {
  video_id: string;
  upload_time: string;
  word: string;
  sentence: string;
  translated_sentence: string;
}

interface RevealedState {
  sentenceSpanish: boolean;
  sentenceEnglish: boolean;
}

export function useVideoManager(
  videos: Ref<Video[]>, 
  loading: Ref<boolean>, 
  flippedStates: Ref<Record<number, boolean>>, 
  revealedStates: Ref<Record<number, RevealedState>>
) {
  async function fetchVideos() {
    try {
      const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
      const response = await axios.get<{ videos: Video[] }>(
        `${apiBaseUrl}today/videos/paginated-videos/`, 
        {
          params: {
            limit: 7,
            page_num: 1
          }
        }
      );

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

  function formatDate(date: Date): string {
    const options: Intl.DateTimeFormatOptions = { 
      weekday: "long", 
      year: "numeric", 
      month: "long", 
      day: "numeric" 
    };
    const formattedDate = new Intl.DateTimeFormat("en-GB", options).format(date);
    const day = date.getDate();

    const ordinalSuffix = (n: number): string => {
      const s = ["th", "st", "nd", "rd"];
      const v = n % 100;
      return n + (s[(v - 20) % 10] || s[v] || s[0]);
    };

    const dayWithOrdinal = ordinalSuffix(day);
    return formattedDate.replace(/\d+/, dayWithOrdinal);
  }

  return {
    fetchVideos
  };
}