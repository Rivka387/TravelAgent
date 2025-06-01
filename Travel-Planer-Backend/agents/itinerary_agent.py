"""
Itinerary Agent - Generates detailed day-by-day travel itineraries using GPT
"""

import openai
from typing import List, Dict, Any
import json
import math
import os

def generate_itinerary(destination: str, duration: int, places: List[Dict[str, Any]], 
                      interests: List[str], travel_style: str = "moderate") -> str:
    """
    Generate a detailed day-by-day itinerary using GPT
    """
    
    print(f"Generating itinerary for {destination}, {duration} days, {len(places)} places")
    
    # Validate inputs to prevent errors
    if not destination or destination == "Unknown":
        destination = "your destination"
    
    if not isinstance(duration, int) or duration <= 0:
        duration = 7  # Default to 7 days
    
    if not places:
        places = []
    
    if not interests:
        interests = ["general"]
    
    # Try GPT generation first
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _gpt_generate_itinerary(destination, duration, places, interests, travel_style)
        except Exception as e:
            print(f"GPT itinerary generation failed: {e}, falling back to basic generation")
            return _generate_basic_itinerary(destination, duration, places, interests, travel_style)
    else:
        print("No OpenAI API key found, using basic itinerary generation")
        return _generate_basic_itinerary(destination, duration, places, interests, travel_style)

def _gpt_generate_itinerary(destination: str, duration: int, places: List[Dict[str, Any]], 
                           interests: List[str], travel_style: str) -> str:
    """
    Use GPT to generate a sophisticated, personalized itinerary
    """
    
    # Prepare places information for GPT
    places_info = []
    for i, place in enumerate(places[:20], 1):  # Limit to top 20 places
        place_info = f"{i}. **{place['name']}**"
        if place.get('type'):
            place_info += f" ({place['type'].replace('_', ' ').title()})"
        
        # Safely get rating
        rating = place.get('rating')
        if rating is not None:
            place_info += f" - Rating: {rating}/5 ⭐"
        
        if place.get('description'):
            place_info += f"\n   Description: {place['description']}"
        if place.get('address'):
            place_info += f"\n   Location: {place['address']}"
        places_info.append(place_info)
    
    places_text = "\n\n".join(places_info) if places_info else "No specific places provided - please suggest popular attractions."
    
    # Create comprehensive system prompt
    system_prompt = f"""
    You are an expert travel planner with deep knowledge of destinations worldwide. Create a detailed, engaging, and practical {duration}-day itinerary for {destination}.

    **User Profile:**
    - Destination: {destination}
    - Duration: {duration} days
    - Interests: {', '.join(interests)}
    - Travel Style: {travel_style}

    **Travel Style Guidelines:**
    - **Budget**: Focus on free/cheap activities, local transport, street food, hostels
    - **Moderate**: Mix of paid attractions and free activities, mid-range dining
    - **Luxury**: High-end experiences, fine dining, premium accommodations
    - **Relaxed**: 2-3 activities per day, longer breaks, leisurely pace
    - **Packed**: 4-6 activities per day, efficient scheduling, maximize experiences
    - **Adventure**: Outdoor activities, unique experiences, off-the-beaten-path

    **Available Places and Attractions:**
    {places_text}

    **Instructions:**
    1. Create a day-by-day plan with specific times
    2. Include morning, afternoon, and evening activities
    3. Suggest specific restaurants/cafes for meals
    4. Add transportation tips between locations
    5. Include cultural insights and local tips
    6. Consider opening hours and travel distances
    7. Add budget estimates where relevant
    8. Include backup plans for bad weather
    9. Suggest what to wear/bring each day
    10. Add local customs and etiquette tips

    **Format Requirements:**
    - Use markdown formatting with headers and bullet points
    - Include emojis to make it engaging
    - Add practical tips and insider knowledge
    - Structure: Day X → Morning → Lunch → Afternoon → Evening
    - End with general tips and recommendations

    Make it personal, engaging, and actionable. Include specific details that show local expertise.
    """
    
    user_prompt = f"""
    Create a comprehensive {duration}-day itinerary for {destination} that focuses on {', '.join(interests)}.
    
    Travel style: {travel_style}
    
    Make it detailed, practical, and exciting. Include specific recommendations, timing, and local insights.
    """
    
    try:
        # Using the new OpenAI API format
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as in the main.py
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        itinerary = response.choices[0].message.content
        
        # Add some post-processing to ensure quality
        if len(itinerary) < 500:
            print("GPT response too short, enhancing...")
            itinerary = _enhance_short_itinerary(itinerary, destination, duration, places, interests)
        
        print(f"GPT generated itinerary: {len(itinerary)} characters")
        return itinerary
        
    except Exception as e:
        print(f"Error generating itinerary with GPT: {e}")
        raise e

def _enhance_short_itinerary(short_itinerary: str, destination: str, duration: int, 
                           places: List[Dict[str, Any]], interests: List[str]) -> str:
    """
    Enhance a short GPT response with additional details
    """
    
    enhanced = f"# {duration}-Day Itinerary for {destination} 🌍\n\n"
    enhanced += f"**Interests:** {', '.join(interests)} | **Style:** Comprehensive\n\n"
    enhanced += short_itinerary
    enhanced += "\n\n---\n\n"
    enhanced += _generate_additional_tips(destination, interests)
    
    return enhanced

def _generate_additional_tips(destination: str, interests: List[str]) -> str:
    """
    Generate additional tips based on destination and interests
    """
    
    tips = f"## 💡 Additional Tips for {destination}\n\n"
    
    # General tips
    tips += "### 🎯 General Travel Tips\n"
    tips += "- Download offline maps before you go\n"
    tips += "- Learn basic local phrases\n"
    tips += "- Keep digital and physical copies of important documents\n"
    tips += "- Research local customs and etiquette\n"
    tips += "- Check visa requirements and vaccination needs\n\n"
    
    # Interest-specific tips
    if interests:
        tips += "### 🎨 Based on Your Interests\n"
        for interest in interests:
            if interest == 'food':
                tips += "- **Food:** Try street food, visit local markets, book food tours\n"
            elif interest == 'history':
                tips += "- **History:** Consider guided tours, audio guides, museum passes\n"
            elif interest == 'nature':
                tips += "- **Nature:** Bring appropriate gear, check weather, book eco-tours\n"
            elif interest == 'art':
                tips += "- **Art:** Check museum schedules, book special exhibitions in advance\n"
            elif interest == 'adventure':
                tips += "- **Adventure:** Book activities in advance, check safety requirements\n"
            elif interest == 'relaxation':
                tips += "- **Relaxation:** Book spa treatments early, find quiet spots\n"
    
    tips += "\n### 📱 Useful Apps\n"
    tips += "- Google Translate for language help\n"
    tips += "- Google Maps for navigation\n"
    tips += "- Local transport apps\n"
    tips += "- Currency converter\n"
    tips += "- Weather forecast app\n"
    
    return tips

def _generate_basic_itinerary(destination: str, duration: int, places: List[Dict[str, Any]], 
                             interests: List[str], travel_style: str) -> str:
    """
    Fallback method to generate a basic itinerary without GPT
    """
    
    if not places:
        return f"""# {duration}-Day Itinerary for {destination} 🌍

**Travel Style:** {travel_style.title()}
**Interests:** {', '.join(interests)}

Unfortunately, I couldn't find specific places for your destination. Here's a general framework:

## Day 1 🚀
**Morning (9:00 AM - 12:00 PM)**
- Arrive and check into accommodation
- Get oriented with the city center

**Lunch (12:00 PM - 1:30 PM)**
- Try local cuisine at a nearby restaurant

**Afternoon (1:30 PM - 5:00 PM)**
- Explore main attractions and landmarks
- Visit tourist information center

**Evening (5:00 PM onwards)**
- Dinner at a recommended local restaurant
- Evening stroll through the city

## Day 2 🏛️
**Morning:** Visit major cultural sites or museums
**Afternoon:** Explore local markets or shopping areas  
**Evening:** Experience local nightlife or entertainment

Continue this pattern for the remaining days, focusing on your interests: {', '.join(interests)}.

## 💡 General Tips
- Research local customs and etiquette
- Book popular attractions in advance
- Try local transportation options
- Learn basic phrases in the local language
- Keep important documents safe
"""
    
    # Determine activities per day based on travel style
    activities_per_day = {
        'relaxed': 2,
        'moderate': 3,
        'packed': 4,
        'luxury': 2,
        'budget': 3,
        'adventure': 4
    }.get(travel_style, 3)
    
    # Group places by type
    categorized_places = {
        'attractions': [],
        'restaurants': [],
        'nature': [],
        'culture': [],
        'general': []
    }
    
    for place in places:
        place_type = place.get('type', '').lower()
        place_name = place.get('name', '').lower()
        
        if 'restaurant' in place_type or 'cafe' in place_type or 'food' in place_name:
            categorized_places['restaurants'].append(place)
        elif 'park' in place_type or 'nature' in place_type or 'garden' in place_name:
            categorized_places['nature'].append(place)
        elif 'museum' in place_type or 'gallery' in place_type or 'church' in place_type:
            categorized_places['culture'].append(place)
        elif 'tourist_attraction' in place_type:
            categorized_places['attractions'].append(place)
        else:
            categorized_places['general'].append(place)
    
    # Start building the itinerary
    itinerary = f"# {duration}-Day Itinerary for {destination} 🌍\n\n"
    itinerary += f"**Travel Style:** {travel_style.title()} | **Interests:** {', '.join(interests)}\n"
    itinerary += f"**Total Places to Visit:** {len(places)} 📍\n\n"
    
    # Combine all attraction places
    all_attractions = (categorized_places['attractions'] + 
                      categorized_places['culture'] + 
                      categorized_places['nature'] +
                      categorized_places['general'])
    
    # Distribute places across days
    places_per_day = max(1, len(all_attractions) // max(1, duration))
    
    day_emojis = ['🚀', '🏛️', '🎨', '🌟', '🎯', '🌈', '✨']
    
    for day in range(1, duration + 1):
        emoji = day_emojis[(day-1) % len(day_emojis)]
        itinerary += f"## Day {day} {emoji}\n\n"
        
        # Get places for this day
        start_idx = (day - 1) * places_per_day
        end_idx = min(start_idx + activities_per_day, len(all_attractions))
        day_places = all_attractions[start_idx:end_idx] if start_idx < len(all_attractions) else []
        
        # Morning activity
        itinerary += "### 🌅 Morning (9:00 AM - 12:00 PM)\n"
        if day_places:
            place = day_places[0]
            itinerary += f"**Visit {place['name']}**"
            
            # Safely get rating
            rating = place.get('rating')
            if rating is not None:
                itinerary += f" ⭐ {rating}/5\n"
            else:
                itinerary += "\n"
                
            if place.get('description'):
                itinerary += f"- {place['description']}\n"
            itinerary += f"- Type: {place.get('type', 'Attraction').replace('_', ' ').title()}\n"
            if place.get('address'):
                itinerary += f"- Location: {place['address']}\n"
        else:
            itinerary += "- Free time for exploration 🚶‍♂️\n"
        
        # Lunch
        itinerary += "\n### 🍽️ Lunch (12:00 PM - 1:30 PM)\n"
        if categorized_places['restaurants']:
            restaurant_idx = (day - 1) % len(categorized_places['restaurants'])
            restaurant = categorized_places['restaurants'][restaurant_idx]
            itinerary += f"**{restaurant['name']}**"
            
            # Safely get rating
            rating = restaurant.get('rating')
            if rating is not None:
                itinerary += f" ⭐ {rating}/5\n"
            else:
                itinerary += "\n"
                
            if restaurant.get('description'):
                itinerary += f"- {restaurant['description']}\n"
        else:
            itinerary += "- Local restaurant (explore the area for dining options) 🔍\n"
        
        # Afternoon activity
        itinerary += "\n### ☀️ Afternoon (1:30 PM - 5:00 PM)\n"
        if len(day_places) > 1:
            place = day_places[1]
            itinerary += f"**Explore {place['name']}**"
            
            # Safely get rating
            rating = place.get('rating')
            if rating is not None:
                itinerary += f" ⭐ {rating}/5\n"
            else:
                itinerary += "\n"
                
            if place.get('description'):
                itinerary += f"- {place['description']}\n"
        elif day_places:
            itinerary += f"- Continue exploring the {day_places[0]['name']} area 🗺️\n"
            itinerary += "- Walk around the neighborhood and discover hidden gems\n"
        else:
            itinerary += "- Free time for shopping or relaxation 🛍️\n"
        
        # Evening
        itinerary += "\n### 🌆 Evening (5:00 PM onwards)\n"
        if len(day_places) > 2:
            place = day_places[2]
            itinerary += f"**Visit {place['name']}**"
            
            # Safely get rating
            rating = place.get('rating')
            if rating is not None:
                itinerary += f" ⭐ {rating}/5\n"
            else:
                itinerary += "\n"
                
            if place.get('description'):
                itinerary += f"- {place['description']}\n"
        else:
            itinerary += "- Dinner at a local restaurant 🍽️\n"
            itinerary += "- Evening stroll or local entertainment 🎭\n"
        
        # Add day-specific tips
        itinerary += "\n**💡 Day Tips:**\n"
        if day == 1:
            itinerary += "- Arrive early to make the most of your first day\n"
            itinerary += "- Get a local SIM card or check WiFi options 📱\n"
        elif day == duration:
            itinerary += "- Pack and prepare for departure ✈️\n"
            itinerary += "- Buy souvenirs and last-minute shopping 🎁\n"
        else:
            itinerary += "- Wear comfortable walking shoes 👟\n"
            itinerary += "- Carry water and snacks 💧\n"
        
        itinerary += "\n" + "-" * 50 + "\n\n"
    
    # Add comprehensive tips section
    itinerary += _generate_additional_tips(destination, interests)
    
    itinerary += "\n**Have an amazing trip! 🌟✈️**"
    
    return itinerary