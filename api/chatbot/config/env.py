import os

from dotenv import load_dotenv

dotenv_path = "../.env"

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Secrets
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COLLEGE_SCORECARD_API_KEY = os.environ["COLLEGE_SCORECARD_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
DATASETS_BUCKET = os.environ["DATASETS_BUCKET"]
# S3_ACCESS_KEY_ID = os.environ["S3_ACCESS_KEY_ID"]
# S3_SECRET_ACCESS_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
