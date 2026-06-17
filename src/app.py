"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
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
        "description": "A club for students who enjoy playing chess.",
        "participants": []
    },
    "Robotics Team": {
        "description": "Design and build robots to compete in local and national competitions.",
        "participants": []
    },
    "Drama Club": {
        "description": "Perform plays and skits throughout the school year.",
        "participants": []
    }
}

# Additional activities
activities.update({
    "Soccer Team": {
        "description": "Competitive soccer team practicing and playing matches against other schools.",
        "participants": []
    },
    "Basketball Team": {
        "description": "School basketball team that competes in regional leagues and tournaments.",
        "participants": []
    },
    "Art Club": {
        "description": "A space for students to explore drawing, painting, and other visual arts.",
        "participants": []
    },
    "Music Ensemble": {
        "description": "Group for students interested in performing instrumental and vocal music together.",
        "participants": []
    },
    "Debate Club": {
        "description": "Practice debate skills, research current events, and compete in tournaments.",
        "participants": []
    },
    "Science Olympiad": {
        "description": "Prepare for science and engineering challenges and regional Science Olympiad competitions.",
        "participants": []
    }
})

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

    # Check if the student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
