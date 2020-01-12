from flask import Flask, jsonify, current_app
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder="dist", static_url_path="/dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/random')
def random_number():
    response = {
        'property': "empty"
    }
    return jsonify(response)

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/<path:path>')
def static_content(path):
    return current_app.send_static_file(path)

if __name__ == "__main__":
    app.run()