import numpy as np
import requests
from skimage import exposure
import base64
from PIL import Image, ImageOps, ImageChops
from io import BytesIO

class ProcessImage:
    def __init__(self, image_url):
        self.image_url = image_url

    def process_image(self):
        try:
            # Send a GET request to fetch the image from the URL
            response = requests.get(self.image_url)
            response.raise_for_status()

            # Open the image using PIL
            image = Image.open(BytesIO(response.content))

            # Apply image processing steps
            replaced_image = self.replace_transparent_background(image)
            trimmed_image = self.trim_borders(replaced_image)
            padded_image = self.pad_image(trimmed_image)
            inverted_image = self.invert_colors(padded_image)
            resized_image = self.resize_image(inverted_image)
            grayscale_image = self.convert_to_grayscale(resized_image)
            normalized_image = self.normalize_image(grayscale_image)

            # Convert the processed image to a 1D array
            image_data = np.array(image).flatten()

            # Return the processed image data
            return image_data

        except Exception as e:
            print(f"Error processing image: {e}")
            return None


    
    @staticmethod
    def replace_transparent_background(image):
        image_arr = np.array(image)

        if len(image_arr.shape) == 2:
            return image

        alpha1 = 0
        r2, g2, b2, alpha2 = 255, 255, 255, 255

        red, green, blue, alpha = image_arr[:, :, 0], image_arr[:, :, 1], image_arr[:, :, 2], image_arr[:, :, 3]
        mask = (alpha == alpha1)
        image_arr[:, :, :4][mask] = [r2, g2, b2, alpha2]

        return Image.fromarray(image_arr)

    @staticmethod
    def trim_borders(image):
        bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return image.crop(bbox)
        
        return image

    @staticmethod
    def pad_image(image):
        return ImageOps.expand(image, border=30, fill='#fff')

    @staticmethod
    def invert_colors(image):
        return ImageOps.invert(image)

    @staticmethod
    def resize_image(image):
        return image.resize((8, 8), Image.LINEAR)
    
    @staticmethod
    def decode_image_data_uri(image_data_uri):
        try:
            if image_data_uri.startswith('data:image/'):
                # Handle base64-encoded image data URI
                image_data = image_data_uri.split(",")[1]
                decoded_image_data = base64.b64decode(image_data)
                image_stream = BytesIO(decoded_image_data)
                image = Image.open(image_stream)
            else:
                # Handle regular URL-based image data URI
                response = requests.get(image_data_uri)
                response.raise_for_status()
                image_stream = BytesIO(response.content)
                image = Image.open(image_stream)

            return image
        except Exception as e:
            print(f"Error decoding image data URI: {e}")
            return None
        

    




