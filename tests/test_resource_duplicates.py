import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_step(msg):
    print(f"\n--- {msg} ---")

def get_token(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]

def test_resource_duplicates():
    suffix = int(time.time())
    isbn = f"978-TEST-{suffix}"
    
    # 1. Login
    admin_token = get_token("admin@example.com", "admin123")
    user_token = get_token("customer@example.com", "customer123")
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 2. Test Duplicate Book (ISBN)
    print_step("1. Test Duplicate Book (ISBN)")
    book_payload = {
        "title": f"Dup Test Book {suffix}",
        "authors": "[\"Tester\"]",
        "categories": "[\"Test\"]",
        "publisher": "TestPub",
        "summary": "Test Summary",
        "isbn": isbn,
        "price": 1000,
        "stock": 10,
        "publication_date": "2025-01-01T00:00:00",
        "subcategory": "Test"
    }
    
    # Create first time
    res = requests.post(f"{BASE_URL}/books/", headers=admin_headers, json=book_payload)
    if res.status_code == 200:
        book_id = res.json()["book_id"]
        print(f"SUCCESS: Book created. ID: {book_id}")
    else:
        print(f"FAILED: Could not create book. {res.status_code} {res.text}")
        return

    # Create second time (Duplicate)
    res = requests.post(f"{BASE_URL}/books/", headers=admin_headers, json=book_payload)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.json()}")
    
    if res.status_code == 409 and res.json()["code"] == "DUPLICATE_RESOURCE":
        print("SUCCESS: Duplicate ISBN returned 409 DUPLICATE_RESOURCE")
    else:
        print("FAILED: Duplicate ISBN check failed.")

    # 3. Test Duplicate Review
    print_step("2. Test Duplicate Review")
    review_payload = {
        "rating": 5,
        "content": "First review"
    }
    
    # Create first review
    res = requests.post(f"{BASE_URL}/reviews/{book_id}", headers=user_headers, json=review_payload)
    if res.status_code == 200:
        print("SUCCESS: First review created.")
    else:
        print(f"FAILED: Could not create review. {res.status_code} {res.text}")
        # If already reviewed (from previous run?), try to continue
    
    # Create second review (Duplicate)
    res = requests.post(f"{BASE_URL}/reviews/{book_id}", headers=user_headers, json=review_payload)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.json()}")
    
    if res.status_code == 409 and res.json()["code"] == "DUPLICATE_RESOURCE":
        print("SUCCESS: Duplicate Review returned 409 DUPLICATE_RESOURCE")
    else:
        print("FAILED: Duplicate Review check failed.")

if __name__ == "__main__":
    test_resource_duplicates()
