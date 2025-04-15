import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

class NASAExplorer:
    def __init__(self):
        self.api_key = os.getenv('NASA_API_KEY')
        if not self.api_key:
            raise ValueError("NASA API key not found. Please set NASA_API_KEY in .env file")
        
        self.base_url = "https://api.nasa.gov"
        
    def get_apod(self, date=None):
        """Get Astronomy Picture of the Day"""
        endpoint = f"{self.base_url}/planetary/apod"
        # Use yesterday's date to ensure we have an image
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        params = {
            'api_key': self.api_key,
            'date': date
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_mars_photos(self, rover="curiosity", sol=1000, camera="FHAZ"):
        """Get Mars Rover photos"""
        endpoint = f"{self.base_url}/mars-photos/api/v1/rovers/{rover}/photos"
        params = {
            'api_key': self.api_key,
            'sol': sol,
            'camera': camera
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_epic_images(self, date=None):
        """Get Earth Polychromatic Imaging Camera images"""
        endpoint = f"{self.base_url}/EPIC/api/natural"
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        params = {
            'api_key': self.api_key,
            'date': date
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def download_and_show_image(self, image_url, title="NASA Image"):
        """Download and display an image"""
        response = requests.get(image_url)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.show(title=title)
        return img

def main():
    try:
        nasa = NASAExplorer()
        
        # Get today's APOD
        print("\nFetching Astronomy Picture of the Day...")
        apod = nasa.get_apod(date="2024-04-15")
        print(f"Title: {apod['title']}")
        print(f"Explanation: {apod['explanation']}")
        nasa.download_and_show_image(apod['url'], "Astronomy Picture of the Day")
        
        # Get Mars Rover photos
        print("\nFetching Mars Rover photos...")
        mars_photos = nasa.get_mars_photos()
        if mars_photos['photos']:
            first_photo = mars_photos['photos'][0]
            print(f"Rover: {first_photo['rover']['name']}")
            print(f"Camera: {first_photo['camera']['full_name']}")
            nasa.download_and_show_image(first_photo['img_src'], "Mars Rover Photo")
        
        # Get EPIC images
        print("\nFetching EPIC images...")
        epic_images = nasa.get_epic_images()
        if epic_images:
            first_image = epic_images[0]
            image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{first_image['date'].split()[0].replace('-', '/')}/png/{first_image['image']}.png"
            nasa.download_and_show_image(image_url, "EPIC Earth Image")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 