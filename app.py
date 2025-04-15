from flask import Flask, render_template, request, jsonify
from nasa_explorer import NASAExplorer
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize NASAExplorer only when needed
def get_nasa_explorer():
    if not hasattr(app, 'nasa'):
        app.nasa = NASAExplorer()
    return app.nasa

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/apod')
def get_apod():
    date = request.args.get('date')
    try:
        nasa = get_nasa_explorer()
        apod = nasa.get_apod(date)
        return jsonify(apod)
    except Exception as e:
        print(f"APOD Error: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 400

@app.route('/api/mars')
def get_mars_photos():
    rover = request.args.get('rover', 'curiosity')
    sol = request.args.get('sol', 1000)
    camera = request.args.get('camera', 'FHAZ')
    try:
        nasa = get_nasa_explorer()
        photos = nasa.get_mars_photos(rover, int(sol), camera)
        return jsonify(photos)
    except Exception as e:
        print(f"Mars Photos Error: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 400

@app.route('/api/epic')
def get_epic():
    date = request.args.get('date')
    try:
        nasa = get_nasa_explorer()
        epic = nasa.get_epic_images(date)
        return jsonify(epic)
    except Exception as e:
        print(f"EPIC Error: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 400

# This is required for Vercel
app = app 