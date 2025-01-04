import base64
import mimetypes
from functools import lru_cache

import requests


@lru_cache(maxsize=100)  # Cache last 100 downloaded images
def _download_image(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content


def image_as_base64(image_path):
    if image_path.startswith('http'):
        content = _download_image(image_path)
        return base64.b64encode(content).decode("utf-8")
    if image_path.startswith('file://'):
        image_path = image_path[7:]
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_as_url(image_path):
    if image_path.startswith('file://'):
        image_path = image_path[7:]
    mime_type = mimetypes.guess_type(image_path)[0] or 'image/jpeg'  # fallback to jpeg if unknown
    return f"data:{mime_type};base64,{image_as_base64(image_path)}"


def guess_mime_type(url_or_path):
    url = url_or_path
    if url.startswith('file://'):
        url = url[7:]
    elif url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    return mimetypes.guess_type(url)[0] or 'image/jpeg'  # fallback to jpeg if unknown
