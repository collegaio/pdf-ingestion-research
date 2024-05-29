FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "fastapi", "run", "chatbot/server/app.py", "--port", "8000" ]
