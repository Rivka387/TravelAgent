from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
from typing import List, Dict, Any
import os
import traceback
from fastapi.middleware.cors import CORSMiddleware

# Import our agents and functions
from agents.functions import travel_functions
from agents.destination_agent import parse_destination_request
from agents.google_places_agent import search_places, get_place_recommendations
from agents.itinerary_agent import generate_itinerary

app = FastAPI(title="Travel Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או ["*"] לפיתוח
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

class TravelRequest(BaseModel):
    message: str

class TravelResponse(BaseModel):
    itinerary: str
    places: List[Dict[str, Any]]
    status: str
    destination_info: Dict[str, Any] = {}

@app.post("/plan-trip", response_model=TravelResponse)
async def plan_trip(request: TravelRequest):
    """
    Main endpoint for planning a trip based on user's natural language input
    """
    try:
        print(f"Received request: {request.message}")
        
        # Step 1: Parse the destination request directly
        print("Step 1: Parsing destination request...")
        try:
            destination_info = parse_destination_request(request.message)
            print(f"Parsed destination info: {destination_info}")
        except Exception as e:
            print(f"Error parsing destination: {e}")
            traceback.print_exc()
            return TravelResponse(
                itinerary=f"I had trouble understanding your travel request. Error: {str(e)}. Please try being more specific about your destination and duration.",
                places=[],
                status="error",
                destination_info={}
            )
        
        if not destination_info.get('destination') or destination_info['destination'] == 'Unknown':
            return TravelResponse(
                itinerary="I couldn't identify a specific destination from your request. Please specify a city or country you'd like to visit.",
                places=[],
                status="error",
                destination_info=destination_info
            )
        
        # Step 2: Search for places
        print("Step 2: Searching for places...")
        try:
            if 'get_place_recommendations' in globals():
                places = get_place_recommendations(
                    location=destination_info['destination'],
                    interests=destination_info.get('interests', ['general']),
                    max_places=15
                )
            else:
                places = search_places(
                    location=destination_info['destination'],
                    interests=destination_info.get('interests', ['general'])
                )
            print(f"Found {len(places)} places")
        except Exception as e:
            print(f"Error searching places: {e}")
            traceback.print_exc()
            # Continue with empty places list
            places = []
        
        # Step 3: Generate itinerary
        print("Step 3: Generating itinerary...")
        try:
            itinerary = generate_itinerary(
                destination=destination_info['destination'],
                duration=destination_info.get('duration', 7),
                places=places,
                interests=destination_info.get('interests', ['general']),
                travel_style=destination_info.get('travel_style', 'moderate')
            )
            
            # Ensure itinerary is a string
            if not isinstance(itinerary, str):
                itinerary = "Unable to generate detailed itinerary. Please try again."
            
            print("Successfully generated travel plan!")
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            traceback.print_exc()
            itinerary = f"I encountered an error while creating your itinerary: {str(e)}. Here's a simple plan instead:\n\n"
            itinerary += f"# Trip to {destination_info['destination']}\n\n"
            itinerary += f"Duration: {destination_info.get('duration', 7)} days\n"
            itinerary += f"Interests: {', '.join(destination_info.get('interests', ['general']))}\n\n"
            itinerary += "I recommend researching popular attractions and creating a day-by-day plan based on your interests."
        
        return TravelResponse(
            itinerary=itinerary,
            places=places,
            status="success",
            destination_info=destination_info
        )
        
    except Exception as e:
        print(f"Unexpected error in plan_trip: {str(e)}")
        traceback.print_exc()
        
        # Return a safe response instead of raising an exception
        return TravelResponse(
            itinerary=f"I encountered an unexpected error while planning your trip: {str(e)}. Please try rephrasing your request.",
            places=[],
            status="error",
            destination_info={}
        )

@app.get("/")
async def root():
    return {
        "message": "Travel Planner API is running!",
        "endpoints": {
            "plan_trip": "POST /plan-trip - Plan a complete trip",
            "health": "GET /health - Check API health",
            "test": "GET /test - Test the API components"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "openai_api": "configured" if openai.api_key else "not configured",
        "version": "1.0.0"
    }

@app.get("/test")
async def test_endpoint():
    """
    Test endpoint to verify all components work
    """
    try:
        # Test parsing
        test_request = "I want a 3-day trip to Rome with history and food"
        destination_info = parse_destination_request(test_request)
        
        # Test places search
        places = search_places(
            location=destination_info['destination'], 
            interests=destination_info['interests']
        )
        
        # Test itinerary generation
        itinerary = generate_itinerary(
            destination=destination_info['destination'],
            duration=destination_info['duration'],
            places=places[:5],  # Use fewer places for test
            interests=destination_info['interests']
        )
        
        return {
            "status": "success",
            "test_results": {
                "parsing": "✅ Working",
                "places_search": f"✅ Found {len(places)} places",
                "itinerary_generation": "✅ Working",
                "sample_destination": destination_info['destination'],
                "sample_duration": destination_info['duration']
            }
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e),
            "test_results": {
                "parsing": "❌ Failed",
                "places_search": "❌ Failed", 
                "itinerary_generation": "❌ Failed"
            }
        }

if __name__ == "__main__":
    import uvicorn
    print("Starting Travel Planner API...")
    print(f"OpenAI API Key: {'Configured' if openai.api_key else 'Not configured'}")
    uvicorn.run(app, host="0.0.0.0", port=8001)