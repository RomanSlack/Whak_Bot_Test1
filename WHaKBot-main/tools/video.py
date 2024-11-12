#use this in moederation, expensive
import requests
from langchain.tools import tool
import subprocess
from pydantic import BaseModel, Field
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
class video_gen(BaseModel):
    video_desc: str = Field(    description="detailed description of the video to be generated"
    )


@tool("video_gen", args_schema=video_gen)
def video_gen(video_desc: str) -> str:
    """Use this tool for video generation"""
    print(f'SOLVING EXPRESSION: {expression}')
    url = "https://api.aivideoapi.com/runway/generate/text"

    payload = {
        "text_prompt": "A small child uses a diamond pickaxe to destroy a levitating pink crystal",
        "model": "gen3",
        "width": 1344,
        "height": 768,
        "motion": 5,
        "seed": 0,
        "upscale": True,
        "interpolate": True,
        "callback_url": "",
        "time": 5
     }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "15f5d2d4d533d461ca25214d5cd55b358"
     }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

    


