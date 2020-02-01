from flask import Flask, jsonify, current_app, redirect
from flask_cors import CORS
import requests
import wideq

app = Flask(__name__, static_folder="dist", static_url_path="/dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

wide_eq_client = wideq.Client()

@app.route('/api/devices')
def get_devices():
    devices = wide_eq_client.devices
    return jsonify(devices)

@app.route('/api/login')
def login():
    return redirect(wide_eq_client.gateway.oauth_url())

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/<path:path>')
def static_content(path):
    return current_app.send_static_file(path)

if __name__ == "__main__":
    app.run()