import uuid
from pathlib import Path
import requests
import base64
from PIL import Image
from io import BytesIO

from mimetypes import MimeTypes


from langchain.tools import tool
from openai import OpenAI
from pydantic import BaseModel, Field


#CLIENT = OpenAI(api_key="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")

api_key = "key-1TsWZR2IduvodtQnD8Fz646mavmu3Id500FTck88qAqu98XVQ4k1IfbF6EuPz7GHWUXbpfvFg2Ea4Zio7UKlMvaIdYVxNDpK"

class GenerateImageInput(BaseModel):
    image_description: str = Field(
        description="A detailed description of the desired image."
    )


@tool("generate_image2", args_schema=GenerateImageInput)
def generate_image2(image_description: str) -> str:
    """Call to generate an image with flux and make sure to remind the user to ask for a link in order to get it"""

    url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"
    t2i_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    t2i_input_params = {
        "prompt": image_description,
        "output_format": "jpeg",
        "width": 768,
        "height": 768,
    }

    response = requests.post(
        url,
        headers=t2i_headers,
        json=t2i_input_params
    )



    DIR_NAME = "./images/"
    dirpath = Path(DIR_NAME)
    # create parent dir if doesn't exist
    dirpath.mkdir(parents=True, exist_ok=True)

    decoded_image = base64.b64decode(response.json()['image'])

    image_name = 'currentImage.jpeg'
    image_path = dirpath / image_name

    with open(image_path, 'wb') as image_file:
        image_file.write(decoded_image)

    print(f"Image saved to {image_path}")



    return response.url


if __name__ == "__main__":  #this is just test
    print(generate_image.run("a picture of a crab"))