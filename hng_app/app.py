from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "Hello HNG Interns"



@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = request.remote_addr
    
    # For local testing purposes, you can use a fixed IP address for demonstration
    if client_ip == '127.0.0.1':
        client_ip = '8.8.8.8'
    
    location_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
    location_data = location_response.json()
    city = location_data.get('city', 'Unknown')
    country = location_data.get('country_name', 'Unknown')
    

    weather_api_key = os.getenv('WEATHER_API_KEY', 'default_value_if_not_set')  # Replace with your OpenWeatherMap API key
    weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp'] if 'main' in weather_data else 'Unknown'
    
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    
    return jsonify({
        'client_ip': client_ip,
        'location': city,
        'greeting': greeting
    })

if __name__ == '__main__':
    app.run(debug=True)
