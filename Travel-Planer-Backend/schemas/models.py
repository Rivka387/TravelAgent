from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class DestinationRequest(BaseModel):
    """Model for parsing user's travel request"""
    destination: str
    duration: int  # days
    interests: List[str]
    budget: Optional[str] = None
    travel_style: Optional[str] = None

class Place(BaseModel):
    """Model for a travel destination/place"""
    name: str
    type: str
    description: str
    rating: Optional[float] = None
    address: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None
    opening_hours: Optional[str] = None
    price_level: Optional[int] = None

class DayPlan(BaseModel):
    """Model for a single day in the itinerary"""
    day: int
    date: Optional[str] = None
    activities: List[str]
    places: List[str]
    notes: Optional[str] = None

class Itinerary(BaseModel):
    """Complete travel itinerary model"""
    destination: str
    duration: int
    total_days: int
    daily_plans: List[DayPlan]
    general_tips: List[str]
    estimated_budget: Optional[str] = None

class TravelPreferences(BaseModel):
    """User's travel preferences"""
    accommodation_type: Optional[str] = None
    transportation: Optional[str] = None
    food_preferences: Optional[List[str]] = None
    activity_level: Optional[str] = None  # relaxed, moderate, active
    group_size: Optional[int] = None

# Response models for API
class PlaceSearchResponse(BaseModel):
    places: List[Place]
    total_found: int
    search_location: str

class ItineraryResponse(BaseModel):
    itinerary: Itinerary
    recommended_places: List[Place]
    status: str

print("Models defined successfully!")
print("Available models:")
print("- DestinationRequest: For parsing user travel requests")
print("- Place: For individual travel destinations")
print("- DayPlan: For daily itinerary planning")
print("- Itinerary: Complete travel plan")
print("- TravelPreferences: User preferences")