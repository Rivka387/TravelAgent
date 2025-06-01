"""
Function definitions for OpenAI function calling.
These functions define what GPT can call to help with travel planning.
"""

travel_functions = [
    {
        "name": "parse_destination_request",
        "description": "Parse user's natural language travel request to extract destination, duration, and interests",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The user's travel request text to parse"
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "search_places",
        "description": "Search for places and attractions based on location and interests",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The destination location to search in"
                },
                "interests": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of user interests (e.g., 'nature', 'food', 'history', 'technology')"
                },
                "place_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Types of places to search for (e.g., 'restaurant', 'museum', 'park')",
                    "default": []
                }
            },
            "required": ["location", "interests"]
        }
    },
    {
        "name": "generate_itinerary",
        "description": "Generate a detailed day-by-day travel itinerary",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "The travel destination"
                },
                "duration": {
                    "type": "integer",
                    "description": "Number of days for the trip"
                },
                "places": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of places to include in the itinerary"
                },
                "interests": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "User's interests to focus on"
                },
                "travel_style": {
                    "type": "string",
                    "description": "Travel style preference (relaxed, moderate, packed)",
                    "default": "moderate"
                }
            },
            "required": ["destination", "duration", "places", "interests"]
        }
    },
    {
        "name": "get_travel_tips",
        "description": "Get specific travel tips and recommendations for a destination",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "The travel destination"
                },
                "tip_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Categories of tips needed (e.g., 'transportation', 'food', 'culture', 'safety')"
                }
            },
            "required": ["destination"]
        }
    }
]

# Function metadata for documentation
function_descriptions = {
    "parse_destination_request": "Analyzes user's travel request to extract key information",
    "search_places": "Finds relevant places and attractions based on user preferences",
    "generate_itinerary": "Creates a structured day-by-day travel plan",
    "get_travel_tips": "Provides destination-specific travel advice"
}