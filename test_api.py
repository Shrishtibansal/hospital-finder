import requests

response = requests.get("https://api.agify.io", params={"name": "shrishti"})
data = response.json()
print(data)