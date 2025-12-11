import json
import urllib.request

def generate_postman_collection():
    openapi_url = "http://localhost:8000/api/v1/openapi.json"
    try:
        with urllib.request.urlopen(openapi_url) as response:
            openapi_spec = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching OpenAPI spec: {e}")
        return

    collection = {
        "info": {
            "name": "Bookstore API",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    folders = {}

    for path, methods in openapi_spec["paths"].items():
        for method, details in methods.items():
            # Determine folder name from tags
            folder_name = "General"
            if "tags" in details and details["tags"]:
                folder_name = details["tags"][0].capitalize()
            
            if folder_name not in folders:
                folders[folder_name] = []

            item = {
                "name": f"{method.upper()} {path}",
                "request": {
                    "method": method.upper(),
                    "header": [],
                    "url": {
                        "raw": f"{{{{baseUrl}}}}{path}",
                        "host": ["{{baseUrl}}"],
                        "path": path.strip("/").split("/")
                    }
                }
            }
            # Add test script for login to save token
            if path == "/api/v1/auth/login" and method == "post":
                item["event"] = [{
                    "listen": "test",
                    "script": {
                        "exec": [
                            "var jsonData = pm.response.json();",
                            "pm.environment.set('access_token', jsonData.access_token);",
                            "pm.test('Status code is 200', function () {",
                            "    pm.response.to.have.status(200);",
                            "});"
                        ],
                        "type": "text/javascript"
                    }
                }]
            else:
                 # Add generic 200 OK test to all other endpoints
                 item["event"] = [{
                    "listen": "test",
                    "script": {
                        "exec": [
                            "pm.test('Status code is 200 or 201', function () {",
                            "    pm.expect(pm.response.code).to.be.oneOf([200, 201]);",
                            "});",
                            "pm.test('Response time is less than 500ms', function () {",
                            "    pm.expect(pm.response.responseTime).to.be.below(500);",
                            "});"
                        ],
                        "type": "text/javascript"
                    }
                }]
            
            # Add auth header to other endpoints
            if method != "get" or path.startswith("/api/v1/users"): # Simplified logic
                 item["request"]["auth"] = {
                    "type": "bearer",
                    "bearer": [
                        {
                            "key": "token",
                            "value": "{{access_token}}",
                            "type": "string"
                        }
                    ]
                }

            # Add Request Body if available
            if "requestBody" in details:
                try:
                    schema = details["requestBody"]["content"]["application/json"]["schema"]
                    # Simple schema to example converter
                    example_body = {}
                    if "$ref" in schema:
                        ref_name = schema["$ref"].split("/")[-1]
                        if "components" in openapi_spec and "schemas" in openapi_spec["components"]:
                            props = openapi_spec["components"]["schemas"][ref_name].get("properties", {})
                            for prop_name, prop_details in props.items():
                                example_body[prop_name] = prop_details.get("example", "string" if prop_details.get("type") == "string" else 0)
                    
                    item["request"]["body"] = {
                        "mode": "raw",
                        "raw": json.dumps(example_body, indent=2),
                        "options": {
                            "raw": {
                                "language": "json"
                            }
                        }
                    }
                except KeyError:
                    pass

            folders[folder_name].append(item)

    # Convert folders dict to Postman item list
    for folder_name, items in folders.items():
        collection["item"].append({
            "name": folder_name,
            "item": items
        })

    with open("postman_collection.json", "w") as f:
        json.dump(collection, f, indent=2)
    print("Postman collection generated: postman_collection.json")

if __name__ == "__main__":
    generate_postman_collection()
