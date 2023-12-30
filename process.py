from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import os
import cv2
import sys
import tempfile
import requests
import traceback
import cloudinary
import numpy as np
from rembg import remove
import cloudinary.uploader
from termcolor import colored
from urllib.parse import urlparse
from logger_config import setup_logger 


## Setup Logger Configuration
logger = setup_logger()


## Cloudinary configuration
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET")
)


###--------------------------------------------------------------------------###


def log_exception(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    trace_details = traceback.format_exception(exc_type, exc_value, exc_traceback)

    logger.error(f"Error: {str(e)}")
    logger.error(f"Exception type: {exc_type}")
    logger.error(f"Exception value: {exc_value}")
    logger.error(f"Exception traceback details: {''.join(trace_details)}")


###--------------------------------------------------------------------------###


def download_image(image_url):
    response = requests.get(image_url)
    image = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    response.close()
    return image


###--------------------------------------------------------------------------###


def generate_output_filename(input_url):
    # Extract the file name from the URL
    parsed_url = urlparse(input_url)
    file_name = os.path.basename(parsed_url.path)
    # Remove file extension and add '_remove_bg.png'
    return os.path.splitext(file_name)[0] + '_remove_bg.png'


###--------------------------------------------------------------------------###


def upload_to_cloudinary(file_path):
    response = cloudinary.uploader.upload(file_path)
    return response['url']


###--------------------------------------------------------------------------###


def remove_background_and_upload(payload):

    required_params = ["image_url"]
    if any(param not in payload for param in required_params):
        return {
            "data": {},
            "status": False,
            "message": "Required parameters missing",
        }, 400

    try:
        image_url = payload["image_url"]

        input_image = download_image(image_url)
        file_name = generate_output_filename(image_url)

        # Use a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, file_name)

            # Convert the image to bytes format
            image_bytes = cv2.imencode('.png', input_image)[1].tobytes() if input_image is not None else None

            # Remove background
            output = remove(image_bytes) if image_bytes is not None else None

            # Save the output image and upload
            if output:
                with open(output_path, 'wb') as file:
                    file.write(output)
                
                result_url = upload_to_cloudinary(output_path)

                # The temporary file and directory will be automatically deleted after this block

                print(colored(f'Background Removed Url : {result_url}', 'green'))
                return {
                    "data": {"original_image_url":image_url,"bg_remove_url": result_url},
                    "status": True,
                    "message": "Success",
                }, 200
    except Exception as e:
        log_exception(e)
        return {
            "data": {},
            "status": False,
            "message": "Input url is invalid or malformed",
        }, 500



## Test the function
if __name__ == '__main__':
    payload = {'image_url':'<public_image_url>'}
    result_url = remove_background_and_upload(payload)
    print(colored(f'Background Removed Url : {result_url}', 'cyan'))


