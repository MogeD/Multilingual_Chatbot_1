from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ml.inference import MultilingualChatbot

app = FastAPI(title="Multilingual Chatbot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = MultilingualChatbot()

class ChatMessage(BaseModel):
    message: str
    language: str

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = chatbot.generate_response(
            chat_message.message,
            chat_message.language
        )
        return {"response": response, "language": chat_message.language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported-languages")
async def get_supported_languages():
    return {"languages": chatbot.get_supported_languages()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 