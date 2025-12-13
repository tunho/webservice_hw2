import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_step(msg):
    print(f"\n--- {msg} ---")

def get_token(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]

def test_admin_review_delete():
    suffix = int(time.time())
    
    # 1. Login
    admin_token = get_token("admin@example.com", "admin123")
    user_token = get_token("customer@example.com", "customer123")
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 2. Create a Book (Need a book to review)
    print_step("1. Create Book for Review")
    book_payload = {
        "title": f"Review Delete Test Book {suffix}",
        "authors": "[\"Tester\"]",
        "categories": "[\"Test\"]",
        "publisher": "TestPub",
        "summary": "Test Summary",
        "isbn": f"978-DEL-{suffix}",
        "price": 1000,
        "stock": 10,
        "publication_date": "2025-01-01T00:00:00",
        "subcategory": "Test"
    }
    res = requests.post(f"{BASE_URL}/books/", headers=admin_headers, json=book_payload)
    if res.status_code == 200:
        book_id = res.json()["book_id"]
        print(f"SUCCESS: Book created. ID: {book_id}")
    else:
        print(f"FAILED: Could not create book. {res.status_code} {res.text}")
        return

    # 3. User creates a Review
    print_step("2. User Creates Review")
    review_payload = {
        "rating": 5,
        "content": "To be deleted by Admin"
    }
    res = requests.post(f"{BASE_URL}/reviews/{book_id}", headers=user_headers, json=review_payload)
    if res.status_code == 200:
        review_id = res.json()["review_id"]
        print(f"SUCCESS: Review created. ID: {review_id}")
    else:
        print(f"FAILED: Could not create review. {res.status_code} {res.text}")
        return

    # 4. Admin Deletes Review
    print_step("3. Admin Deletes Review")
    res = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=admin_headers)
    print(f"Status: {res.status_code}")
    print(f"Raw Body: {res.text}")
    
    try:
        print(f"Body: {res.json()}")
    except:
        print("Could not parse JSON body")
    
    if res.status_code == 200:
        print("SUCCESS: Admin deleted review.")
    else:
        print("FAILED: Admin could not delete review.")

    # 5. Verify Deletion
    print_step("4. Verify Deletion")
    res = requests.get(f"{BASE_URL}/reviews/{review_id}/detail", headers=admin_headers)
    if res.status_code == 404:
        print("SUCCESS: Review not found (Deleted).")
    else:
        print(f"FAILED: Review still exists. Status: {res.status_code}")

if __name__ == "__main__":
    test_admin_review_delete()
