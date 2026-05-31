"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=500)


def generate_chatbot_response(message: str) -> str:
    normalized_message = message.lower()

    if any(greeting in normalized_message for greeting in ["hello", "hi", "hey"]):
        return "Hi! I can help with school activities and sign-up questions."

    if "activity" in normalized_message or "activities" in normalized_message:
        return f"Available activities: {', '.join(activities.keys())}."

    if "signup" in normalized_message or "sign up" in normalized_message or "register" in normalized_message:
        return "To sign up, choose an activity, enter your email, and click the Sign Up button."

    return "I can help with activities and sign-up questions. Ask me about available activities or how to register."


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/chatbot")
def chatbot(chat_request: ChatRequest):
    message = chat_request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    return {"response": generate_chatbot_response(message)}
