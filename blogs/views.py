import sqlite3
import os
from django.shortcuts import render
from django.conf import settings

DB_PATH = os.path.join(settings.BASE_DIR, 'blogs.db')

CITY_IMAGES = {
    'Kanchipuram': 'packages/kanchi.jpg',
    'Madurai': 'packages/madurai.jpg',
    'Ooty': 'packages/ooty.jpg',
    'Rameswaram': 'packages/railway-bridge-to-rameshwaram-india-34771747.jpg',
    'Tanjore': 'packages/tanjore.jpg',
    'Tuticorin': 'packages/tuticorin.jpg',
}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def blog_list(request):
    """Shows a list of unique cities as cards."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Group by city and pick representative fields
    cursor.execute('''
        SELECT city, nearest_city, best_season, MIN(id) as first_id
        FROM blogs 
        GROUP BY city
    ''')
    cities_raw = cursor.fetchall()
    conn.close()
    
    cities = []
    for row in cities_raw:
        city_data = dict(row)
        city_data['image_url'] = f"{settings.MEDIA_URL}{CITY_IMAGES.get(row['city'], 'packages/default.jpg')}"
        cities.append(city_data)
        
    return render(request, 'blogs/city_list.html', {'cities': cities})

def city_detail(request, city_name):
    """Shows all blog entries (places) for a specific city."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blogs WHERE city = ? ORDER BY id ASC', (city_name,))
    blogs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not blogs:
        # Fallback if no blogs found for this city
        return render(request, 'blogs/city_detail.html', {'city_name': city_name, 'blogs': []})
        
    # Pick metadata from the first entry
    metadata = {
        'city': city_name,
        'image_url': f"{settings.MEDIA_URL}{CITY_IMAGES.get(city_name, 'packages/default.jpg')}",
        'nearest_city': blogs[0]['nearest_city'],
        'best_season': blogs[0]['best_season']
    }
    
    return render(request, 'blogs/city_detail.html', {'metadata': metadata, 'blogs': blogs})
