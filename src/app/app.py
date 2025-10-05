from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from helpers import *

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def get_path():
    if 'userText' in request.form:
        path = request.form.get('userText')
        print("did")
        store_image_data(path)
    text = request.form.get('search_text')
    print(check_match(text))
    return render_template("show_files.html", users=check_match(text))

if __name__ == '__main__':
    app.run(debug=True)
  