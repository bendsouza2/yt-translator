
/**
 * Calculates the next occurrence of noon (12pm UTC).
 * @returns {Date} - A Date object representing the next noon.
 */
function getNextNoon() {
    const now = new Date();
    const nextNoon = new Date();

    nextNoon.setHours(12, 0, 0, 0)

    if (now >= nextNoon) {
        nextNoon.setDate(nextNoon.getDate() + 1);
    } 

    return nextNoon;
}

const a = getNextNoon();
console.log(a);

/**
 * Get a countdown to the next upload time (12pm UTC).
 * @param {Function} callback - A function to handle the countdown values.
 */
function uploadCountdown(callback) {
    const nextUpload = getNextNoon().getTime();

    let countInterval = setInterval(function() {
        const now = new Date().getTime();

        const timeDistance = nextUpload - now;

        if (timeDistance <= 0) {
            clearInterval(countInterval); // Stop the countdown when time reaches 0
            callback({
                hours: 0,
                minutes: 0,
                seconds: 0,
            });
            return;
        }

        const hours = Math.floor((timeDistance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeDistance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDistance % (1000 * 60)) / 1000);

        // Send the countdown values to the callback
        callback({
            hours: hours,
            minutes: minutes,
            seconds: seconds,
        });
    }, 1000); // Update every second
}

// Example usage
uploadCountdown((countdown) => {
    console.log(countdown); // Logs the countdown every second
});
