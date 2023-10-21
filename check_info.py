import requests
import json

# URL of the target web application
base_url = "http://localhost:3000"

# Registration endpoint
registration_url = f"{base_url}/api/users"
registration_response = requests.post(registration_url, json={
    "email": "nobu@example.com",
    "password": "Password123!"
})

print(f"Registration Status Code: {registration_response.status_code}")
print(f"Registration Response: {json.dumps(registration_response.json(), indent=4)}")

# Extract token if available in the registration response
token = registration_response.json().get('data', {}).get('deluxeToken', None)
print(f"Token: {token}")

# Browse Products endpoint
browse_products_url = f"{base_url}/api/products"
browse_products_response = requests.get(browse_products_url)

print(f"Browse Products Status Code: {browse_products_response.status_code}")
print(f"Browse Products Response: {json.dumps(browse_products_response.json(), indent=4)}")

# If token is available, proceed to view basket
if token:
    # View Basket endpoint
    view_basket_url = f"{base_url}/api/basket"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    view_basket_response = requests.get(view_basket_url, headers=headers)

    print(f"View Basket Status Code: {view_basket_response.status_code}")
    try:
        print(f"View Basket Response: {json.dumps(view_basket_response.json(), indent=4)}")
    except json.decoder.JSONDecodeError:
        print(f"Failed to parse JSON response: {view_basket_response.text}")
else:
    print("No authorization token available. Unable to view basket.")
