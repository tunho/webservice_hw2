import urllib.request
import urllib.parse
import json
import urllib.error

BASE_URL = "http://localhost:8000/api/v1"

def test_seller_flow():
    # 1. Login as Seller
    print("1. Logging in as Seller...")
    login_data = urllib.parse.urlencode({
        "username": "seller@example.com",
        "password": "seller123"
    }).encode()
    
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=login_data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            token = data["access_token"]
            print("Login Successful!")
    except urllib.error.HTTPError as e:
        print(f"Login Failed: {e.code} {e.read().decode()}")
        return

    # 2. Create Settlement
    print("\n2. Creating Settlement...")
    settlement_data = json.dumps({
        "period_start": "2025-01-01T00:00:00",
        "period_end": "2025-01-31T23:59:59"
    }).encode()
    
    req = urllib.request.Request(f"{BASE_URL}/settlements/", data=settlement_data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("Settlement Created Successfully!")
            print(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Settlement Creation Failed: {e.code}")
        print(e.read().decode())

if __name__ == "__main__":
    test_seller_flow()
