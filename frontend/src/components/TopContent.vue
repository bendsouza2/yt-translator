<template>
    <div class="top-content">
      <button
        @click="$emit('toggle-language')"
        class="language-switch-btn"
      >
        {{ isSpanish ? translations.switchLanguage.es : translations.switchLanguage.en }}
      </button>
      <h1>{{ isSpanish ? translations.title.es : translations.title.en }}</h1>
      <h2 v-if="currentVideo.upload_time">
        {{ translatedDate }}
      </h2>
    </div>
</template>
    
<script setup>
import { defineProps, defineEmits, computed } from 'vue';
import { useLanguageTranslation } from '../composables/useLanguageTranslation';

const props = defineProps({
    isSpanish: Boolean,
    translations: Object,
    currentVideo: {
        type: Object,
        default: () => ({})
    }
});

const emit = defineEmits(['toggle-language']);

const { translateDate } = useLanguageTranslation(); 

const translatedDate = computed(() => {
  if (props.currentVideo.upload_time) {
    return translateDate(props.currentVideo.upload_time, props.isSpanish); 
  }
  return '';
});
</script>

<style>
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

.top-content h1, .top-content h2 {
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

.language-switch-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ae852c;
  color: #333;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}
</style>