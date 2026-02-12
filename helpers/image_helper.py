"""
Helper functions for image operations.
"""
from PIL import Image
from io import BytesIO
import requests
import config


def download_random_dog_image(output_path=config.TEMP_IMAGE):
    """
    Downloads a random dog image from the Dog API and saves it as PNG.
    
    Args:
        output_path: Path where the image will be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get random dog image URL
        response = requests.get(config.DOG_API_URL, timeout=config.API_TIMEOUT)
        response.raise_for_status()
        image_url = response.json()["message"]

        # Download image bytes
        img_response = requests.get(image_url, timeout=15)
        img_response.raise_for_status()

        # Open image from memory and convert to RGB
        img = Image.open(BytesIO(img_response.content))
        img = img.convert("RGB")

        # Save as PNG
        img.save(output_path, format="PNG")
        
        return True

    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def calculate_capacity(image_path, safety_factor=config.SAFETY_FACTOR):
    """
    Calculates the approximate capacity in bytes for LSB 1-bit/channel (RGB) steganography.
    
    Args:
        image_path: Path to the image file
        safety_factor: Safety margin (0.0 to 1.0) to prevent data loss
        
    Returns:
        int: Usable capacity in bytes
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            raw_capacity = (width * height * 3) // 8  # Theoretical bytes
            usable_capacity = int(raw_capacity * safety_factor)
            return max(0, usable_capacity)
    except Exception as e:
        print(f"Error calculating capacity: {e}")
        return 0
