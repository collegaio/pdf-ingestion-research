from fastapi import FastAPI

from chatbot.server.conversations.route import router as conversations_router

app = FastAPI()

app.include_router(conversations_router)
