# # journal.py
# from fastapi import APIRouter, HTTPException, Depends, status
# from pydantic import BaseModel, Field
# from typing import List, Optional
# from datetime import datetime, timedelta
# from uuid import UUID, uuid4
# import random
# from fastapi.security import OAuth2PasswordBearer
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# import os
# from pydantic import json
# from bson.json_util import dumps, loads

# # MongoDB setup
# MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
# client = AsyncIOMotorClient(MONGODB_URL)
# db = client.calmverse
# journal_collection = db.journal_entries
# community_collection = db.community_posts

# # Sample authentication - in production, you'd implement proper auth
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# router = APIRouter(
#     prefix="/journal",
#     tags=["Journal"],
#     responses={404: {"description": "Not found"}},
# )

# # Helper class for ObjectId conversion
# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")

# # Models
# class JournalEntry(BaseModel):
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     user_id: str
#     title: str
#     content: str
#     mood: str = Field(description="User's mood when creating entry")
#     tags: List[str] = []
#     created_at: datetime = Field(default_factory=datetime.now)
#     updated_at: datetime = Field(default_factory=datetime.now)
#     is_private: bool = True
    
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str,
#             datetime: lambda dt: dt.isoformat()
#         }
    
# class JournalEntryCreate(BaseModel):
#     title: str
#     content: str
#     mood: str
#     tags: List[str] = []
#     is_private: bool = True

# class JournalEntryUpdate(BaseModel):
#     title: Optional[str] = None
#     content: Optional[str] = None
#     mood: Optional[str] = None
#     tags: Optional[List[str]] = None
#     is_private: Optional[bool] = None

# class PromptResponse(BaseModel):
#     prompt: str
#     category: str

# class CommunityPost(BaseModel):
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     journal_entry_id: PyObjectId
#     user_id: str
#     created_at: datetime = Field(default_factory=datetime.now)
#     likes: int = 0
#     comments: int = 0
    
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str,
#             datetime: lambda dt: dt.isoformat()
#         }

# # Helpers
# def get_user_id(token: str = Depends(oauth2_scheme)) -> str:
#     # Simplified auth for example - would validate token in production
#     return "user123" 

# # Journal entry CRUD operations
# @router.post("/entries", response_model=JournalEntry, status_code=status.HTTP_201_CREATED)
# async def create_journal_entry(entry: JournalEntryCreate, user_id: str = Depends(get_user_id)):
#     """Create a new journal entry"""
#     new_entry = JournalEntry(
#         user_id=user_id,
#         title=entry.title,
#         content=entry.content,
#         mood=entry.mood,
#         tags=entry.tags,
#         is_private=entry.is_private,
#         created_at=datetime.now(),
#         updated_at=datetime.now()
#     )
    
#     entry_dict = {k: v for k, v in new_entry.dict(by_alias=True).items() if v is not None}
#     if "_id" in entry_dict and entry_dict["_id"] is None:
#         del entry_dict["_id"]
        
#     result = await journal_collection.insert_one(entry_dict)
#     created_entry = await journal_collection.find_one({"_id": result.inserted_id})
    
#     return JournalEntry(**created_entry)

# @router.get("/entries", response_model=List[JournalEntry])
# async def get_journal_entries(
#     user_id: str = Depends(get_user_id),
#     skip: int = 0, 
#     limit: int = 10,
#     tag: Optional[str] = None,
#     mood: Optional[str] = None,
#     start_date: Optional[datetime] = None,
#     end_date: Optional[datetime] = None
# ):
#     """Get user's journal entries with optional filtering"""
#     query = {"user_id": user_id}
    
#     # Apply filters
#     if tag:
#         query["tags"] = {"$in": [tag]}
#     if mood:
#         query["mood"] = mood
#     if start_date:
#         query["created_at"] = {"$gte": start_date}
#     if end_date:
#         if "created_at" in query:
#             query["created_at"]["$lte"] = end_date
#         else:
#             query["created_at"] = {"$lte": end_date}
    
#     cursor = journal_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
#     entries = await cursor.to_list(length=limit)
    
#     return [JournalEntry(**entry) for entry in entries]

# @router.get("/entries/{entry_id}", response_model=JournalEntry)
# async def get_journal_entry(entry_id: str, user_id: str = Depends(get_user_id)):
#     """Get a specific journal entry by ID"""
#     try:
#         object_id = PyObjectId(entry_id)
#     except:
#         raise HTTPException(status_code=400, detail="Invalid ID format")
        
#     entry = await journal_collection.find_one({"_id": object_id, "user_id": user_id})
#     if entry:
#         return JournalEntry(**entry)
    
#     raise HTTPException(status_code=404, detail="Journal entry not found")

# @router.put("/entries/{entry_id}", response_model=JournalEntry)
# async def update_journal_entry(
#     entry_id: str, 
#     entry_update: JournalEntryUpdate,
#     user_id: str = Depends(get_user_id)
# ):
#     """Update a journal entry"""
#     try:
#         object_id = PyObjectId(entry_id)
#     except:
#         raise HTTPException(status_code=400, detail="Invalid ID format")
    
#     # Filter out None values
#     update_data = {k: v for k, v in entry_update.dict().items() if v is not None}
    
#     # Add updated timestamp
#     update_data["updated_at"] = datetime.now()
    
#     if update_data:
#         result = await journal_collection.update_one(
#             {"_id": object_id, "user_id": user_id},
#             {"$set": update_data}
#         )
        
#         if result.modified_count == 0:
#             # Check if entry exists
#             entry = await journal_collection.find_one({"_id": object_id})
#             if not entry:
#                 raise HTTPException(status_code=404, detail="Journal entry not found")
    
#     updated_entry = await journal_collection.find_one({"_id": object_id, "user_id": user_id})
#     if updated_entry:
#         return JournalEntry(**updated_entry)
    
#     raise HTTPException(status_code=404, detail="Journal entry not found")

# @router.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_journal_entry(entry_id: str, user_id: str = Depends(get_user_id)):
#     """Delete a journal entry"""
#     try:
#         object_id = PyObjectId(entry_id)
#     except:
#         raise HTTPException(status_code=400, detail="Invalid ID format")
        
#     # Delete associated community posts first
#     await community_collection.delete_many({"journal_entry_id": object_id})
    
#     # Then delete the entry
#     result = await journal_collection.delete_one({"_id": object_id, "user_id": user_id})
    
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Journal entry not found")

# # Journal prompts
# JOURNAL_PROMPTS = {
#     "gratitude": [
#         "List three things you're grateful for today and why.",
#         "Describe a person who helped you recently. How did they impact your day?",
#         "What's something in your daily routine that you appreciate but often take for granted?",
#         "Think about a challenge you've overcome. What positive lessons came from it?",
#         "What's something in nature that brought you joy today?"
#     ],
#     "reflection": [
#         "What was the most meaningful part of your day?",
#         "Describe a moment today when you felt really engaged or focused. What contributed to that?",
#         "What's something you learned about yourself today?",
#         "If you could change one decision you made today, what would it be and why?",
#         "What emotions were most present for you today? What triggered them?"
#     ],
#     "mindfulness": [
#         "Describe your surroundings right now using all five senses.",
#         "What physical sensations are you aware of in your body right now?",
#         "What thoughts keep coming up for you today? Can you observe them without judgment?",
#         "Describe your breathing pattern right now. Try taking 5 deep breaths and note how you feel after.",
#         "Choose an everyday activity. How can you bring more mindfulness to it tomorrow?"
#     ],
#     "goals": [
#         "What's one small step you can take tomorrow toward a bigger goal?",
#         "Describe your ideal day. What elements could you realistically incorporate into your life now?",
#         "What's a habit you'd like to develop? How might you start implementing it?",
#         "What's something that's holding you back right now? How might you address it?",
#         "What would you like to be celebrating about yourself one year from now?"
#     ],
#     "stress_relief": [
#         "Describe a place where you feel completely at peace. What details make it special?",
#         "What activities help you relieve stress? How could you make more time for them?",
#         "Write about a worry you're carrying. What's one small action you could take to address it?",
#         "List three self-care activities you could do in 5 minutes or less.",
#         "What boundaries might you need to set to protect your mental well-being?"
#     ]
# }

# @router.get("/prompts/random", response_model=PromptResponse)
# async def get_random_prompt(category: Optional[str] = None):
#     """Get a random journaling prompt, optionally filtered by category"""
#     if category and category not in JOURNAL_PROMPTS:
#         raise HTTPException(status_code=400, detail=f"Category not found. Available categories: {list(JOURNAL_PROMPTS.keys())}")
    
#     if category:
#         prompts = JOURNAL_PROMPTS[category]
#         return {"prompt": random.choice(prompts), "category": category}
#     else:
#         chosen_category = random.choice(list(JOURNAL_PROMPTS.keys()))
#         return {"prompt": random.choice(JOURNAL_PROMPTS[chosen_category]), "category": chosen_category}

# @router.get("/prompts/categories")
# async def get_prompt_categories():
#     """Get available prompt categories"""
#     return {"categories": list(JOURNAL_PROMPTS.keys())}

# # Mood tracking
# @router.get("/mood/history")
# async def get_mood_history(
#     user_id: str = Depends(get_user_id),
#     days: int = 7
# ):
#     """Get mood history for the specified number of past days"""
#     start_date = datetime.now() - timedelta(days=days)
    
#     pipeline = [
#         {"$match": {"user_id": user_id, "created_at": {"$gte": start_date}}},
#         {"$project": {
#             "date_str": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
#             "mood": 1
#         }},
#         {"$group": {
#             "_id": "$date_str",
#             "moods": {"$push": "$mood"}
#         }},
#         {"$sort": {"_id": 1}}
#     ]
    
#     cursor = journal_collection.aggregate(pipeline)
#     results = await cursor.to_list(length=100)
    
#     mood_data = {result["_id"]: result["moods"] for result in results}
    
#     return {"mood_history": mood_data}

# # Journal insights and analytics
# @router.get("/insights")
# async def get_journal_insights(user_id: str = Depends(get_user_id)):
#     """Get insights based on journal entries"""
#     # Count total entries
#     total_entries = await journal_collection.count_documents({"user_id": user_id})
    
#     if total_entries == 0:
#         return {"message": "No journal entries found to generate insights"}
    
#     # Calculate average length
#     pipeline_avg_length = [
#         {"$match": {"user_id": user_id}},
#         {"$project": {"content_length": {"$strLenCP": "$content"}}},
#         {"$group": {"_id": None, "avg_length": {"$avg": "$content_length"}}}
#     ]
#     avg_length_result = await journal_collection.aggregate(pipeline_avg_length).to_list(length=1)
#     avg_length = round(avg_length_result[0]["avg_length"]) if avg_length_result else 0
    
#     # Count moods
#     pipeline_moods = [
#         {"$match": {"user_id": user_id}},
#         {"$group": {"_id": "$mood", "count": {"$sum": 1}}},
#         {"$sort": {"count": -1}}
#     ]
#     mood_results = await journal_collection.aggregate(pipeline_moods).to_list(length=100)
#     mood_counts = {result["_id"]: result["count"] for result in mood_results}
    
#     # Count tags
#     pipeline_tags = [
#         {"$match": {"user_id": user_id}},
#         {"$unwind": "$tags"},
#         {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
#         {"$sort": {"count": -1}},
#         {"$limit": 5}
#     ]
#     tag_results = await journal_collection.aggregate(pipeline_tags).to_list(length=5)
#     most_common_tags = [(result["_id"], result["count"]) for result in tag_results]
    
#     # Get dates for first and most recent entries
#     first_entry = await journal_collection.find_one(
#         {"user_id": user_id},
#         sort=[("created_at", 1)]
#     )
    
#     most_recent_entry = await journal_collection.find_one(
#         {"user_id": user_id},
#         sort=[("created_at", -1)]
#     )
    
#     # Calculate streak
#     pipeline_streak = [
#         {"$match": {"user_id": user_id}},
#         {"$project": {"date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}}},
#         {"$group": {"_id": "$date"}},
#         {"$sort": {"_id": -1}}
#     ]
    
#     unique_dates = await journal_collection.aggregate(pipeline_streak).to_list(length=100)
#     date_strings = [entry["_id"] for entry in unique_dates]
    
#     streak = 0
#     if date_strings:
#         current_date = datetime.now().date()
#         for date_str in date_strings:
#             entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#             if (current_date - entry_date).days <= 1:
#                 streak += 1
#                 current_date = entry_date
#             else:
#                 break
    
#     return {
#         "total_entries": total_entries,
#         "average_length": avg_length,
#         "mood_distribution": mood_counts,
#         "common_themes": most_common_tags,
#         "current_streak": streak,
#         "first_entry_date": first_entry["created_at"] if first_entry else None,
#         "most_recent_entry": most_recent_entry["created_at"] if most_recent_entry else None,
#     }

# # Community features (for shared journals)
# @router.post("/community/share/{entry_id}", response_model=CommunityPost)
# async def share_to_community(entry_id: str, user_id: str = Depends(get_user_id)):
#     """Share a journal entry to the community"""
#     try:
#         object_id = PyObjectId(entry_id)
#     except:
#         raise HTTPException(status_code=400, detail="Invalid ID format")
    
#     # Check if entry exists and belongs to user
#     entry = await journal_collection.find_one({"_id": object_id, "user_id": user_id})
#     if not entry:
#         raise HTTPException(status_code=404, detail="Journal entry not found")
    
#     # Update privacy setting if needed
#     if entry["is_private"]:
#         await journal_collection.update_one(
#             {"_id": object_id}, 
#             {"$set": {"is_private": False}}
#         )
    
#     # Check if already shared
#     existing_post = await community_collection.find_one({"journal_entry_id": object_id})
#     if existing_post:
#         return CommunityPost(**existing_post)
    
#     # Create new community post
#     post = CommunityPost(
#         journal_entry_id=object_id,
#         user_id=user_id,
#         created_at=datetime.now(),
#         likes=0,
#         comments=0
#     )
    
#     post_dict = {k: v for k, v in post.dict(by_alias=True).items() if v is not None}
#     if "_id" in post_dict and post_dict["_id"] is None:
#         del post_dict["_id"]
    
#     result = await community_collection.insert_one(post_dict)
#     created_post = await community_collection.find_one({"_id": result.inserted_id})
    
#     return CommunityPost(**created_post)

# @router.get("/community/feed", response_model=List[dict])
# async def get_community_feed(skip: int = 0, limit: int = 10):
#     """Get shared journal entries from the community"""
#     pipeline = [
#         {"$sort": {"created_at": -1}},
#         {"$skip": skip},
#         {"$limit": limit},
#         {"$lookup": {
#             "from": "journal_entries",
#             "localField": "journal_entry_id",
#             "foreignField": "_id",
#             "as": "entry"
#         }},
#         {"$unwind": "$entry"},
#         {"$match": {"entry.is_private": False}},
#         {"$project": {
#             "post": "$$ROOT",
#             "entry": {
#                 "title": "$entry.title",
#                 "content": "$entry.content",
#                 "mood": "$entry.mood",
#                 "tags": "$entry.tags",
#                 "created_at": "$entry.created_at"
#             }
#         }}
#     ]
    
#     results = await community_collection.aggregate(pipeline).to_list(length=limit)
    
#     # Convert ObjectIds to strings for JSON serialization
#     for result in results:
#         result["post"]["_id"] = str(result["post"]["_id"])
#         result["post"]["journal_entry_id"] = str(result["post"]["journal_entry_id"])
    
#     return results

# # Mental health features
# class MentalHealthTip(BaseModel):
#     tip: str
#     category: str

# MENTAL_HEALTH_TIPS = {
#     "anxiety": [
#         "Practice box breathing: inhale for 4 counts, hold for 4, exhale for 4, hold for 4.",
#         "Try the 5-4-3-2-1 technique: identify 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, and 1 thing you taste.",
#         "Progressive muscle relaxation can help release physical tension caused by anxiety.",
#         "Schedule a 'worry time' – set aside a specific time to address your worries, then try to let them go outside that time.",
#         "Challenge unhelpful thoughts by asking yourself: 'What's the evidence for and against this thought?'"
#     ],
#     "stress": [
#         "Take short breaks throughout your day to reset your mind and reduce stress buildup.",
#         "Consider limiting news and social media consumption if it's increasing your stress levels.",
#         "Physical activity, even a short walk, can reduce stress hormones and boost endorphins.",
#         "Try mindful eating: slow down and fully experience your food without distractions.",
#         "Laughter genuinely helps reduce stress - watch a funny video or call a friend who makes you laugh."
#     ],
#     "mood": [
#         "Morning sunlight exposure can help regulate your circadian rhythm and boost mood.",
#         "Try the 'three good things' exercise: write down three positive things that happened today.",
#         "Small accomplishments matter - break tasks into manageable steps and celebrate completing them.",
#         "Social connection is powerful for mood - reach out to someone even when you don't feel like it.",
#         "Music can significantly impact mood - create playlists for different emotional states."
#     ],
#     "sleep": [
#         "Create a consistent sleep schedule, even on weekends, to help regulate your body clock.",
#         "Make your bedroom a sleep sanctuary: dark, quiet, cool, and comfortable.",
#         "Limit screen time 1-2 hours before bed to reduce blue light exposure.",
#         "If you can't fall asleep after 20 minutes, get up and do something relaxing until you feel sleepy.",
#         "Consider a bedtime routine that signals to your body it's time to wind down."
#     ],
#     "mindfulness": [
#         "Practice 'noting' thoughts: mentally label thoughts as they arise without judgment.",
#         "Try 'mindful listening' - fully focus on sounds around you as a quick mindfulness practice.",
#         "Use everyday triggers (like a phone ringing) as reminders to take a conscious breath.",
#         "Notice the sensation of your feet touching the ground as you walk.",
#         "Practice eating one meal a day without distractions, fully focusing on the experience."
#     ]
# }

# @router.get("/mental-health/tips/random", response_model=MentalHealthTip)
# async def get_random_mental_health_tip(category: Optional[str] = None):
#     """Get a random mental health tip, optionally filtered by category"""
#     if category and category not in MENTAL_HEALTH_TIPS:
#         raise HTTPException(status_code=400, detail=f"Category not found. Available categories: {list(MENTAL_HEALTH_TIPS.keys())}")
    
#     if category:
#         tips = MENTAL_HEALTH_TIPS[category]
#         return {"tip": random.choice(tips), "category": category}
#     else:
#         chosen_category = random.choice(list(MENTAL_HEALTH_TIPS.keys()))
#         return {"tip": random.choice(MENTAL_HEALTH_TIPS[chosen_category]), "category": chosen_category}

# @router.get("/mental-health/tips/categories")
# async def get_mental_health_tip_categories():
#     """Get available mental health tip categories"""
#     return {"categories": list(MENTAL_HEALTH_TIPS.keys())}



# journals.py
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from pymongo import MongoClient
import os
from bson import ObjectId
from bson.json_util import dumps
import json
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.calmverse
journal_collection = db.journals

# Create router
router = APIRouter(prefix="/journal", tags=["Journal"])

# Models
class JournalEntry(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    mood: str = Field(None)
    tags: List[str] = []
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Finding peace today",
                "content": "I took some time to meditate this morning and it really helped clear my mind...",
                "mood": "calm",
                "tags": ["meditation", "morning", "reflection"]
            }
        }

class JournalEntryDB(JournalEntry):
    id: str = None
    created_at: datetime = None
    
class JournalPrompt(BaseModel):
    prompt: str
    category: str

# List of prompts for users
journal_prompts = [
    JournalPrompt(prompt="What made you smile today?", category="gratitude"),
    JournalPrompt(prompt="Describe three things you're grateful for right now.", category="gratitude"),
    JournalPrompt(prompt="What's one small win you had today?", category="achievements"),
    JournalPrompt(prompt="How did you practice self-care today?", category="self-care"),
    JournalPrompt(prompt="What's something that challenged you today and how did you respond?", category="growth"),
    JournalPrompt(prompt="Describe a moment of calm you experienced recently.", category="mindfulness"),
    JournalPrompt(prompt="What's one thing you're looking forward to tomorrow?", category="hope"),
    JournalPrompt(prompt="If your emotions today were weather, what would they be and why?", category="emotions"),
    JournalPrompt(prompt="Write a letter to your future self about how you're feeling right now.", category="reflection"),
    JournalPrompt(prompt="What's one small change you could make tomorrow to improve your wellbeing?", category="self-improvement")
]

# Helper function to parse ObjectId
def parse_json(data):
    return json.loads(dumps(data))

# Routes
@router.post("/entries", response_description="Create a new journal entry")
async def create_journal_entry(journal: JournalEntry = Body(...)):
    """Create a new journal entry in the database"""
    journal_dict = journal.dict()
    journal_dict["created_at"] = datetime.now()
    
    new_journal = journal_collection.insert_one(journal_dict)
    created_journal = journal_collection.find_one({"_id": new_journal.inserted_id})
    
    return parse_json(created_journal)

@router.get("/entries", response_description="List all journal entries")
async def list_journal_entries():
    """Retrieve all journal entries from the database"""
    journals = journal_collection.find().sort("created_at", -1)
    return parse_json(journals)

@router.get("/entries/{id}", response_description="Get a single journal entry")
async def get_journal_entry(id: str):
    """Retrieve a specific journal entry by ID"""
    try:
        if journal := journal_collection.find_one({"_id": ObjectId(id)}):
            return parse_json(journal)
        
        raise HTTPException(status_code=404, detail=f"Journal entry with ID {id} not found")
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid ID format")

@router.delete("/entries/{id}", response_description="Delete a journal entry")
async def delete_journal_entry(id: str):
    """Delete a journal entry by ID"""
    try:
        delete_result = journal_collection.delete_one({"_id": ObjectId(id)})
        
        if delete_result.deleted_count == 1:
            return {"message": f"Journal entry with ID {id} deleted successfully"}
            
        raise HTTPException(status_code=404, detail=f"Journal entry with ID {id} not found")
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid ID format")

@router.put("/entries/{id}", response_description="Update a journal entry")
async def update_journal_entry(id: str, journal: JournalEntry = Body(...)):
    """Update a journal entry by ID"""
    try:
        journal_dict = journal.dict(exclude_unset=True)
        
        update_result = journal_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": journal_dict}
        )
        
        if update_result.modified_count == 1:
            if updated_journal := journal_collection.find_one({"_id": ObjectId(id)}):
                return parse_json(updated_journal)
        
        if (
            journal_collection.find_one({"_id": ObjectId(id)}) is None
        ):
            raise HTTPException(status_code=404, detail=f"Journal entry with ID {id} not found")
            
        return parse_json(journal_collection.find_one({"_id": ObjectId(id)}))
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid ID format or update data")

@router.get("/prompts", response_description="Get journal prompts")
async def get_journal_prompts():
    """Return a list of journal prompts to inspire writing"""
    return journal_prompts

@router.get("/insights", response_description="Get journal insights")
async def get_journal_insights():
    """Generate insights based on journal entries (frequency, mood patterns, etc.)"""
    # Count total entries
    total_entries = journal_collection.count_documents({})
    
    # Get most used moods
    mood_pipeline = [
        {"$match": {"mood": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$mood", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    mood_data = list(journal_collection.aggregate(mood_pipeline))
    
    # Get most used tags
    tag_pipeline = [
        {"$match": {"tags": {"$exists": True, "$ne": []}}},
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    tag_data = list(journal_collection.aggregate(tag_pipeline))
    
    # Get entries per week
    date_pipeline = [
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%U", "date": "$created_at"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": -1}},
        {"$limit": 10}
    ]
    date_data = list(journal_collection.aggregate(date_pipeline))
    
    return {
        "total_entries": total_entries,
        "top_moods": parse_json(mood_data),
        "top_tags": parse_json(tag_data),
        "entries_by_week": parse_json(date_data),
        "message": "Continue journaling regularly to see more detailed insights!"
    }