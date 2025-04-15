# NASA API Explorer

This project allows you to explore NASA's APIs, including:
- Mars Rover Photos
- Astronomy Picture of the Day (APOD)
- Earth Polychromatic Imaging Camera (EPIC)
- And more!

## Setup

1. Get your NASA API key from https://api.nasa.gov/
2. Create a `.env` file in the project root and add your API key:
   ```
   NASA_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the script:
   ```bash
   python nasa_explorer.py
   ```

## Features

- View Mars Rover photos
- Get the Astronomy Picture of the Day
- View Earth images from EPIC
- Save and display images locally

## Note

This project uses NASA's public APIs. Please be mindful of API rate limits and usage guidelines. 