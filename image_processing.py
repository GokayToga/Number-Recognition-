import numpy as np
from skimage import exposure
import base64
from PIL import Image, ImageOps, ImageChops
from io import BytesIO

class ProcessImage:
    #process_image
    def __init__(self, image_data_uri): 
        self.image_data_uri = image_data_uri

    def process_image(self):

        print('Received image data URI:', self.image_data_uri)
        try:
            image = self.decode_image_data_uri()
            if image is None:
                return None

            image = self.replace_transparent_background(image)
            image = self.trim_borders(image)
            image = self.pad_image(image)
            image = self.invert_colors(image)
            image = self.resize_image(image)
            image = self.convert_to_grayscale(image)
            image = self.normalize_image(image)

            # Convert the image to a 1D array
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
            # Extract the base64-encoded image data from the URI
            image_data = image_data_uri.split(",")[1]
            
            # Decode the base64-encoded image data
            decoded_image_data = base64.b64decode(image_data)
            
            # Create a BytesIO object from the decoded image data
            image_stream = BytesIO(decoded_image_data)
            
            # Open the image using PIL
            image = Image.open(image_stream)
            
            # Return the PIL image object
            return image
        except Exception as e:
            print(f"Error decoding image data URI: {e}")
            return None
        

    




