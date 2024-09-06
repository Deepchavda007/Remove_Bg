import os
import sys
import torch
import boto3
import requests
import traceback
import numpy as np
from loguru import logger
import torch.nn.functional as F
from torchvision.transforms.functional import normalize


###--------------------------------------------------------------------------###


def create_response(status, message, data, code):
    return {"status": status, "message": message, "data": data}, code


###--------------------------------------------------------------------------###


def log_exception(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    trace_details = traceback.format_exception(exc_type, exc_value, exc_traceback)

    logger.error(
        {
            "error": str(e),
            "exception_type": str(exc_type),
            "exception_value": str(exc_value),
            "exception_traceback": "".join(trace_details),
        }
    )


###--------------------------------------------------------------------------###


def preprocess_image(im: np.ndarray, model_input_size: list) -> torch.Tensor:
    if len(im.shape) < 3:
        im = im[:, :, np.newaxis]
    if im.shape[2] == 4:  # Convert RGBA to RGB
        im = im[:, :, :3]
    im_tensor = torch.tensor(im, dtype=torch.float32).permute(2, 0, 1)
    im_tensor = F.interpolate(
        torch.unsqueeze(im_tensor, 0),
        size=model_input_size,
        mode="bilinear",
        align_corners=False,
    ).squeeze(0)
    im_tensor = im_tensor / 255.0  # Normalize the image to 0-1
    image = normalize(im_tensor, [0.5, 0.5, 0.5], [1.0, 1.0, 1.0])
    return image


###--------------------------------------------------------------------------###


def postprocess_image(result: torch.Tensor, im_size: list) -> np.ndarray:
    result = torch.squeeze(F.interpolate(result, size=im_size, mode="bilinear"), 0)
    ma = torch.max(result)
    mi = torch.min(result)
    result = (result - mi) / (ma - mi)
    im_array = (result * 255).permute(1, 2, 0).cpu().data.numpy().astype(np.uint8)
    im_array = np.squeeze(im_array)
    return im_array


###--------------------------------------------------------------------------###


def upload_to_S3(file_path, filename, folder):
    """upload file or folder to S3 bucket"""

    # Fetch environment variables
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    access_key = os.getenv("AWS_S3_ACCESS_KEY")
    secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")

    # Check if the environment variables are set
    if not all([bucket_name, access_key, secret_access_key]):
        raise Exception("Error: AWS S3 environment variables are not properly set.")

    try:
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
        )

        with open(file_path, "rb") as data:
            s3.Bucket(bucket_name).put_object(
                Key=f"{folder}/{filename}", Body=data, ACL="public-read"
            )

        return f"https://{bucket_name}.s3.amazonaws.com/{folder}/{filename}"

    except Exception as e:
        raise Exception(e)


###--------------------------------------------------------------------------###


def download_file(url: str, output_dir: str = "temp"):
    """Download file from the given URL and save it to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.basename(url)
    file_path = os.path.join(output_dir, file_name)

    # Check if file already exists to avoid re-downloading
    if not os.path.exists(file_path):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                return file_path
            else:
                e = f"Error: Unable to download the file. HTTP status code: {response.status_code}"
                logger.error(e)
        except requests.exceptions.RequestException as e:
            log_exception(e)
    else:
        logger.info(f"File already exists: {file_path}")
        return file_path
