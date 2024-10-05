import fs from 'fs';
import * as Echogarden from 'echogarden';


const args = process.argv.slice(2); 

const audioPath = args[0];
const subtitleText = args[1];
const outputFilePath = args[2];

console.log(`Audio Path: ${audioPath}`);
console.log(`Subtitle Text: ${subtitleText}`);

function formatTime(seconds) {
    const date = new Date(0);
    date.setSeconds(seconds);
    return date.toISOString().substr(11, 8) + ',' + Math.floor((seconds % 1) * 1000).toString().padStart(3, '0');
}

// Function to split text into chunks of three words
function splitIntoChunks(text, chunkSize) {
    const words = text.split(' ');
    const chunks = [];

    for (let i = 0; i < words.length; i += chunkSize) {
        chunks.push(words.slice(i, i + chunkSize).join(' '));
    }

    return chunks;
}

async function synchronizeSubtitles(audioPath, subtitleText, outputFilePath) {
    try {
        const result = await Echogarden.align(audioPath, subtitleText, { format: 'srt' });

        const timeline = result.timeline;
        const wordTimeline = result.wordTimeline; // Get word timelines
        let srtContent = '';
        let subtitleIndex = 1;

        // Flatten the word timeline to get start and end times for each word
        const words = wordTimeline.map(word => ({
            text: word.text,
            startTime: word.startTime,
            endTime: word.endTime,
        }));

        for (let i = 0; i < words.length; i += 3) {
            const chunkWords = words.slice(i, i + 3);
            const startTime = formatTime(chunkWords[0].startTime); // Start time of the first word
            const endTime = formatTime(chunkWords[chunkWords.length - 1].endTime); // End time of the last word
            const chunkText = chunkWords.map(word => word.text).join(' '); // Join words in the chunk

            srtContent += `${subtitleIndex++}\n${startTime} --> ${endTime}\n${chunkText}\n\n`;
        }

        fs.writeFileSync(outputFilePath, srtContent.trim());
        console.log(`Subtitles synchronized and saved to ${outputFilePath}`);
    } catch (error) {
        console.error('Error synchronizing subtitles:', error);
    }
}

synchronizeSubtitles(audioPath, subtitleText, outputFilePath);