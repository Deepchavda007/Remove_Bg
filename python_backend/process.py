import os
import uuid
import torch
import shutil
import subprocess
from PIL import Image
from skimage import io
from briarmbg import BriaRMBG
from utils import (
    postprocess_image,
    preprocess_image,
    create_response,
    download_file,
    upload_to_S3,
)


###--------------------------------------------------------------------------###


si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW


###--------------------------------------------------------------------------###


def remove_background(payload):
    required_params = ["image_url"]
    if any(param not in payload for param in required_params):
        return create_response(False, "Required parameters missing", {}, 400)

    image_url = payload.get("image_url")
    unique_id = payload.get("image_id", str(uuid.uuid4()))
    output_dir = os.path.join("temp", unique_id)
    os.makedirs(output_dir, exist_ok=True)

    try:
        img_path = download_file(image_url, output_dir)

        net = BriaRMBG()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
        net.to(device)
        net.eval()

        # prepare input
        model_input_size = [1024, 1024]
        orig_im = io.imread(img_path)
        orig_im_size = orig_im.shape[0:2]
        image = preprocess_image(orig_im, model_input_size).to(device)

        # inference
        image = image.unsqueeze(0)
        result = net(image)

        # post process
        result_image = postprocess_image(result[0][0], orig_im_size)

        # save result
        remove_bg_image = os.path.join(output_dir, f"{unique_id}_remove_bg.png")
        pil_im = Image.fromarray(result_image)
        no_bg_image = Image.new("RGBA", pil_im.size, (0, 0, 0, 0))
        orig_image = Image.open(img_path)
        no_bg_image.paste(orig_image, mask=pil_im)
        no_bg_image.save(remove_bg_image)

        remove_bg_url = upload_to_S3(
            remove_bg_image, f"{unique_id}_remove_bg.png", "remove_bg"
        )

        response = {
            "remove_bg_url": remove_bg_url,
            "unique_id": unique_id,
        }

        return create_response(True, "Background removed successfully", response, 200)
    except Exception as e:
        return create_response(False, str(e), {}, 500)
    finally:
        shutil.rmtree(output_dir)


###--------------------------------------------------------------------------###
