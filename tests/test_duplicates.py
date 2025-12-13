import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_step(msg):
    print(f"\n--- {msg} ---")

def test_duplicates():
    # Unique suffix
    suffix = int(time.time())
    email = f"dup_test_{suffix}@example.com"
    phone = f"010-9999-{suffix % 10000:04d}"
    
    # 1. Create Initial User
    print_step("1. Create Initial User")
    payload = {
        "email": email,
        "password": "password123",
        "name": "Original User",
        "phone_number": phone,
        "birth_date": "2000-01-01T00:00:00",
        "gender": "MALE"
    }
    response = requests.post(f"{BASE_URL}/users/", json=payload)
    if response.status_code != 200:
        print(f"FAILED: Could not create initial user. {response.status_code} {response.text}")
        return
    print("SUCCESS: Initial user created.")

    # 2. Test Duplicate Email
    print_step("2. Test Duplicate Email")
    dup_email_payload = payload.copy()
    dup_email_payload["phone_number"] = f"010-8888-{suffix % 10000:04d}" # Different phone
    dup_email_payload["name"] = "Duplicate Email User"
    
    response = requests.post(f"{BASE_URL}/users/", json=dup_email_payload)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}")
    
    if response.status_code == 409 and response.json()["code"] == "DUPLICATE_RESOURCE":
        print("SUCCESS: Duplicate Email returned 409 DUPLICATE_RESOURCE")
    else:
        print("FAILED: Duplicate Email check failed.")

    # 3. Test Duplicate Phone
    print_step("3. Test Duplicate Phone")
    dup_phone_payload = payload.copy()
    dup_phone_payload["email"] = f"unique_{suffix}@example.com" # Different email
    dup_phone_payload["name"] = "Duplicate Phone User"
    
    response = requests.post(f"{BASE_URL}/users/", json=dup_phone_payload)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}")
    
    if response.status_code == 409 and response.json()["code"] == "DUPLICATE_RESOURCE":
        print("SUCCESS: Duplicate Phone returned 409 DUPLICATE_RESOURCE")
    else:
        print("FAILED: Duplicate Phone check failed.")

if __name__ == "__main__":
    test_duplicates()
