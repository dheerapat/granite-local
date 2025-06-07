def get_weather(location: str) -> dict:
    """
    Fetches the current weather for a given location (default: San Francisco).
    Args:
    location: The name of the city for which to retrieve the weather information.
    Returns:
    A dictionary containing weather information such as temperature, weather description, and humidity.
    """
    print(f"Getting current weather for {location}")
    try:
        return {"description": "clear and sunny", "temperature": 35, "humidity": "20 %"}
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {"description": "none", "temperature": "none", "humidity": "none"}
