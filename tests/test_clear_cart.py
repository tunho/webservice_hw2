import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def print_step(msg):
    print(f"\n--- {msg} ---")

def get_token(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]

def test_clear_cart():
    # 1. Login
    user_token = get_token("customer@example.com", "customer123")
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # 2. Add Item to Cart
    print_step("1. Add Item to Cart")
    # Get a book first
    books = requests.get(f"{BASE_URL}/books/").json()["content"]
    book_id = books[0]["book_id"]
    
    payload = {"book_id": book_id, "quantity": 1}
    res = requests.post(f"{BASE_URL}/carts/items", headers=headers, json=payload)
    if res.status_code == 200:
        print("SUCCESS: Item added to cart.")
    else:
        print(f"FAILED: Could not add item. {res.status_code} {res.text}")
        return

    # 3. Verify Cart has items
    print_step("2. Verify Cart has items")
    res = requests.get(f"{BASE_URL}/carts/items", headers=headers)
    items = res.json()["payload"]
    print(f"Cart Items: {len(items)}")
    if len(items) > 0:
        print("SUCCESS: Cart is not empty.")
    else:
        print("FAILED: Cart is empty.")
        return

    # 4. Clear Cart
    print_step("3. Clear Cart")
    res = requests.delete(f"{BASE_URL}/carts/", headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.json()}")
    
    if res.status_code == 200:
        print("SUCCESS: Clear Cart request successful.")
    else:
        print("FAILED: Clear Cart request failed.")
        return

    # 5. Verify Cart is empty
    print_step("4. Verify Cart is empty")
    res = requests.get(f"{BASE_URL}/carts/items", headers=headers)
    items = res.json()["payload"]
    print(f"Cart Items: {len(items)}")
    if len(items) == 0:
        print("SUCCESS: Cart is empty.")
    else:
        print("FAILED: Cart is NOT empty.")

if __name__ == "__main__":
    test_clear_cart()
