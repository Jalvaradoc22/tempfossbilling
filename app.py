from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

FLASK_API_URL = 'http://127.0.0.1:5000/predict'  # Your Flask API endpoint

@app.route('/', methods=['POST', 'OPTIONS'])
def handle_request():
    if request.method == 'OPTIONS':
        # Respond to preflight requests
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)

            headers = {'Content-Type': 'application/json'}
            response = requests.post(FLASK_API_URL, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes

            flask_result = response.json()
            print("Flask API response:", flask_result)
            return jsonify(flask_result)

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Flask API: {e}")
            return jsonify({'error': f'Failed to connect to recommendation service: {e}'}), 500
        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': f'Error processing request: {e}'}), 400

    return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
