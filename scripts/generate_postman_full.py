import json
from app.core.config import settings

def generate_postman_collection():
    collection = {
        "info": {
            "name": "Bookstore API (Full)",
            "description": "Complete API collection optimized for sequential testing (Runner). Create uses distinct data, Delete targets created items.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "variable": [
            {
                "key": "base_url",
                "value": "http://localhost:8000",
                "type": "string"
            },
            {
                "key": "access_token",
                "value": "",
                "type": "string"
            }
        ]
    }

    # Helper to create request item
    def create_item(name, method, url, body=None, auth=True, event=None):
        if not url.startswith("/api/v1"):
            url = "/api/v1" + url
            
        item = {
            "name": name,
            "request": {
                "method": method,
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "url": {
                    "raw": "{{base_url}}" + url,
                    "host": ["{{base_url}}"],
                    "path": url.strip("/").split("/")
                },
                "body": {}
            }
        }
        
        if body:
            item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(body, indent=2)
            }
            
        if auth:
            item["request"]["auth"] = {
                "type": "bearer",
                "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}]
            }
            
        if event:
            item["event"] = event
            
        return item

    # 1. Auth Folder
    auth_folder = {"name": "1. Auth", "item": []}
    
    # Login (Admin) - The ONLY Login
    login_admin = create_item("Login (Admin)", "POST", "/auth/login", auth=False)
    login_admin["request"]["body"] = {
        "mode": "urlencoded",
        "urlencoded": [
            {"key": "username", "value": "admin@example.com", "type": "text"},
            {"key": "password", "value": "admin123", "type": "text"}
        ]
    }
    login_admin["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "pm.collectionVariables.set('access_token', jsonData.access_token);",
                "console.log('Token saved:', jsonData.access_token);"
            ],
            "type": "text/javascript"
        }
    }]
    auth_folder["item"].append(login_admin)
    
    auth_folder["item"].append(create_item("Refresh Token", "POST", "/auth/refresh"))
    auth_folder["item"].append(create_item("Get Me", "GET", "/auth/me"))
    
    collection["item"].append(auth_folder)

    # 2. Users Folder
    users_folder = {"name": "2. Users", "item": []}
    
    users_folder["item"].append(create_item("List Users (Admin)", "GET", "/users/?page=0&size=10"))
    
    # Create User (Test Endpoint Only)
    create_user = create_item("Create User", "POST", "/users/", body={
        "email": "demo_{{$timestamp}}@example.com",
        "name": "Demo User",
        "password": "password123",
        "phone_number": "010-{{$randomInt}}{{$randomInt}}-{{$randomInt}}{{$randomInt}}",
        "gender": "FEMALE",
        "birth_date": "1995-05-05T00:00:00",
        "address": "Busan, Korea",
        "role": "USER"
    })
    create_user["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "if(jsonData.user_id) {",
                "    pm.collectionVariables.set('created_user_id', jsonData.user_id);",
                "    pm.collectionVariables.set('created_user_email', jsonData.email);",
                "    console.log('Created User ID:', jsonData.user_id);",
                "}"
            ],
            "type": "text/javascript"
        }
    }]
    users_folder["item"].append(create_user)
    
    # Login as Created User to get token
    login_user = create_item("Login (Created User)", "POST", "/auth/login", auth=False)
    login_user["request"]["body"] = {
        "mode": "urlencoded",
        "urlencoded": [
            {"key": "username", "value": "{{created_user_email}}", "type": "text"},
            {"key": "password", "value": "password123", "type": "text"}
        ]
    }
    login_user["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "pm.collectionVariables.set('user_token', jsonData.access_token);",
                "console.log('User Token saved');"
            ],
            "type": "text/javascript"
        }
    }]
    users_folder["item"].append(login_user)
    
    users_folder["item"].append(create_item("Get My Info", "GET", "/users/me"))
    
    update_me = create_item("Update My Info", "PUT", "/users/me", body={
        "name": "Updated Name {{$timestamp}}",
        "phone_number": "010-9876-5432",
        "address": "Busan, Korea"
    })
    users_folder["item"].append(update_me)
    
    patch_me = create_item("Patch My Info", "PATCH", "/users/me", body={
        "address": "Busan, Korea"
    })
    users_folder["item"].append(patch_me)
    
    users_folder["item"].append(create_item("Get User By ID (Admin)", "GET", "/users/1"))
    users_folder["item"].append(create_item("Logout", "POST", "/users/logout"))
    
    # Soft Delete Me (Using User Token)
    soft_delete_me = create_item("Soft Delete Me (User)", "DELETE", "/users/me/soft")
    soft_delete_me["request"]["auth"] = {
        "type": "bearer",
        "bearer": [{"key": "token", "value": "{{user_token}}", "type": "string"}]
    }
    users_folder["item"].append(soft_delete_me)
    
    # Hard Delete (Admin) - Cleans up the soft-deleted user
    hard_delete = create_item("Hard Delete User (Admin)", "DELETE", "/users/{{created_user_id}}/hard")
    users_folder["item"].append(hard_delete)
    
    collection["item"].append(users_folder)

    # 3. Books Folder
    books_folder = {"name": "3. Books", "item": []}
    books_folder["item"].append(create_item("List Books", "GET", "/books/?page=0&size=10", auth=False))
    books_folder["item"].append(create_item("Get Book Detail", "GET", "/books/1", auth=False))
    
    # Create Book (Distinct & Dynamic)
    create_book = create_item("Create Book (Admin)", "POST", "/books/", body={
        "title": "1984 Edition {{$timestamp}}",
        "authors": "[\"George Orwell\"]",
        "categories": "[\"Fiction\", \"Dystopian\"]",
        "publisher": "Secker & Warburg",
        "summary": "A dystopian social science fiction novel.",
        "isbn": "978-{{$timestamp}}",
        "price": 12000,
        "stock": 50,
        "cover_image": "http://example.com/1984.jpg",
        "publication_date": "1949-06-08T00:00:00",
        "subcategory": "Science Fiction"
    })
    # Use Access Token (Admin)
    create_book["request"]["auth"]["bearer"][0]["value"] = "{{access_token}}"
    
    # Capture Book ID
    create_book["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "if(jsonData.book_id) {",
                "    pm.collectionVariables.set('created_book_id', jsonData.book_id);",
                "    console.log('Created Book ID:', jsonData.book_id);",
                "}"
            ],
            "type": "text/javascript"
        }
    }]
    books_folder["item"].append(create_book)
    
    # Update Created Book
    update_book = create_item("Update Book (Admin)", "PUT", "/books/{{created_book_id}}", body={
        "price": 12000,
        "stock": 90,
        "discount_rate": 10
    })
    update_book["request"]["auth"]["bearer"][0]["value"] = "{{access_token}}"
    books_folder["item"].append(update_book)
    
    # Delete Created Book
    delete_book = create_item("Delete Book (Admin)", "DELETE", "/books/{{created_book_id}}")
    delete_book["request"]["auth"]["bearer"][0]["value"] = "{{access_token}}"
    books_folder["item"].append(delete_book)
    
    collection["item"].append(books_folder)

    # 4. Orders Folder
    orders_folder = {"name": "4. Orders", "item": []}
    
    create_order = create_item("Create Order", "POST", "/orders/", body={
        "payment_method": "CARD",
        "receiver_name": "John Doe",
        "receiver_phone": "010-1234-5678",
        "shipping_address": "Seoul, Korea",
        "items": [
            {
                "book_id": 1,
                "quantity": 1,
                "unit_price": 15000,
                "subtotal": 15000
            }
        ]
    })
    # Capture Order ID
    create_order["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "if(jsonData.order_id) {",
                "    pm.collectionVariables.set('created_order_id', jsonData.order_id);",
                "    console.log('Created Order ID:', jsonData.order_id);",
                "}"
            ],
            "type": "text/javascript"
        }
    }]
    orders_folder["item"].append(create_order)
    
    orders_folder["item"].append(create_item("List My Orders", "GET", "/orders/"))
    
    # Cancel Created Order
    orders_folder["item"].append(create_item("Cancel Order", "PATCH", "/orders/{{created_order_id}}/cancel"))
    
    collection["item"].append(orders_folder)

    # 5. Carts Folder
    carts_folder = {"name": "5. Carts", "item": []}
    
    carts_folder["item"].append(create_item("Get My Cart", "GET", "/carts/"))
    
    add_cart = create_item("Add Item", "POST", "/carts/items", body={
        "book_id": 1,
        "quantity": 1
    })
    # Capture Cart Item ID
    add_cart["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "if(jsonData.cart_item_id) {",
                "    pm.collectionVariables.set('created_cart_item_id', jsonData.cart_item_id);",
                "    console.log('Created Cart Item ID:', jsonData.cart_item_id);",
                "}"
            ],
            "type": "text/javascript"
        }
    }]
    carts_folder["item"].append(add_cart)
    
    update_cart = create_item("Update Item Quantity", "PUT", "/carts/items", body={
        "book_id": 1,
        "quantity": 2
    })
    carts_folder["item"].append(update_cart)
    
    carts_folder["item"].append(create_item("Get Cart Items", "GET", "/carts/items"))
    
    # Delete Created Item (Uses Book ID, not Cart Item ID)
    carts_folder["item"].append(create_item("Delete Item", "DELETE", "/carts/items/1"))
    
    carts_folder["item"].append(create_item("Clear Cart", "DELETE", "/carts/"))
    
    collection["item"].append(carts_folder)

    # 6. Reviews Folder
    review_folder = {"name": "6. Reviews", "item": []}
    
    # Create Review (Target Dynamic Book)
    create_review = create_item("Write Review", "POST", "/reviews/{{created_book_id}}", body={
        "rating": 5,
        "content": "This book was amazing! Highly recommended."
    })
    # Capture Review ID
    create_review["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "if(jsonData.review_id) {",
                "    pm.collectionVariables.set('created_review_id', jsonData.review_id);",
                "    console.log('Created Review ID:', jsonData.review_id);",
                "}"
            ],
            "type": "text/javascript"
        }
    }]
    review_folder["item"].append(create_review)
    
    review_folder["item"].append(create_item("Get Book Reviews", "GET", "/reviews/{{created_book_id}}", auth=False))
    
    # Update Created Review
    update_review = create_item("Update Review", "PATCH", "/reviews/{{created_review_id}}", body={
        "rating": 4,
        "content": "Updated review content."
    })
    review_folder["item"].append(update_review)
    
    # Get Created Review Detail
    review_folder["item"].append(create_item("Get Review Detail", "GET", "/reviews/{{created_review_id}}/detail", auth=False))
    
    # Delete Created Review
    review_folder["item"].append(create_item("Delete Review", "DELETE", "/reviews/{{created_review_id}}"))
    
    collection["item"].append(review_folder)

    # 7. Favorites Folder
    fav_folder = {"name": "7. Favorites", "item": []}
    
    add_fav = create_item("Add Favorite", "POST", "/favorites/", body={
        "book_id": 1
    })
    # Capture Favorite ID (Optional, but endpoint returns it)
    add_fav["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "if(jsonData.favorite_id) {",
                "    pm.collectionVariables.set('created_fav_id', jsonData.favorite_id);",
                "    console.log('Created Fav ID:', jsonData.favorite_id);",
                "}"
            ],
            "type": "text/javascript"
        }
    }]
    fav_folder["item"].append(add_fav)
    
    fav_folder["item"].append(create_item("List Favorites", "GET", "/favorites/"))
    
    # Remove Created Favorite (Uses Book ID)
    fav_folder["item"].append(create_item("Remove Favorite", "DELETE", "/favorites/1"))
    
    collection["item"].append(fav_folder)

    # 8. Error Tests Folder
    error_folder = {"name": "8. Error Tests", "item": []}
    
    # 1. 400 Bad Request (Login with Invalid Credentials)
    error_400 = create_item("1. 400 Bad Request (Login)", "POST", "/auth/login", auth=False)
    error_400["request"]["body"] = {
        "mode": "urlencoded",
        "urlencoded": [
            {"key": "username", "value": "invalid_{{$timestamp}}@example.com", "type": "text"},
            {"key": "password", "value": "wrongpass", "type": "text"}
        ]
    }
    error_folder["item"].append(error_400)
    
    # 2. 401 Unauthorized (Get Me without Token)
    error_401 = create_item("2. 401 Unauthorized (Get Me)", "GET", "/users/me", auth=False)
    error_folder["item"].append(error_401)
    
    # 3. 403 Forbidden (User Create Book)
    # We need a USER token for this, not Admin.
    login_user_for_error = create_item("Setup: Login as User for 403 Test", "POST", "/auth/login", auth=False)
    login_user_for_error["request"]["body"] = {
        "mode": "urlencoded",
        "urlencoded": [
            {"key": "username", "value": "demo_{{$timestamp}}@example.com", "type": "text"}, # Use dynamic email? No, use created_user_email if possible, or just create a temp user.
            # Actually, we can use the 'created_user_email' we didn't save? 
            # We removed 'created_user_email' saving. Let's use a hardcoded customer if available, or just fail if not.
            # Better: Create a temp user for this test.
            {"key": "username", "value": "customer@example.com", "type": "text"}, # Assuming customer exists from seed? No, we removed seed customer login.
            # Let's use the 'created_user_id' to find the user? No.
            # Let's just use a hardcoded 'customer@example.com' which SHOULD exist if we ran seed. 
            # Wait, did we create customer in seed? Yes, usually.
            {"key": "password", "value": "customer123", "type": "text"}
        ]
    }
    
    create_temp_user = create_item("Setup: Create Temp User", "POST", "/users/", auth=False, body={
        "email": "error_test_{{$timestamp}}@example.com",
        "name": "Error Tester",
        "password": "password123",
        "phone_number": "010-{{$randomInt}}{{$randomInt}}-{{$randomInt}}{{$randomInt}}",
        "gender": "MALE",
        "birth_date": "2000-01-01T00:00:00",
        "role": "USER"
    })
    create_temp_user["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "pm.collectionVariables.set('temp_user_email', jsonData.email);"
            ],
            "type": "text/javascript"
        }
    }]
    error_folder["item"].append(create_temp_user)
    
    login_temp_user = create_item("3-1. Login (Temp User)", "POST", "/auth/login", auth=False)
    login_temp_user["request"]["body"] = {
        "mode": "urlencoded",
        "urlencoded": [
            {"key": "username", "value": "{{temp_user_email}}", "type": "text"},
            {"key": "password", "value": "password123", "type": "text"}
        ]
    }
    login_temp_user["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "pm.collectionVariables.set('temp_user_token', jsonData.access_token);"
            ],
            "type": "text/javascript"
        }
    }]
    error_folder["item"].append(login_temp_user)

    error_403 = create_item("3-2. 403 Forbidden (User Create Book)", "POST", "/books/", body={
        "title": "Forbidden Book",
        "authors": "[\"Me\"]",
        "isbn": "0000000000",
        "price": 1000,
        "stock": 10,
        "publication_date": "2025-01-01T00:00:00",
        "subcategory": "Test",
        "publisher": "Forbidden Publisher",
        "categories": "[\"Test\"]"
    })
    error_403["request"]["auth"] = {
        "type": "bearer",
        "bearer": [{"key": "token", "value": "{{temp_user_token}}", "type": "string"}]
    }
    error_folder["item"].append(error_403)
    
    # 4. 404 Not Found (Get Non-existent Book)
    error_404 = create_item("4. 404 Not Found (Book)", "GET", "/books/999999", auth=False)
    error_folder["item"].append(error_404)
    
    # 5. 409 Conflict (Duplicate User)
    error_409 = create_item("5. 409 Conflict (Duplicate User)", "POST", "/users/", auth=False, body={
        "email": "admin@example.com", # Existing email
        "password": "password123",
        "name": "Duplicate",
        "phone_number": "010-0000-0000",
        "birth_date": "2000-01-01T00:00:00",
        "gender": "MALE"
    })
    error_folder["item"].append(error_409)
    
    # 6. 400 Bad Request (Invalid Email Format) - Exception handler returns 400
    error_422 = create_item("6. 400 Bad Request (Invalid Email)", "POST", "/users/", auth=False, body={
        "email": "not-an-email",
        "password": "password123",
        "name": "Invalid Email",
        "phone_number": "010-1111-2222",
        "gender": "MALE",
        "birth_date": "2000-01-01T00:00:00",
        "role": "USER"
    })
    error_folder["item"].append(error_422)
    
    # 7. 404 Not Found (Delete Non-existent Book)
    error_404_del = create_item("7. 404 Not Found (Delete Book)", "DELETE", "/books/999999")
    error_404_del["request"]["auth"]["bearer"][0]["value"] = "{{access_token}}" # Admin token
    error_folder["item"].append(error_404_del)
    
    # 8. 400 Bad Request (Create Order with Empty Items)
    error_400_order = create_item("8. 400 Bad Request (Empty Order)", "POST", "/orders/", body={
        "payment_method": "CARD",
        "receiver_name": "Test",
        "receiver_phone": "010-1234-5678",
        "shipping_address": "Seoul",
        "items": []
    })
    error_folder["item"].append(error_400_order)
    
    # 9. 404 Not Found (Update Non-existent Review)
    error_404_review = create_item("9. 404 Not Found (Update Review)", "PATCH", "/reviews/999999", body={
        "content": "Updated"
    })
    error_folder["item"].append(error_404_review)
    
    # 10. 400 Bad Request (Invalid Password Length)
    error_400_pw = create_item("10. 400 Bad Request (Short Password)", "POST", "/users/", auth=False, body={
        "email": "shortpw_{{$timestamp}}@example.com",
        "password": "123", # Too short
        "name": "Short PW",
        "phone_number": "010-{{$randomInt}}-{{$randomInt}}",
        "gender": "MALE",
        "birth_date": "2000-01-01T00:00:00",
        "role": "USER"
    })
    error_folder["item"].append(error_400_pw)

    # 11. 400 Bad Request (Invalid Query Param)
    error_400_query = create_item("11. 400 Bad Request (Invalid Query Param)", "GET", "/books/?page=invalid", auth=False)
    error_folder["item"].append(error_400_query)

    # 12. 404 Not Found (User Not Found)
    error_404_user = create_item("12. 404 Not Found (User Not Found)", "GET", "/users/999999")
    error_404_user["request"]["auth"]["bearer"][0]["value"] = "{{access_token}}" # Admin token
    error_folder["item"].append(error_404_user)

    # 13. 409 Conflict (State Conflict - Cancel Cancelled Order)
    # First create an order, then cancel it twice
    create_order_conflict = create_item("13-1. Create Order (Success)", "POST", "/orders/", body={
        "payment_method": "CARD",
        "receiver_name": "Conflict Test",
        "receiver_phone": "010-1234-5678",
        "shipping_address": "Seoul",
        "items": [{"book_id": 1, "quantity": 1, "unit_price": 15000, "subtotal": 15000}]
    })
    create_order_conflict["event"] = [{
        "listen": "test",
        "script": {
            "exec": [
                "var jsonData = pm.response.json();",
                "pm.collectionVariables.set('conflict_order_id', jsonData.order_id);"
            ],
            "type": "text/javascript"
        }
    }]
    error_folder["item"].append(create_order_conflict)
    
    cancel_order_1 = create_item("13-2. Cancel Order (Success)", "PATCH", "/orders/{{conflict_order_id}}/cancel")
    error_folder["item"].append(cancel_order_1)
    
    error_409_state = create_item("13-3. 409 Conflict (State Conflict)", "PATCH", "/orders/{{conflict_order_id}}/cancel")
    error_folder["item"].append(error_409_state)

    collection["item"].append(error_folder)

    # Save to file
    with open("bookstore_api_collection_full.json", "w") as f:
        json.dump(collection, f, indent=2)
    
    print("Postman collection generated: bookstore_api_collection_full.json")

if __name__ == "__main__":
    generate_postman_collection()
