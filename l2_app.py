import datetime as dt
import json
import requests
from flask import Flask, request, jsonify

API_TOKEN = ''
API_KEY = ''

def get_weather(q, d):

    BASE_URL = 'http://api.weatherapi.com/v1/history.json'
    url = f'{BASE_URL}?key={API_KEY}&q={q}&dt={d}'

    payload = {}
    headers = {"Authorization": API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)['forecast']['forecastday'][0]['day']

app = Flask(__name__)

class InvalidUsage(Exception):
    
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return f'<head><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@900&display=swap" rel="stylesheet"></head><body style="min-height:100%; background-color: hsl(220, 14%, 91%);"><h1 style="display: block; border: 2px dashed hsl(212, 52%, 60%); padding: 15px;position:ab>

@app.route("/content/api/v1/integration/generate", methods=["POST"])
def weather_endpoint():
    json_data = request.get_json()

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("Wrong API token", status_code=403)

    location = ''
    date = ''
    requester_name = ''

    if json_data.get("location", "date"):
        location = json_data.get("location")
        date = json_data.get("date")
        requester_name = json_data.get("requester_name")


    weather = get_weather(location, date)
    timestamp = dt.datetime.utcnow()

    result = {
        "requester_name": requester_name,
        "timestamp": timestamp,
        "location": location,
        "date": date,
        "weather": weather
    }

    return result
