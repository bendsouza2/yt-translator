<template>
    <div class="top-content">
      <button @click="$emit('toggle-language')" class="language-switch-btn">
        {{ isSpanish ? translations.switchLanguage.es : translations.switchLanguage.en }}
      </button>
  
      <h1>{{ isSpanish ? translations.title.es : translations.title.en }}</h1>
  
      <!-- Render date if available -->
      <h2 v-if="currentVideo?.upload_time">
        {{ translateDate(currentVideo.upload_time) }}
      </h2>
    </div>
  </template>
  
  <script setup>
  import { computed } from "vue";
  
  defineProps({
    isSpanish: Boolean,
    translations: Object,
    currentVideo: Object,
  });
  
  defineEmits(["toggle-language"]);
  
  const translateDate = (date) => {
    // Ensure date formatting logic is consistent
    if (!isSpanish) return date;
    const parts = date.split(' ');
    const day = parts[0];
    const dayNumber = parts[1].replace(/\D/g, '');
    const month = parts[parts.length - 2];
    const year = parts[parts.length - 1];
  
    const languageMap = {
      days: {
        en: {
          Monday: "lunes",
          Tuesday: "martes",
          Wednesday: "miércoles",
          Thursday: "jueves",
          Friday: "viernes",
          Saturday: "sábado",
          Sunday: "domingo",
        },
      },
      months: {
        en: {
          January: "enero",
          February: "febrero",
          March: "marzo",
          April: "abril",
          May: "mayo",
          June: "junio",
          July: "julio",
          August: "agosto",
          September: "septiembre",
          October: "octubre",
          November: "noviembre",
          December: "diciembre",
        },
      },
    };
  
    const translatedDay = languageMap.days.en[day] || day;
    const translatedMonth = languageMap.months.en[month] || month;
  
    return `${translatedDay} ${dayNumber} ${translatedMonth} ${year}`;
  };
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