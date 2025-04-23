# chatbot_example.py
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def chat_with_mental_health_bot(message, user_id, session_id=None):
    """Send a message to the mental health chatbot and get the response"""
    
    payload = {
        "message": message,
        "user_id": user_id
    }
    
    if session_id:
        payload["session_id"] = session_id
    
    response = requests.post(
        f"{BASE_URL}/mental-health/chat",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Bot: {result['response']}")
        
        if result.get('resources'):
            print("\nRecommended Resources:")
            for resource in result['resources']:
                print(f"- {resource['name']}")
        
        if result.get('emergency_contact'):
            print("\n⚠️ EMERGENCY RESOURCES PROVIDED - Please review carefully ⚠️")
        
        return result['session_id']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def end_chat_session(session_id):
    """End the current chat session"""
    response = requests.delete(f"{BASE_URL}/mental-health/chat/{session_id}")
    
    if response.status_code == 200:
        print("Chat session ended successfully")
    else:
        print(f"Error ending session: {response.status_code}")
        print(response.text)

def main():
    user_id = "user123"
    session_id = None
    
    print("CalmVerse Mental Health Assistant")
    print("Type 'exit' to end the conversation")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            if session_id:
                end_chat_session(session_id)
            break
        
        session_id = chat_with_mental_health_bot(user_input, user_id, session_id)

if __name__ == "__main__":
    main()