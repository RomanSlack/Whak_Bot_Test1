import argparse
from typing import List, Tuple

import streamlit
from langchain.tools import tool
from langchain_core.documents import Document
from openai import OpenAI
from pydantic import BaseModel, Field
from pathlib import Path
import requests
import base64
from langchain.tools import tool
from pydantic import BaseModel, Field
import mysql.connector
from aws_link import upload_to_aws
from main import set_environment_variables
from tools.RAG import RetrievalAugmentedGeneration, clear_database, load_documents, split_documents, add_to_chroma, \
    SQL_RAG, load_documents_rag
from tools.interface import query_rag
from tools.getembedding import get_embedding_function
from langchain_chroma import Chroma
from tools.interface import CHROMA_PATH

CLIENT = OpenAI(api_key="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")


class GenerateImageInput(BaseModel):
    image_description: str = Field(
        description="A detailed description of the desired image."
    )


@tool("generate_image", args_schema=GenerateImageInput)
def generate_image(image_description: str) -> str:
    """Call to generate an image and make sure to remind the user to ask for a link in order to get it"""

    response = CLIENT.images.generate(
        model="dall-e-3",
        prompt=image_description,
        size="1024x1024",
        quality="standard",  # standard or hd
        n=1,
    )
    image_url = response.data[0].url
    return image_url




api_key = "key-1TsWZR2IduvodtQnD8Fz646mavmu3Id500FTck88qAqu98XVQ4k1IfbF6EuPz7GHWUXbpfvFg2Ea4Zio7UKlMvaIdYVxNDpK"

class GenerateImageInputFlux(BaseModel):
    image_description: str = Field(
        description="A detailed description of the desired image. Must be a SINGLE STRING"
    )


@tool("generate_image2", args_schema=GenerateImageInputFlux)
def generate_image2(image_description: str) -> str:
    """Input must be a SINGLE string. Call to generate an image and make sure to remind the user to ask for a link in order to get it"""

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


    return upload_to_aws(image_path.as_posix())




class GetDatabaseInformation(BaseModel):
    image_description: str = Field(
        description="Get all the previous user inputs and agent responses from a SQL database"
    )



@tool("get_data", args_schema=GetDatabaseInformation)


def get_data():
    """No input is required. The following tool will return previous interactions stored on a SQL database. Use this information to formulate your response"""
    conn = mysql.connector.connect(
        host="database-1.cxaqcs0sejmd.us-east-1.rds.amazonaws.com",
        user="admin",
        password="AmazonSucks$1",
        database="user_data"
    )
    cursor = conn.cursor()


    cursor.execute("SELECT user_query, agent_response FROM user_inputs")
    rows = cursor.fetchall()
    cursor.close()

    return rows

'''@tool("RAG", args_schema=RetrievalAugmentedGeneration)
def RAG_TOOL(filename: str, context: str) -> list[tuple[Document, float]]:
    """When you get a request for info that may be stored in a pdf in file 'data' you use this tool to retrieve info from the appropriate pdf file
    From there, provide the context (user question) to the tool so that it may process it"""
    set_environment_variables("WHaK AI")
    streamlit.write("This is the file utilized: " + filename)
    print("here3")
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()
    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)

    add_to_chroma(chunks)

    embedding_function = get_embedding_function()

    print("here")

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    print("here2")
    results = db.similarity_search_with_score(context, k=5)
    return results'''


@tool("SQL_RAG", args_schema=SQL_RAG)
def SQL_RAG(context: str) -> list[tuple[Document, float]]:
    """Search SQL database to get potential answer"""
    set_environment_variables("WHaK AI")


    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()


    # Create (or update) the data store.
    documents = load_documents_rag()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

    embedding_function = get_embedding_function()

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(context, k=5)
    return results






