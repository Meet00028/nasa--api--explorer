from flask import Flask, render_template, request, jsonify
from nasa_explorer import NASAExplorer
import os

app = Flask(__name__)
nasa = NASAExplorer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/apod')
def get_apod():
    date = request.args.get('date')
    try:
        apod = nasa.get_apod(date)
        return jsonify(apod)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/mars')
def get_mars_photos():
    rover = request.args.get('rover', 'curiosity')
    sol = request.args.get('sol', 1000)
    camera = request.args.get('camera', 'FHAZ')
    try:
        photos = nasa.get_mars_photos(rover, int(sol), camera)
        return jsonify(photos)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/epic')
def get_epic():
    date = request.args.get('date')
    try:
        epic = nasa.get_epic_images(date)
        return jsonify(epic)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 