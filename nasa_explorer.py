import os
import requests
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import logging
from config import NASA_API_KEY

logger = logging.getLogger(__name__)

class NASAExplorer:
    def __init__(self, api_key, apod_url, mars_url, epic_url):
        """Initialize NASAExplorer with API key and endpoints."""
        self.api_key = api_key
        self.apod_url = apod_url
        self.mars_url = mars_url
        self.epic_url = epic_url
        self.logger = logging.getLogger(__name__)
        logger.info("NASAExplorer initialized successfully")
        
    def get_apod(self, date=None):
        """Get Astronomy Picture of the Day."""
        try:
            params = {'api_key': self.api_key}
            if date:
                params['date'] = date
            response = requests.get(self.apod_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching APOD: {str(e)}")
            return None
    
    def get_mars_photos(self, rover="curiosity", sol=1000, camera="FHAZ"):
        """Get Mars photos from specified rover."""
        try:
            # Check if rover is active
            active_rovers = ["curiosity", "perseverance", "opportunity"]
            if rover.lower() not in active_rovers:
                self.logger.warning(f"Rover {rover} is not currently active. Active rovers are: {', '.join(active_rovers)}")
                return {"error": f"Rover {rover} is not currently active. Try one of: {', '.join(active_rovers)}"}

            params = {
                'api_key': self.api_key,
                'sol': sol,
                'camera': camera
            }
            response = requests.get(f"{self.mars_url}/{rover}/photos", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check if photos were found
            if not data.get('photos'):
                self.logger.warning(f"No photos found for rover {rover} on sol {sol} with camera {camera}")
                return {"error": f"No photos found for rover {rover} on sol {sol} with camera {camera}"}
            
            # Convert HTTP URLs to HTTPS
            for photo in data['photos']:
                if photo.get('img_src', '').startswith('http://'):
                    photo['img_src'] = photo['img_src'].replace('http://', 'https://')
                
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching Mars photos: {str(e)}")
            return {"error": f"Error fetching Mars photos: {str(e)}"}
    
    def get_epic_images(self, date=None):
        """Get Earth Polychromatic Imaging Camera (EPIC) images."""
        try:
            # First get the list of available dates
            params = {'api_key': self.api_key}
            response = requests.get(f"{self.epic_url}/natural/available", params=params)
            response.raise_for_status()
            available_dates = response.json()
            
            if not available_dates:
                return {
                    'status': 'success',
                    'message': 'Showing default Earth image',
                    'data': [{
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'identifier': 'default_earth',
                        'caption': 'Beautiful Earth from Space',
                        'image_url': '@nasa-vhSz50AaFAs-unsplash.jpg'
                    }]
                }
            
            # If no date specified, use the most recent available date
            if not date:
                date = available_dates[0]
            
            # Get images for the specified date
            response = requests.get(f"{self.epic_url}/natural/date/{date}", params=params)
            response.raise_for_status()
            images = response.json()
            
            if not images:
                return {
                    'status': 'success',
                    'message': 'Showing default Earth image',
                    'data': [{
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'identifier': 'default_earth',
                        'caption': 'Beautiful Earth from Space',
                        'image_url': '@nasa-vhSz50AaFAs-unsplash.jpg'
                    }]
                }
            
            # Process the images to include the full image URL
            valid_images = []
            for image in images:
                if not isinstance(image, dict):
                    continue
                    
                # Extract required fields with fallbacks
                image_id = image.get('image')
                caption = image.get('caption', '')
                image_date = image.get('date', date)
                
                if not image_id:
                    continue
                
                # Construct the image URL using the correct format
                year = date[:4]
                month = date[5:7]
                day = date[8:10]
                
                valid_images.append({
                    'date': image_date,
                    'identifier': image_id,
                    'caption': caption,
                    'image_url': f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{image_id}.png"
                })
            
            if not valid_images:
                return {
                    'status': 'success',
                    'message': 'Showing default Earth image',
                    'data': [{
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'identifier': 'default_earth',
                        'caption': 'Beautiful Earth from Space',
                        'image_url': '@nasa-vhSz50AaFAs-unsplash.jpg'
                    }]
                }
            
            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(valid_images)} EPIC images for {date}',
                'data': valid_images
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'success',
                'message': 'Showing default Earth image',
                'data': [{
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'identifier': 'default_earth',
                    'caption': 'Beautiful Earth from Space',
                    'image_url': '@nasa-vhSz50AaFAs-unsplash.jpg'
                }]
            }
        except (ValueError, KeyError, IndexError) as e:
            return {
                'status': 'success',
                'message': 'Showing default Earth image',
                'data': [{
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'identifier': 'default_earth',
                    'caption': 'Beautiful Earth from Space',
                    'image_url': '@nasa-vhSz50AaFAs-unsplash.jpg'
                }]
            }
    
    def download_and_show_image(self, image_url, title="NASA Image"):
        """Download and display an image"""
        logger.info(f"Downloading image: {image_url}")
        response = requests.get(image_url)
        logger.info(f"Image download status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Image download error: {response.text}")
            raise Exception(f"Image download error: {response.text}")
            
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.show(title=title)
        return img

def main():
    try:
        nasa = NASAExplorer(NASA_API_KEY, "https://api.nasa.gov/planetary/apod", "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos", "https://epic.gsfc.nasa.gov/archive/natural")
        
        # Get today's APOD
        print("\nFetching Astronomy Picture of the Day...")
        apod = nasa.get_apod(date="2024-04-15")
        if apod:
            print(f"Title: {apod['title']}")
            print(f"Explanation: {apod['explanation']}")
            nasa.download_and_show_image(apod['url'], "Astronomy Picture of the Day")
        
        # Get Mars Rover photos
        print("\nFetching Mars Rover photos...")
        mars_photos = nasa.get_mars_photos()
        if mars_photos and mars_photos['photos']:
            first_photo = mars_photos['photos'][0]
            print(f"Rover: {first_photo['rover']['name']}")
            print(f"Camera: {first_photo['camera']['full_name']}")
            nasa.download_and_show_image(first_photo['img_src'], "Mars Rover Photo")
        
        # Get EPIC images
        print("\nFetching EPIC images...")
        epic_images = nasa.get_epic_images()
        if epic_images and epic_images['data']:
            first_image = epic_images['data'][0]
            print(f"Caption: {first_image['caption']}")
            print(f"Date: {first_image['date']}")
            nasa.download_and_show_image(first_image['image_url'], "EPIC Earth Image")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 