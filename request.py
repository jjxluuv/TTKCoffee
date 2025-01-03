import requests

url = "http://127.0.0.1:8000/coffeerep/add"
data = {
    "name": "Mocha",
    "ingredients": "espresso,milk,chocolate",
    "preparation": "Mix ingredients and serve hot",
    "serving_size": "250ml"
}

response = requests.post(url, data=data)
print(response.json())