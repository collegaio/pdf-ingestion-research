import os

from dotenv import load_dotenv

load_dotenv("../../.env")

COHERE_API_KEY = os.environ["COHERE_API_KEY"]
