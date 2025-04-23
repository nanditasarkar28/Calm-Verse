# CalmVerse API

This API provides music recommendations and mental health support features for the CalmVerse application.

## Features

- **Music Recommendations**: Get personalized music recommendations based on similarity to songs you like
- **Mental Health Chatbot**: Chat with an AI assistant that provides mental wellness guidance and resources

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```
   export GROQ_API_KEY=your_groq_api_key
   export SPOTIFY_CLIENT_ID=your_spotify_client_id
   export SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```
4. Run the application:
   ```
   python main.py
   ```

## API Endpoints

### Music Recommendation

- `GET /songs` - Get list of all available songs
- `GET /recommend?song=<song_name>` - Get song recommendations based on similarity
- `GET /song_details?song=<song_name>&artist=<artist_name>` - Get details for a specific song

### Mental Health Support

- `POST /mental-health/chat` - Chat with the mental health assistant
  - Request body: `{"message": "your message", "user_id": "user123", "session_id": "optional_session_id"}`
- `DELETE /mental-health/chat/{session_id}` - End a chat session

## Example Usage

```python
import requests

# Chat with the mental health bot
response = requests.post(
    "http://localhost:8000/mental-health/chat",
    json={
        "message": "I've been feeling anxious lately",
        "user_id": "user123"
    }
)

print(response.json())
```

## Requirements

- Python 3.8+
- Groq API key
- Spotify API credentials (for music recommendation features)