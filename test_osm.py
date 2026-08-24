import requests

url = "https://nominatim.openstreetmap.org/search"
params = {
    "q": "hospital in Jaipur",
    "format": "json",
    "limit": 5
}
headers = {
    "User-Agent": "hospital-finder-app"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
print(data)