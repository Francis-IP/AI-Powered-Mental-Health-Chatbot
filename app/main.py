from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .chatbot import MentalHealthBot

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

chatbot = MentalHealthBot()

class UserMessage(BaseModel):
    message: str

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(user_message: UserMessage):
    response = chatbot.get_response(user_message.message)
    return response

# Add this new route for mood history
@app.get("/mood-history")
async def get_mood_history():
    return {"mood_data": chatbot.mood_tracker.get_mood_summary()}

# Optional: Add a route to get mood patterns
@app.get("/mood-pattern")
async def get_mood_pattern():
    return {"mood_pattern": chatbot.mood_tracker.get_mood_pattern()}