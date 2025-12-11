import requests
import json

url = "http://localhost:8000/api/v1/users/"
payload = {
    "email": "testuser500@example.com",
    "password": "password123",
    "name": "Test User",
    "phone_number": "010-9999-8888",
    "gender": "MALE",
    "birth_date": "1990-01-01T00:00:00",
    "address": "Seoul",
    "role": "USER"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
