
from flask import Flask, render_template, jsonify
from weather import get_weather
from prediction import calculate_probability

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/prediction")
def prediction():
    try:
        weather = get_weather()
        probability = calculate_probability(weather)

        return jsonify({
            "probability": probability,
            **weather
        })

    except Exception as error:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Unable to retrieve weather forecast"
        }), 503


if __name__ == "__main__":
    app.run(debug=True)

