"""
Google Places Agent - Handles searching for places and attractions
"""

from typing import List, Dict, Any
import os

class GooglePlacesService:
    """
    Service class for interacting with Google Places API
    """
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        self.use_mock_data = not self.api_key
        
    def search_places(self, location: str, place_type: str, radius: int = 50000) -> List[Dict[str, Any]]:
        """
        Search for places near a location (mock implementation)
        """
        print(f"Searching for {place_type} in {location}")
        
        # Use mock data for demonstration
        return self._get_mock_places(location, place_type)
    
    def _get_mock_places(self, location: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Generate mock places data for demonstration
        """
        
        mock_data = {
            'rome': {
                'tourist_attraction': [
                    {'name': 'Colosseum', 'rating': 4.6, 'description': 'Ancient Roman amphitheater and gladiator arena'},
                    {'name': 'Vatican Museums', 'rating': 4.5, 'description': 'World-renowned art collection including Sistine Chapel'},
                    {'name': 'Trevi Fountain', 'rating': 4.4, 'description': 'Baroque fountain where wishes come true'},
                    {'name': 'Pantheon', 'rating': 4.5, 'description': 'Best-preserved Roman building with impressive dome'},
                    {'name': 'Roman Forum', 'rating': 4.3, 'description': 'Ancient Roman marketplace and political center'}
                ],
                'restaurant': [
                    {'name': 'Da Enzo al 29', 'rating': 4.7, 'description': 'Authentic Roman trattoria in Trastevere'},
                    {'name': 'Checchino dal 1887', 'rating': 4.5, 'description': 'Historic restaurant serving traditional Roman cuisine'},
                    {'name': 'Piperno', 'rating': 4.4, 'description': 'Famous for carciofi alla giudia since 1860'},
                    {'name': 'Il Sorpasso', 'rating': 4.3, 'description': 'Modern bistro with excellent wine selection'}
                ],
                'museum': [
                    {'name': 'Capitoline Museums', 'rating': 4.4, 'description': 'Oldest public museums with ancient Roman statues'},
                    {'name': 'Palazzo Altemps', 'rating': 4.2, 'description': 'Renaissance palace housing ancient sculptures'},
                    {'name': 'Baths of Diocletian', 'rating': 4.1, 'description': 'Ancient Roman public baths complex'}
                ]
            },
            'tokyo': {
                'tourist_attraction': [
                    {'name': 'Senso-ji Temple', 'rating': 4.3, 'description': 'Ancient Buddhist temple in Asakusa'},
                    {'name': 'Tokyo Skytree', 'rating': 4.2, 'description': 'Tallest tower in Japan with panoramic views'},
                    {'name': 'Meiji Shrine', 'rating': 4.4, 'description': 'Shinto shrine dedicated to Emperor Meiji'},
                    {'name': 'Tsukiji Outer Market', 'rating': 4.1, 'description': 'Famous fish market and food destination'}
                ],
                'restaurant': [
                    {'name': 'Sukiyabashi Jiro', 'rating': 4.8, 'description': 'World-famous sushi restaurant'},
                    {'name': 'Ramen Yashichi', 'rating': 4.5, 'description': 'Authentic ramen shop in Shibuya'},
                    {'name': 'Tonki', 'rating': 4.4, 'description': 'Traditional tonkatsu restaurant since 1939'}
                ]
            }
        }
        
        # Normalize location name
        location_key = location.lower().split(',')[0].strip()
        
        # Get places for the location and type
        places_data = []
        
        # Try to find exact match for location
        if location_key in mock_data:
            if place_type in mock_data[location_key]:
                places_data = mock_data[location_key][place_type]
        
        # If no exact match, generate some generic places
        if not places_data:
            generic_places = [
                {'name': f'{location} Museum', 'rating': 4.2, 'description': 'Main museum in the area'},
                {'name': f'{location} Park', 'rating': 4.0, 'description': 'Beautiful park with local flora'},
                {'name': f'{location} Historical Site', 'rating': 4.1, 'description': 'Important historical landmark'},
                {'name': f'{location} Restaurant', 'rating': 4.3, 'description': 'Popular local cuisine restaurant'},
                {'name': f'{location} Market', 'rating': 3.9, 'description': 'Traditional market with local products'}
            ]
            places_data = generic_places
        
        # Convert to standard format
        places = []
        for i, place_data in enumerate(places_data):
            place = {
                'name': place_data['name'],
                'type': place_type,
                'rating': place_data.get('rating', 4.0),  # Default rating if none provided
                'address': f"{location}",
                'coordinates': {'lat': 41.9028 + i*0.01, 'lng': 12.4964 + i*0.01},  # Mock coordinates
                'description': place_data.get('description', 'A popular destination'),
                'place_id': f"mock_{location_key}_{place_type}_{i}"
            }
            places.append(place)
        
        return places

def search_places(location: str, interests: List[str], place_types: List[str] = None) -> List[Dict[str, Any]]:
    """
    Search for places based on location and user interests
    """
    
    print(f"Searching for places in {location} with interests: {interests}")
    
    # Initialize the Google Places service
    places_service = GooglePlacesService()
    
    # Map interests to place types
    interest_to_place_types = {
        'food': ['restaurant', 'cafe', 'bakery', 'meal_takeaway'],
        'nature': ['park', 'natural_feature', 'zoo'],
        'history': ['museum', 'church', 'tourist_attraction'],
        'art': ['art_gallery', 'museum'],
        'technology': ['electronics_store', 'museum'],
        'adventure': ['amusement_park', 'gym', 'tourist_attraction'],
        'relaxation': ['spa', 'park', 'beach'],
        'shopping': ['shopping_mall', 'store', 'clothing_store'],
        'general': ['tourist_attraction', 'point_of_interest']
    }
    
    # Determine place types to search for
    if not place_types:
        place_types = []
        for interest in interests:
            if interest in interest_to_place_types:
                place_types.extend(interest_to_place_types[interest])
        
        # Remove duplicates
        place_types = list(set(place_types))
    
    # If no specific types found, use general categories
    if not place_types:
        place_types = ['tourist_attraction', 'restaurant', 'museum']
    
    all_places = []
    
    # Search for each place type
    for place_type in place_types[:5]:  # Limit to 5 types to avoid too many API calls
        try:
            places = places_service.search_places(
                location=location,
                place_type=place_type,
                radius=50000  # 50km radius
            )
            all_places.extend(places)
        except Exception as e:
            print(f"Error searching for {place_type} in {location}: {e}")
            continue
    
    # Remove duplicates based on name and location
    unique_places = []
    seen_names = set()
    
    for place in all_places:
        place_key = f"{place['name']}_{place.get('address', '')}"
        if place_key not in seen_names:
            seen_names.add(place_key)
            unique_places.append(place)
    
    # Sort by rating (highest first) - SAFELY
    def get_rating(place):
        rating = place.get('rating')
        # Return a default rating if None to avoid comparison errors
        return rating if rating is not None else 0
    
    unique_places.sort(key=get_rating, reverse=True)
    
    # Return top 20 places
    return unique_places[:20]

def get_place_recommendations(location: str, interests: List[str], max_places: int = 15) -> List[Dict[str, Any]]:
    """
    Get curated place recommendations based on location and interests
    """
    
    # Search for places
    places = search_places(location, interests)
    
    # Filter by interests
    filtered_places = filter_places_by_interest(places, interests)
    
    # If we don't have enough places, add some general attractions
    if len(filtered_places) < max_places:
        general_places = search_places(location, ['general'])
        for place in general_places:
            if place not in filtered_places and len(filtered_places) < max_places:
                filtered_places.append(place)
    
    return filtered_places[:max_places]

def filter_places_by_interest(places: List[Dict[str, Any]], interests: List[str]) -> List[Dict[str, Any]]:
    """
    Filter places based on user interests
    """
    
    interest_keywords = {
        'food': ['restaurant', 'cafe', 'food', 'cuisine', 'dining'],
        'nature': ['park', 'garden', 'nature', 'outdoor', 'hiking'],
        'history': ['museum', 'historical', 'ancient', 'heritage', 'monument'],
        'art': ['gallery', 'art', 'exhibition', 'cultural'],
        'technology': ['tech', 'science', 'innovation', 'modern'],
        'adventure': ['adventure', 'sports', 'activity', 'thrill'],
        'relaxation': ['spa', 'peaceful', 'quiet', 'relaxing'],
        'nightlife': ['bar', 'club', 'nightlife', 'entertainment'],
        'shopping': ['shop', 'market', 'mall', 'boutique']
    }
    
    filtered_places = []
    
    for place in places:
        place_text = f"{place['name']} {place.get('description', '')} {place.get('type', '')}".lower()
        
        # Check if place matches any of the user's interests
        matches_interest = False
        for interest in interests:
            if interest in interest_keywords:
                keywords = interest_keywords[interest]
                if any(keyword in place_text for keyword in keywords):
                    matches_interest = True
                    break
        
        if matches_interest or not interests:  # Include if matches interest or no specific interests
            filtered_places.append(place)
    
    return filtered_places




#     """import googlemaps

# class GooglePlacesService:
#     def __init__(self):
#         self.api_key = os.getenv("GOOGLE_PLACES_API_KEY")
#         self.use_mock_data = not self.api_key
#         if self.api_key:
#             self.client = googlemaps.Client(key=self.api_key)

#     def search_places(self, location: str, place_type: str, radius: int = 50000):
#         if self.use_mock_data:
#             print("Using mock data")
#             return self._get_mock_places(location, place_type)

#         print(f"Searching Google Places for {place_type} near {location}")
#         geocode_result = self.client.geocode(location)
#         if not geocode_result:
#             raise ValueError(f"Could not geocode location: {location}")
        
#         latlng = geocode_result[0]['geometry']['location']
        
#         results = self.client.places_nearby(
#             location=latlng,
#             radius=radius,
#             type=place_type
#         )
        
#         places = []
#         for place in results.get("results", []):
#             places.append({
#                 'name': place.get('name'),
#                 'type': place_type,
#                 'rating': place.get('rating'),
#                 'address': place.get('vicinity'),
#                 'coordinates': place.get('geometry', {}).get('location'),
#                 'description': place.get('name'),  # Optional: use name or fetch Place Details for more
#                 'place_id': place.get('place_id')
#             })
        
#         return places"""