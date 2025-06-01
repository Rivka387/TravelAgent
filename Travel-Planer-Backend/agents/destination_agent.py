"""
Destination Agent - Responsible for parsing and understanding user travel requests
"""

import re
import openai
from typing import Dict, List, Any
import json
import os

def parse_destination_request(text: str) -> Dict[str, Any]:
    """
    Parse user's natural language travel request to extract:
    - Destination
    - Duration
    - Interests/preferences
    - Travel style
    """
    
    print(f"Parsing request: {text}")
    
    # Try GPT parsing first
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _gpt_parse(text)
        except Exception as e:
            print(f"GPT parsing failed: {e}, falling back to regex parsing")
            return _fallback_parse(text)
    else:
        print("No OpenAI API key found, using fallback parsing")
        return _fallback_parse(text)

def _gpt_parse(text: str) -> Dict[str, Any]:
    """
    Use GPT to parse the travel request intelligently
    """
    
    system_prompt = """
    You are an expert travel request parser. Extract the following information from user's travel request and return ONLY a valid JSON object:

    Required fields:
    - destination: The main destination (city, country, or region)
    - duration: Number of days (if not specified, use 7)
    - interests: Array of interests/activities mentioned
    - travel_style: One of: "budget", "moderate", "luxury", "relaxed", "packed", "adventure"
    - special_requirements: Array of any special needs mentioned

    Common interests include: food, history, nature, art, technology, adventure, relaxation, nightlife, shopping, culture, architecture, music, sports, photography, wildlife, beaches, mountains, museums, festivals, local_life

    Examples:
    Input: "I want a 5-day trip to Rome with history and food"
    Output: {"destination": "Rome, Italy", "duration": 5, "interests": ["history", "food"], "travel_style": "moderate", "special_requirements": []}

    Input: "Planning a relaxing week in Bali with beaches and spa"
    Output: {"destination": "Bali, Indonesia", "duration": 7, "interests": ["relaxation", "beaches", "spa"], "travel_style": "relaxed", "special_requirements": []}

    Return ONLY the JSON object, no other text.
    """
    
    try:
        # Using the new OpenAI API format
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as in the main.py
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Parse this travel request: {text}"}
            ],
            temperature=0.1,
            max_tokens=300
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"GPT response: {response_text}")
        
        # Try to parse the JSON response
        try:
            parsed_data = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                parsed_data = json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in GPT response")
        
        # Validate and clean the parsed data
        result = {
            "destination": parsed_data.get("destination", "").strip(),
            "duration": int(parsed_data.get("duration", 7)),
            "interests": [interest.strip().lower() for interest in parsed_data.get("interests", [])],
            "travel_style": parsed_data.get("travel_style", "moderate").lower(),
            "special_requirements": parsed_data.get("special_requirements", [])
        }
        
        # Validate destination
        if not result["destination"] or result["destination"].lower() == "unknown":
            print("GPT couldn't identify destination, using fallback")
            fallback_result = _fallback_parse(text)
            result["destination"] = fallback_result["destination"]
        
        # Ensure we have at least one interest
        if not result["interests"]:
            result["interests"] = ["general"]
        
        print(f"GPT parsed result: {result}")
        return result
        
    except Exception as e:
        print(f"Error in GPT parsing: {e}")
        raise e

def _fallback_parse(text: str) -> Dict[str, Any]:
    """
    Fallback parsing method using regex and keyword matching
    """
    text_lower = text.lower()
    
    # Extract duration
    duration_patterns = [
        r'(\d+)\s*days?',
        r'(\d+)\s*weeks?',
        r'(\d+)\s*months?'
    ]
    
    duration = 7  # default
    for pattern in duration_patterns:
        match = re.search(pattern, text_lower)
        if match:
            num = int(match.group(1))
            if 'week' in pattern:
                duration = num * 7
            elif 'month' in pattern:
                duration = num * 30
            else:
                duration = num
            break
    
    # Extract interests using keywords
    interest_keywords = {
        'nature': ['nature', 'hiking', 'mountains', 'forest', 'beach', 'outdoor', 'wildlife', 'park'],
        'food': ['food', 'cuisine', 'restaurant', 'culinary', 'cooking', 'eating', 'local food', 'dining'],
        'history': ['history', 'historical', 'museum', 'ancient', 'heritage', 'culture', 'historic'],
        'art': ['art', 'gallery', 'painting', 'sculpture', 'artistic', 'exhibition'],
        'technology': ['technology', 'tech', 'innovation', 'modern', 'digital', 'science'],
        'adventure': ['adventure', 'extreme', 'sports', 'climbing', 'diving', 'thrill'],
        'relaxation': ['relax', 'spa', 'peaceful', 'quiet', 'calm', 'rest', 'wellness'],
        'nightlife': ['nightlife', 'bars', 'clubs', 'party', 'entertainment', 'night'],
        'shopping': ['shopping', 'market', 'boutique', 'souvenir', 'mall', 'store']
    }
    
    interests = []
    for category, keywords in interest_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            interests.append(category)
    
    # Extract destination
    destination = _extract_destination(text)
    
    # Extract travel style
    travel_style = 'moderate'  # default
    if any(word in text_lower for word in ['luxury', 'expensive', 'high-end', 'premium']):
        travel_style = 'luxury'
    elif any(word in text_lower for word in ['budget', 'cheap', 'affordable', 'backpack']):
        travel_style = 'budget'
    elif any(word in text_lower for word in ['relax', 'slow', 'peaceful', 'calm']):
        travel_style = 'relaxed'
    elif any(word in text_lower for word in ['packed', 'busy', 'active', 'full']):
        travel_style = 'packed'
    
    result = {
        "destination": destination,
        "duration": duration,
        "interests": interests if interests else ["general"],
        "travel_style": travel_style,
        "special_requirements": []
    }
    
    print(f"Fallback parsed result: {result}")
    return result

def _extract_destination(text: str) -> str:
    """
    Extract destination from text using multiple strategies
    """
    text_lower = text.lower()
    
    # Enhanced destination mapping
    destination_mapping = {
        'rome': 'Rome, Italy',
        'italy': 'Italy',
        'japan': 'Japan',
        'tokyo': 'Tokyo, Japan',
        'kyoto': 'Kyoto, Japan',
        'osaka': 'Osaka, Japan',
        'paris': 'Paris, France',
        'france': 'France',
        'london': 'London, UK',
        'uk': 'United Kingdom',
        'england': 'England, UK',
        'spain': 'Spain',
        'madrid': 'Madrid, Spain',
        'barcelona': 'Barcelona, Spain',
        'seville': 'Seville, Spain',
        'greece': 'Greece',
        'athens': 'Athens, Greece',
        'santorini': 'Santorini, Greece',
        'mykonos': 'Mykonos, Greece',
        'thailand': 'Thailand',
        'bangkok': 'Bangkok, Thailand',
        'phuket': 'Phuket, Thailand',
        'chiang mai': 'Chiang Mai, Thailand',
        'india': 'India',
        'delhi': 'New Delhi, India',
        'mumbai': 'Mumbai, India',
        'goa': 'Goa, India',
        'rajasthan': 'Rajasthan, India',
        'new york': 'New York, USA',
        'usa': 'United States',
        'america': 'United States',
        'california': 'California, USA',
        'los angeles': 'Los Angeles, USA',
        'san francisco': 'San Francisco, USA',
        'las vegas': 'Las Vegas, USA',
        'miami': 'Miami, USA',
        'germany': 'Germany',
        'berlin': 'Berlin, Germany',
        'munich': 'Munich, Germany',
        'netherlands': 'Netherlands',
        'amsterdam': 'Amsterdam, Netherlands',
        'china': 'China',
        'beijing': 'Beijing, China',
        'shanghai': 'Shanghai, China',
        'australia': 'Australia',
        'sydney': 'Sydney, Australia',
        'melbourne': 'Melbourne, Australia',
        'canada': 'Canada',
        'toronto': 'Toronto, Canada',
        'vancouver': 'Vancouver, Canada',
        'brazil': 'Brazil',
        'rio': 'Rio de Janeiro, Brazil',
        'sao paulo': 'São Paulo, Brazil',
        'argentina': 'Argentina',
        'buenos aires': 'Buenos Aires, Argentina',
        'egypt': 'Egypt',
        'cairo': 'Cairo, Egypt',
        'turkey': 'Turkey',
        'istanbul': 'Istanbul, Turkey',
        'russia': 'Russia',
        'moscow': 'Moscow, Russia',
        'south korea': 'South Korea',
        'seoul': 'Seoul, South Korea',
        'vietnam': 'Vietnam',
        'hanoi': 'Hanoi, Vietnam',
        'ho chi minh': 'Ho Chi Minh City, Vietnam',
        'singapore': 'Singapore',
        'malaysia': 'Malaysia',
        'kuala lumpur': 'Kuala Lumpur, Malaysia',
        'indonesia': 'Indonesia',
        'bali': 'Bali, Indonesia',
        'jakarta': 'Jakarta, Indonesia',
        'philippines': 'Philippines',
        'manila': 'Manila, Philippines',
        'morocco': 'Morocco',
        'marrakech': 'Marrakech, Morocco',
        'casablanca': 'Casablanca, Morocco',
        'portugal': 'Portugal',
        'lisbon': 'Lisbon, Portugal',
        'porto': 'Porto, Portugal',
        'croatia': 'Croatia',
        'dubrovnik': 'Dubrovnik, Croatia',
        'split': 'Split, Croatia',
        'iceland': 'Iceland',
        'reykjavik': 'Reykjavik, Iceland',
        'norway': 'Norway',
        'oslo': 'Oslo, Norway',
        'bergen': 'Bergen, Norway',
        'sweden': 'Sweden',
        'stockholm': 'Stockholm, Sweden',
        'denmark': 'Denmark',
        'copenhagen': 'Copenhagen, Denmark'
    }
    
    # Check for exact matches first (longer phrases first)
    sorted_destinations = sorted(destination_mapping.items(), key=lambda x: len(x[0]), reverse=True)
    
    for key, value in sorted_destinations:
        if key in text_lower:
            return value
    
    # Try to find capitalized words that might be destinations
    words = text.split()
    for word in words:
        if word[0].isupper() and len(word) > 3:
            # Check if it's a common destination
            if word.lower() in destination_mapping:
                return destination_mapping[word.lower()]
            # Otherwise return as-is if it looks like a place name
            return word
    
    return "Unknown"