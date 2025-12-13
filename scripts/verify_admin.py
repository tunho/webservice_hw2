import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def print_step(msg):
    print(f"\n--- {msg} ---")

def verify_admin_flow():
    # 1. Login as Admin
    print_step("1. Admin Login")
    login_payload = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_payload)
    if response.status_code != 200:
        print(f"FAILED: Login failed. {response.status_code} {response.text}")
        return
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("SUCCESS: Admin logged in.")

    # 2. List Users (Admin Only)
    print_step("2. List Users (Admin)")
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    if response.status_code == 200:
        users = response.json()["content"]
        print(f"SUCCESS: Retrieved {len(users)} users.")
    else:
        print(f"FAILED: Could not list users. {response.status_code} {response.text}")

    # 3. Create Book (Using Swagger Example Data)
    print_step("3. Create Book (Swagger Example)")
    book_payload = {
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
    response = requests.post(f"{BASE_URL}/books/", headers=headers, json=book_payload)
    if response.status_code == 200:
        book = response.json()
        book_id = book["book_id"]
        print(f"SUCCESS: Book created. ID: {book_id}, Title: {book['title']}")
    else:
        print(f"FAILED: Could not create book. {response.status_code} {response.text}")
        return

    # 4. Update Book
    print_step("4. Update Book")
    update_payload = {
        "price": 12000,
        "stock": 90,
        "discount_rate": 10
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", headers=headers, json=update_payload)
    if response.status_code == 200:
        updated_book = response.json()
        print(f"SUCCESS: Book updated. Price: {updated_book['price']}, Stock: {updated_book['stock']}")
    else:
        print(f"FAILED: Could not update book. {response.status_code} {response.text}")

    # 5. List Orders (Admin View)
    print_step("5. List Orders (Admin)")
    response = requests.get(f"{BASE_URL}/orders/", headers=headers)
    if response.status_code == 200:
        orders = response.json()["content"]
        print(f"SUCCESS: Retrieved {len(orders)} orders.")
    else:
        print(f"FAILED: Could not list orders. {response.status_code} {response.text}")

    # 6. Delete Book
    print_step("6. Delete Book")
    response = requests.delete(f"{BASE_URL}/books/{book_id}", headers=headers)
    if response.status_code == 200:
        print("SUCCESS: Book deleted.")
    else:
        print(f"FAILED: Could not delete book. {response.status_code} {response.text}")

if __name__ == "__main__":
    verify_admin_flow()
