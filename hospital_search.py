import requests
from math import radians, sin, cos, sqrt, atan2


def get_coordinates(place_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
        "countrycodes": "in"
    }
    headers = {
        "User-Agent": "hospital-finder-app"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        return None, None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 2)


def search_hospitals(city, user_lat, user_lon):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"hospital in {city}",
        "format": "json",
        "limit": 10,
        "countrycodes": "in",
        "extratags": 1
    }
    headers = {
        "User-Agent": "hospital-finder-app"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    hospitals = []
    for item in data:
        hospital_lat = float(item.get("lat"))
        hospital_lon = float(item.get("lon"))

        distance = calculate_distance(user_lat, user_lon, hospital_lat, hospital_lon)

        extra = item.get("extratags") or {}

        hospital = {
            "name": item.get("name", "Unknown"),
            "address": item.get("display_name", "No address"),
            "distance_km": distance,
            "emergency": extra.get("emergency", "unknown"),
            "phone": extra.get("phone", "Not available")
        }
        hospitals.append(hospital)

    hospitals.sort(key=lambda h: h["distance_km"])
    return hospitals


if __name__ == "__main__":
    city = input("Enter city name: ")
    user_location = input("Enter your area/locality (e.g. 'Malviya Nagar, Jaipur'): ")

    full_query = f"{user_location}, {city}"
    user_lat, user_lon = get_coordinates(full_query)

    if user_lat is None:
        print(f"Couldn't find '{user_location}' specifically. Using {city} city center instead.")
        user_lat, user_lon = get_coordinates(city)

    if user_lat is None:
        print("Sorry, couldn't find that city either. Try being more specific.")
    else:
        results = search_hospitals(city, user_lat, user_lon)
        for h in results:
            print(h["name"])
            print(h["address"])
            print(f"Distance: {h['distance_km']} km")
            print(f"Emergency: {h['emergency']}")
            print(f"Phone: {h['phone']}")
            print("---")