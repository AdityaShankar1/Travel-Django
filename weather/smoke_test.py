import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django (if needed for standalone scripts depending on services)
import django
django.setup()

from weather.services import get_weather_data

def test_weather():
    print("Testing Weather Service...")
    data = get_weather_data()
    for entry in data:
        if entry.get('error'):
            print(f"FAILED: {entry['city']}")
        else:
            print(f"SUCCESS: {entry['city']} - {entry['temp']}°C, {entry['condition']}")

if __name__ == "__main__":
    test_weather()
