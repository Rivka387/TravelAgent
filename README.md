# TravelAgent
AI-powered travel planner that creates personalized trip itineraries based on user preferences.

TravelPlannerAI is an intelligent agent-based system that assists users in planning personalized trips by understanding their natural language queries and generating optimized travel itineraries. The system leverages LLM-based function calling to dynamically query structured tools like mapping services and itinerary generation logic.

## Overview

This project includes:

- A Python-based backend with integration to OpenAI's API using function calling (tool use)
- Integration with Google Maps API for geolocation, directions, and points of interest
- A React-based frontend that provides a chat interface for users to describe their travel preferences in natural language
- An orchestration layer that translates user requests into actionable function calls to retrieve and compile trip data

## Features

- Accepts free-form user input (e.g., "Plan me a 3-day trip in northern Italy with focus on history and food")
- Parses intents using OpenAI's function calling capabilities
- Queries relevant APIs to retrieve location data, attractions, and travel durations
- Dynamically constructs a structured itinerary
- Presents results in an intuitive chat interface

## Architecture

- **Backend**: Python (FastAPI), with support for:
  - OpenAI's `ChatCompletion` with function/tool calling
  - Google Maps Places API, Directions API
  - Internal task routing and caching layer
- **Frontend**: React with a simple chat interface that:
  - Captures user input
  - Displays agent responses as chat bubbles
  - Shows trip suggestions and itineraries in structured components

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key
- Google Maps API key

### Backend Installation

```bash
git clone https://github.com/your-username/TravelPlannerAI.git
cd TravelPlannerAI/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
