import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def get_token(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]

def create_seed_book():
    # 1. Login as Admin
    token = get_token("admin@example.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Check if Book 1 exists
    res = requests.get(f"{BASE_URL}/books/1")
    if res.status_code == 200:
        print("Book 1 already exists.")
        return

    # 3. Create Book (Matching Swagger Example)
    payload = {
        "title": "The Great Gatsby",
        "authors": "[\"F. Scott Fitzgerald\"]",
        "categories": "[\"Fiction\", \"Classic\"]",
        "publisher": "Scribner",
        "summary": "A novel about the American dream.",
        "isbn": "978-0743273565",
        "price": 15000,
        "stock": 100,
        "cover_image": "http://example.com/gatsby.jpg",
        "publication_date": "1925-04-10T00:00:00",
        "subcategory": "Classic Literature"
    }
    res = requests.post(f"{BASE_URL}/books/", headers=headers, json=payload)
    if res.status_code == 200:
        print(f"SUCCESS: Created Book ID {res.json()['book_id']}")
    else:
        print(f"FAILED: {res.status_code} {res.text}")

if __name__ == "__main__":
    create_seed_book()
