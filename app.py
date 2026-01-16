from flask import Flask, jsonify, render_template, request
from analyzer import analyze_numbers
from external_api import fetch_hourly_temperature
from weather_analysis import analyze_time_series, WeatherAnalysisError

app = Flask(__name__)

@app.route('/')
def index():
    a = "Thitima"
    return render_template("index.html", name=a)

@app.route('/analyze', methods=['GET', 'POST']) 
def analyze():
    request_data = request.form.get('numbers', '')
    if request_data:
        try:
            # Replace commas with spaces, split on whitespace, ignore empty tokens
            cleaned = request_data.replace(',', ' ')
            tokens = cleaned.split()
            numbers = []
            for token in tokens:
                # convert each token to float (will raise ValueError if invalid)
                numbers.append(float(token))
        except ValueError:
            error_message = "Invalid input. Please enter a list of numbers separated by commas or whitespace."
            return render_template("index.html", error=error_message)
        
        results = analyze_numbers(numbers)
        return render_template("results.html", numbers=numbers, results=results)            
    return render_template("index.html", error="No input provided. Please enter some numbers.")

@app.route('/test-weather')
def test_weather():
    # Example coordinates for testing
    latitude = 40.7128
    longitude = -74.0060
    times, temperatures = fetch_hourly_temperature(latitude, longitude)
    return render_template("weather_analysis_results.html", times=times, temperatures=temperatures)

@app.route('/analyze-weather', methods=['GET', 'POST'])
def analyze_weather():
    if request.method == 'POST':
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)

        if latitude is None or longitude is None:
            error_message = "Please provide valid latitude and longitude."
            return render_template("weather_input.html", error=error_message)
        
        times, temperatures = fetch_hourly_temperature(latitude, longitude)
        try:
            results = analyze_time_series(times, temperatures)
        except WeatherAnalysisError as e:
            # Render input page with a clear error message for the user
            return render_template("weather_input.html", error=str(e))
        return render_template("weather_analysis_results.html", analysis=results)
    error_message = "Please provide valid latitude and longitude."
    return render_template("weather_input.html", error=error_message)

@app.route('/weather-input')
def weather_input():
    return render_template("weather_input.html")  

if __name__ == '__main__':
    app.run(debug=True)

