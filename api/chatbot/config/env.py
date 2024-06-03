import os

from dotenv import load_dotenv

load_dotenv("../.env")

# Secrets
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COLLEGE_SCORECARD_API_KEY = os.environ["COLLEGE_SCORECARD_API_KEY"]
