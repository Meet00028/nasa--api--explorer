from flask import Flask, render_template, request, jsonify
from nasa_explorer import NASAExplorer
import logging
from flask_cors import CORS
from config import NASA_API_KEY, APOD_URL, MARS_URL, EPIC_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_nasa_explorer():
    """Initialize and return a NASAExplorer instance."""
    logger.info("Initializing NASAExplorer instance")
    return NASAExplorer(NASA_API_KEY, APOD_URL, MARS_URL, EPIC_URL)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/apod')
def get_apod():
    date = request.args.get('date')
    try:
        nasa = get_nasa_explorer()
        logger.info("Fetching APOD data...")
        apod = nasa.get_apod(date)
        logger.info("APOD data fetched successfully")
        return jsonify(apod)
    except Exception as e:
        logger.error(f"APOD Error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/mars')
def get_mars_photos():
    rover = request.args.get('rover', 'curiosity')
    sol = request.args.get('sol', 1000)
    camera = request.args.get('camera', 'FHAZ')
    try:
        nasa = get_nasa_explorer()
        logger.info(f"Fetching Mars photos for rover: {rover}")
        photos = nasa.get_mars_photos(rover=rover, sol=int(sol), camera=camera)
        logger.info("Mars photos fetched successfully")
        return jsonify(photos)
    except Exception as e:
        logger.error(f"Mars Photos Error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/epic')
def get_epic():
    date = request.args.get('date')
    try:
        nasa = get_nasa_explorer()
        logger.info("Fetching EPIC images...")
        epic = nasa.get_epic_images(date)
        logger.info("EPIC images fetched successfully")
        return jsonify(epic)
    except Exception as e:
        logger.error(f"EPIC Error: {str(e)}")
        return jsonify({'error': str(e)}), 400

# This is required for Vercel
app = app 