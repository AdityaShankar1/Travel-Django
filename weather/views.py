import json
from django.shortcuts import render
from .services import get_weather_data

def weather_dashboard(request):
    """
    Renders the weather alert dashboard with real-time data and a map.
    """
    weather_data = get_weather_data()
    context = {
        'weather_data': weather_data,
        'weather_data_json': json.dumps(weather_data),
    }
    return render(request, 'weather/alerts.html', context)
