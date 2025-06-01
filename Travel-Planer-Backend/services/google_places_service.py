"""
Google Places Service - Handles communication with Google Places API
"""

from dotenv import load_dotenv
import requests
import os
from typing import List, Dict, Any, Optional

class GooglePlacesService:
    """
    Service class for interacting with Google Places API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GOOGLE_PLACES_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # For demo purposes, we'll use mock data if no API key is provided
        self.use_mock_data = not self.api_key
        
        if self.use_mock_data:
            print("Warning: No Google Places API key found. Using mock data for demonstration.")
    
    def search_places(self, location: str, place_type: str, radius: int = 50000) -> List[Dict[str, Any]]:
        """
        Search for places near a location
        """
        
        if self.use_mock_data:
            return self._get_mock_places(location, place_type)
        
        try:
            # First, get coordinates for the location
            geocode_url = f"{self.base_url}/findplacefromtext/json"
            geocode_params = {
                'input': location,
                'inputtype': 'textquery',
                'fields': 'geometry',
                'key': self.api_key
            }
            
            geocode_response = requests.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()
            
            if not geocode_data.get('candidates'):
                return []
            
            # Get coordinates
            lat = geocode_data['candidates'][0]['geometry']['location']['lat']
            lng = geocode_data['candidates'][0]['geometry']['location']['lng']
            
            # Search for places nearby
            search_url = f"{self.base_url}/nearbysearch/json"
            search_params = {
                'location': f"{lat},{lng}",
                'radius': radius,
                'type': place_type,
                'key': self.api_key
            }
            
            search_response = requests.get(search_url, params=search_params)
            search_data = search_response.json()
            
            places = []
            for result in search_data.get('results', []):
                place = {
                    'name': result.get('name', ''),
                    'type': place_type,
                    'rating': result.get('rating'),
                    'address': result.get('vicinity', ''),
                    'coordinates': {
                        'lat': result['geometry']['location']['lat'],
                        'lng': result['geometry']['location']['lng']
                    },
                    'price_level': result.get('price_level'),
                    'place_id': result.get('place_id'),
                    'description': self._get_place_description(place_type)
                }
                places.append(place)
            
            return places
            
        except Exception as e:
            print(f"Error searching places: {e}")
            return self._get_mock_places(location, place_type)
    
    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific place
        """
        
        if self.use_mock_data:
            return self._get_mock_place_details(place_id)
        
        try:
            details_url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,rating,formatted_address,opening_hours,website,formatted_phone_number,reviews',
                'key': self.api_key
            }
            
            response = requests.get(details_url, params=params)
            data = response.json()
            
            if data.get('result'):
                return data['result']
            else:
                return {}
                
        except Exception as e:
            print(f"Error getting place details: {e}")
            return {}
    
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
        places_data = mock_data.get(location_key, {}).get(place_type, [])
        
        # Convert to standard format
        places = []
        for i, place_data in enumerate(places_data):
            place = {
                'name': place_data['name'],
                'type': place_type,
                'rating': place_data['rating'],
                'address': f"{location}",
                'coordinates': {'lat': 41.9028 + i*0.01, 'lng': 12.4964 + i*0.01},  # Mock coordinates
                'description': place_data['description'],
                'place_id': f"mock_{location_key}_{place_type}_{i}"
            }
            places.append(place)
        
        return places
    
    def _get_mock_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Generate mock place details
        """
        return {
            'name': 'Mock Place',
            'rating': 4.2,
            'formatted_address': 'Mock Address',
            'opening_hours': {'open_now': True},
            'website': 'https://example.com',
            'formatted_phone_number': '+1 234 567 8900'
        }
    
    def _get_place_description(self, place_type: str) -> str:
        """
        Generate generic descriptions based on place type
        """
        descriptions = {
            'restaurant': 'Local dining establishment',
            'tourist_attraction': 'Popular tourist destination',
            'museum': 'Cultural institution with exhibits',
            'park': 'Green space for recreation',
            'shopping_mall': 'Retail shopping center',
            'church': 'Religious place of worship',
            'art_gallery': 'Space for art exhibitions'
        }
        
        return descriptions.get(place_type, 'Point of interest')

# Test the service
if __name__ == "__main__":
    print("Testing Google Places Service...")
    
    service = GooglePlacesService()
    
    # Test search
    places = service.search_places("Rome, Italy", "tourist_attraction")
    print(f"\nFound {len(places)} tourist attractions in Rome:")
    
    for place in places[:3]:
        print(f"- {place['name']} (Rating: {place['rating']}) - {place['description']}")
    
    # Test different place types
    restaurants = service.search_places("Tokyo, Japan", "restaurant")
    print(f"\nFound {len(restaurants)} restaurants in Tokyo:")
    
    for restaurant in restaurants[:3]:
        print(f"- {restaurant['name']} (Rating: {restaurant['rating']}) - {restaurant['description']}")