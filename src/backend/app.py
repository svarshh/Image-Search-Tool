from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from helpers import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# able to send back
@app.route('/api/data/<string:word>', methods=['GET'])
def get_files(word):
    paths = check_match(word)
    keys = list(range(1, len(paths)+1))
    return jsonify( dict(zip(keys, paths)))

# cors is not giving access
@app.route('/api/submit', methods=['POST'])
def post_files():
    dummy_data = {
        "message": "This is a dummy JSON response.",
        "status": "success",
        "data": [
            {"id": 1, "name": "Item A"},
            {"id": 2, "name": "Item B"},
            {"id": 3, "name": "Item C"}
        ]
    }

    return dummy_data

    

if __name__ == '__main__':
    app.run(debug=True, port=8000)
  