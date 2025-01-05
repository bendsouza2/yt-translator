<template>
    <div class="background-container">
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
  
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";

/**
 * Calculates the next occurrence of noon (12pm UTC).
 * @returns {Date} A Date object representing the next noon.
 */
function getNextNoon(): Date {
    const now = new Date();
    const nextNoon = new Date();
  
    nextNoon.setHours(12, 0, 0, 0); 
    if (now >= nextNoon) {
      nextNoon.setDate(nextNoon.getDate() + 1); 
    }
    return nextNoon;
}
  
const countdown = ref<{
    hours: number;
    minutes: number;
    seconds: number;
}>({
    hours: 0,
    minutes: 0,
    seconds: 0,
});

const isSpinning = ref<boolean>(true);

/**
 * Computes an array of individual digits for the countdown timer.
 * @returns {string[]} An array of strings representing the digits.
 */
const timerDigits = computed<string[]>(() => {
    const hours = String(countdown.value.hours).padStart(2, '0');
    const minutes = String(countdown.value.minutes).padStart(2, '0');
    const seconds = String(countdown.value.seconds).padStart(2, '0');
    return [...hours, ...minutes, ...seconds];
});

/**
 * Gets the previous digit in a circular sequence (0 → 9, otherwise -1).
 * @param {string} digit - A single-digit string.
 * @returns {string} The previous digit as a string.
 */
function getPrevDigit(digit: string): string {
    return digit === '0' ? '9' : String(Number(digit) - 1);
}

/**
 * Gets the next digit in a circular sequence (9 → 0, otherwise +1).
 * @param {string} digit - A single-digit string.
 * @returns {string} The next digit as a string.
 */
function getNextDigit(digit: string): string {
    return digit === '9' ? '0' : String(Number(digit) + 1);
}

/**
 * Calculates the countdown to the next noon.
 * @returns {{ hours: number; minutes: number; seconds: number }} The remaining time until next noon.
 */
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

let interval: ReturnType<typeof setInterval> | undefined = undefined;

/**
 * Animates the spinning countdown (slot machine) effect towards a target value.
 * @param targetCountdown - The target countdown values.
 */
function startSpinningAnimation(targetCountdown: typeof countdown.value): void {
    const duration = 1200; // Total animation duration in ms
    const steps = 10; // Number of steps to reach target
    const stepDuration = duration / steps;
    
    let currentStep = 0;
    const spinInterval = setInterval(() => {
        currentStep++;
        
        // Calculate intermediate values that progress towards the target
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

/**
 * Updates the countdown and manages spinning animations.
 */
function updateCountdown(): void {
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
        }
    }
}

// Text animation logic
const englishWords = ref<string[]>(['Next', 'word', 'in:']);
const spanishWords = ref<string[]>(['Hasta', 'la', 'próxima', 'palabara']);
const visibleEnglishWords = ref<boolean[]>(Array(englishWords.value.length).fill(false));
const visibleSpanishWords = ref<boolean[]>(Array(spanishWords.value.length).fill(false));
const isAnimatingEnglish = ref<boolean>(true);

/**
 * Pauses execution for a given number of milliseconds.
 * @param {number} ms - The number of milliseconds to wait.
 * @returns {Promise<void>} A promise that resolves after the delay.
 */
async function sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Animates the display of text, alternating between English and Spanish words.
 */
async function animateText(): Promise<void> {
    while (true) {
        if (isAnimatingEnglish.value) {
            // Reset Spanish words
            visibleSpanishWords.value = Array(spanishWords.value.length).fill(false);
            
            // Animate English words
            for (let i = 0; i < englishWords.value.length; i++) {
                visibleEnglishWords.value[i] = true;
                await sleep(300); // Time between each word appearing
            }
            
            await sleep(2000); // Pause with full English text visible
            visibleEnglishWords.value = Array(englishWords.value.length).fill(false);
        } else {
            // Reset English words
            visibleEnglishWords.value = Array(englishWords.value.length).fill(false);
            
            // Animate Spanish words
            for (let i = 0; i < spanishWords.value.length; i++) {
                visibleSpanishWords.value[i] = true;
                await sleep(300); // Time between each word appearing
            }
            
            await sleep(2000); // Pause with full Spanish text visible
            visibleSpanishWords.value = Array(spanishWords.value.length).fill(false);
        }
        
        isAnimatingEnglish.value = !isAnimatingEnglish.value;
        await sleep(500); // Pause between language switches
    }
}


onMounted(() => {
    updateCountdown();
    animateText();
});
  
onUnmounted(() => {
    if (interval !== undefined) {
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