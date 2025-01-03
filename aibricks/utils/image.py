import base64
import mimetypes


def image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_as_url(image_path):
    mime_type = mimetypes.guess_type(image_path)[0] or 'image/jpeg'  # fallback to jpeg if unknown
    return f"data:{mime_type};base64,{image_as_base64(image_path)}"
