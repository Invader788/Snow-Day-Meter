
async function updateMeter() {
    const statusElement = document.getElementById("status");

    try {
        statusElement.textContent = "Loading forecast...";

        const response = await fetch("/api/prediction");

        if (!response.ok) {
            throw new Error("Weather forecast unavailable");
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        const probability = data.probability;

        // Update probability
        document.getElementById("percentage").textContent =
            probability + "%";

        // Animate gauge
        document.getElementById("gauge").style.setProperty(
            "--progress",
            probability + "%"
        );

        // Update prediction status
        let status;

        if (probability >= 80) {
            status = "Possible Snow Day";
        } else if (probability >= 60) {
            status = "Maybe";
        } else if (probability >= 40) {
            status = "Not Very Likely";
        } else if (probability >= 20) {
            status = "Unlikely";
        } else {
            status = "School";
        }

        statusElement.textContent = status;

        // Update weather information
        document.getElementById("snowfall").textContent =
            data.snowfall + " cm";

        document.getElementById("temperature").textContent =
            data.temperature + "°C";

        document.getElementById("wind").textContent =
            data.wind + " km/h";

    } catch (error) {
        console.error("Prediction error:", error);

        statusElement.textContent = "Forecast unavailable";
    }
}


// Create falling snow
function createSnowflakes() {
    const container = document.getElementById("snow");

    for (let i = 0; i < 35; i++) {
        const snowflake = document.createElement("div");

        snowflake.className = "snowflake";
        snowflake.textContent = "O";
// Change for snow particle
        snowflake.style.left =
            Math.random() * 100 + "vw";

        snowflake.style.animationDuration =
            (5 + Math.random() * 10) + "s";

        snowflake.style.animationDelay =
            Math.random() * 10 + "s";

        snowflake.style.fontSize =
            (10 + Math.random() * 15) + "px";

        container.appendChild(snowflake);
    }
}


// Initialize website
updateMeter();
createSnowflakes();

// Refresh forecast every 30 minutes
setInterval(updateMeter, 30 * 60 * 1000);

