import os
import httpx
import datetime
import re
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# --- Helper Functions ---
def parse_iso_datetime(iso_str):
    if not iso_str:
        return None
    try:
        return datetime.datetime.fromisoformat(iso_str)
    except ValueError:
        return None

def find_closest_hour_index(times, target_time_str):
    if not target_time_str or not times:
        return 0
    target_dt = parse_iso_datetime(target_time_str)
    best_idx = 0
    best_diff = float('inf')
    for i, t in enumerate(times):
        current_dt = parse_iso_datetime(t)
        diff = abs((current_dt - target_dt).total_seconds())
        if diff < best_diff:
            best_diff = diff
            best_idx = i
    return best_idx

def fetch_weather_data(city: str) -> dict:
    """Fetch raw weather data and structured info."""
    try:
        # Step 1: Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        with httpx.Client() as client:
            geo_response = client.get(geo_url)
            geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return {"error": f"Could not find coordinates for {city}."}
        
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        place_name = location["name"]
        country = location.get("country", "")
        
        # Step 2: Detailed Weather Fetch
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,windspeed_10m,weathercode",
            "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,weathercode",
            "current_weather": "true",
            "forecast_days": 4,
            "timezone": "auto"
        }
        
        with httpx.Client() as client:
            resp = client.get(weather_url, params=params)
            data = resp.json()
            
        # Process Current
        current_weather = data.get("current_weather", {})
        curr_temp = current_weather.get("temperature", "N/A")
        wind = current_weather.get("windspeed", "N/A")
        
        # Process Hourly (for humidity)
        hourly = data.get("hourly", {})
        h_hum = hourly.get("relative_humidity_2m", [])
        h_time = hourly.get("time", [])
        
        curr_time = current_weather.get("time")
        idx = find_closest_hour_index(h_time, curr_time) if curr_time else 0
        humidity = h_hum[idx] if idx < len(h_hum) else "N/A"
        
        # Forecast
        daily = data.get("daily", {})
        d_time = daily.get("time", [])
        d_max = daily.get("temperature_2m_max", [])
        d_min = daily.get("temperature_2m_min", [])
        d_code = daily.get("weathercode", [])
        
        forecast_list = []
        for i in range(min(4, len(d_time))):
            forecast_list.append({
                "date": d_time[i],
                "max_temp": d_max[i],
                "min_temp": d_min[i],
                "code": d_code[i] if i < len(d_code) else None
            })

        return {
            "location": f"{place_name}, {country}",
            "current": {
                "temp": curr_temp,
                "wind": wind,
                "humidity": humidity,
                "code": current_weather.get("weathercode")
            },
            "forecast": forecast_list
        }
        
    except Exception as e:
        return {"error": f"Error fetching weather data: {str(e)}"}

def format_weather_string(data: dict) -> str:
    if "error" in data:
        return data["error"]
    
    loc = data.get("location", "Unknown")
    curr = data.get("current", {})
    forecast = data.get("forecast", [])
    
    f_str = ""
    for day in forecast:
        f_str += f"\n- {day['date']}: Max {day['max_temp']}°C, Min {day['min_temp']}°C"
        
    return (
        f"Weather Report for {loc}:\n"
        f"Current: {curr.get('temp')}°C, Wind: {curr.get('wind')} km/h, Humidity: {curr.get('humidity')}%\n"
        f"Forecast:{f_str}"
    )

# --- Tool Definition ---
@tool
def get_weather(city: str) -> str:
    """Get the current weather and detailed forecast for a specific city."""
    data = fetch_weather_data(city)
    return format_weather_string(data)

# --- Agent & Fallback Logic ---
def get_agent_response(user_query: str) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    error_msg = "API Key missing"
    
    # 1. Try using the Agent
    if api_key:
        try:
            llm = ChatOpenAI(
                model="google/gemini-2.0-flash-exp:free", 
                openai_api_key=api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0
            )
            tools = [get_weather]
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a weather assistant. Fetch data using the tool and summarize it nicely. Use emojis!"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ])
            agent = create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
            
            result = agent_executor.invoke({"input": user_query})
            
            return {
                "type": "ai",
                "message": result["output"]
            }

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "Rate limit" in error_str:
                error_msg = "Daily AI Rate Limit Reached (Free Tier)"
            else:
                error_msg = f"AI Error: {error_str[:100]}..." # Truncate long errors
            
            print(f"AI Agent failed. Switching to fallback mode. Error: {error_msg}")
    
    # 2. Fallback
    match = re.search(r'in\s+([a-zA-Z\s]+)', user_query, re.IGNORECASE)
    
    city = "London" # Default
    if match:
        city = match.group(1).strip()
    else:
        clean_query = user_query.strip()
        if len(clean_query.split()) < 3:
            city = clean_query
            
    print(f"Fallback utilizing city: {city}")
    data = fetch_weather_data(city)
    
    return {
        "type": "fallback",
        "data": data,
        "error": error_msg,
        "city_query": city
    }
