import ffmpeg from 'fluent-ffmpeg';
import sharp from 'sharp';
import fs from 'fs';
import srtToVtt from 'srt-to-vtt'; // Import the whole module as a default import

// Paths to your files
const imagePath = '/Users/bendsouza/PycharmProjects/yt_translator/images/02-23-2024 20:04:39.jpg';
const audioPath = '/Users/bendsouza/PycharmProjects/yt_translator/audio/09-28-2024 13:39:02.mp3';
const subtitlePath = '/Users/bendsouza/PycharmProjects/yt_translator/subtitles/10-05-2024 19:03:28.srt';
const outputPath = '/Users/bendsouza/PycharmProjects/yt_translator/video/output_video_2.mp4';
const vttPath = '/Users/bendsouza/PycharmProjects/yt_translator/video/subtitles.vtt'; // Path for VTT file

// Convert SRT to VTT
const convertSrtToVtt = (srtFilePath, vttFilePath) => {
    const srtStream = fs.createReadStream(srtFilePath);
    const vttStream = fs.createWriteStream(vttFilePath);
    
    // Pipe the streams through srtToVtt
    srtStream.pipe(srtToVtt()).pipe(vttStream).on('finish', () => {
        console.log('SRT converted to VTT successfully.');
    }).on('error', (err) => {
        console.error('Error during conversion:', err);
    });
};

// Convert subtitles
convertSrtToVtt(subtitlePath, vttPath);

// Load the audio file and get its duration
ffmpeg.ffprobe(audioPath, (err, metadata) => {
    if (err) {
        console.error('Error retrieving audio metadata:', err);
        return;
    }

    const audioDuration = metadata.format.duration; // Duration in seconds
    console.log(`Audio duration: ${audioDuration} seconds`);

    // Set the image duration based on the audio duration
    const imageDuration = audioDuration < 6.34 ? audioDuration : 6.34;

    // Create a temporary image with the desired duration
    const tempImagePath = 'temp_image.mp4';
    ffmpeg()
        .input(imagePath)
        .loop(imageDuration) // Loop the image for the duration of the audio
        .outputOptions('-c:v libx264')
        .outputOptions('-t', imageDuration)
        .output(tempImagePath)
        .on('end', () => {
            console.log('Image video created');

            // Combine the image video, audio, and subtitles into the final output
            ffmpeg()
                .input(tempImagePath)
                .input(audioPath)
                .input(vttPath) // Use the VTT file for subtitles
                .outputOptions('-c:v copy') // Copy video codec
                .outputOptions('-c:a aac') // Set audio codec
                .outputOptions('-vf', `subtitles=${vttPath}`) // Add subtitles
                .output(outputPath)
                .on('end', () => {
                    console.log('Final video created successfully!');
                    // Clean up temporary files
                    fs.unlinkSync(tempImagePath); // Remove temporary image file
                    fs.unlinkSync(vttPath); // Remove temporary VTT file
                })
                .on('error', (err) => {
                    console.error('Error creating final video:', err);
                })
                .run();
        })
        .on('error', (err) => {
            console.error('Error creating temporary image video:', err);
        })
        .run();
});
