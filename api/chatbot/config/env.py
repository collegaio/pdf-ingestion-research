import os

from dotenv import load_dotenv

dotenv_path = "../.env"

if os.path.exists(dotenv_path):
    print("loading dotenv...")
    load_dotenv(dotenv_path)

# Secrets
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
COLLEGE_SCORECARD_API_KEY = os.environ["COLLEGE_SCORECARD_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
DATASETS_BUCKET = os.environ["DATASETS_BUCKET"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = os.environ["AWS_REGION"]
