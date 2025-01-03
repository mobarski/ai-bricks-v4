import base64


def image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_as_url(image_path):
    extension = image_path.split(".")[-1]
    return f"data:image/{extension};base64,{image_as_base64(image_path)}"
