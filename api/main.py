from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
# Import your existing app code
from app import app as music_app
# Import chatbot router
from chatbot import router as chatbot_router
# Import journal router
from journal import router as journal_router
# from apps.journal import router as journal_router

# Create main application
app = FastAPI(
    title="CalmVerse API",
    description="API for music recommendations, journaling, and mental health support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(music_app.router)  # Include your existing music app routes
app.include_router(chatbot_router)  # Include the mental health chatbot routes
app.include_router(journal_router)  # Include the journal routes

@app.get("/", tags=["Root"])
async def read_root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to the CalmVerse API",
        "features": [
            "Music Recommendations - Get personalized music suggestions based on your preferences",
            "Mental Health Support - Chat with our AI assistant for mental wellness guidance",
            "Journaling - Express thoughts, track moods, and receive guided prompts for reflection"
        ],
        "endpoints": {
            "music": "/songs, /recommend, /song_details",
            "mental_health": "/mental-health/chat",
            "journal": "/journal/entries, /journal/prompts, /journal/insights"
        }
    }

if __name__ == "__main__":
    # Set Groq API key from environment variables
    # os.environ["GROQ_API_KEY"] = ""  # For testing only, use proper env variables
    
    # Set MongoDB connection string
    # os.environ["MONGODB_URI"] = "mongodb://localhost:27017"  # For testing, use proper env variables
    
    # Run the application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)