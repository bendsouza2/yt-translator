import { Ref } from 'vue';

interface LanguageMap {
  days: {
    en: Record<string, string>;
  };
  months: {
    en: Record<string, string>;
  };
}

export function useLanguageTranslation() {
  const languageMap: LanguageMap = {
    days: {
      en: {
        "Monday": "lunes",
        "Tuesday": "martes",
        "Wednesday": "miércoles",
        "Thursday": "jueves",
        "Friday": "viernes",
        "Saturday": "sábado",
        "Sunday": "domingo",
      }
    },
    months: {
      en: {
        "January": "enero",
        "February": "febrero",
        "March": "marzo",
        "April": "abril",
        "May": "mayo",
        "June": "junio",
        "July": "julio",
        "August": "agosto",
        "September": "septiembre",
        "October": "octubre",
        "November": "noviembre",
        "December": "diciembre"
      }
    }
  };

  function toggleLanguage(isSpanish: Ref<boolean>) {
    isSpanish.value = !isSpanish.value;
  }

  function translateDate(date: string, isSpanish: boolean): string { 
    if (!isSpanish) return date; 

    const parts = date.split(' ');
    const day = parts[0];
    const dayNumber = parts[1].replace(/\D/g, ''); 
    const month = parts[parts.length - 2];
    const year = parts[parts.length - 1];

    const translatedDay = languageMap.days.en[day] || day;
    const translatedMonth = languageMap.months.en[month] || month;

    return `${translatedDay} ${dayNumber} ${translatedMonth} ${year}`;
  }

  return {
    toggleLanguage,
    translateDate
  };
}