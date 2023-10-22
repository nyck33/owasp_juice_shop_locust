from locust import HttpUser, TaskSet, task, between
import json
import random
import sys
import string

class UserBehavior(TaskSet):
    def on_start(self):
        self.register_and_login()

    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    def register_and_login(self):
        email = self.random_email()
        password = "Password123!"

        reg_response = self.client.post(
            "/api/Users/",
            json={
                "email": email,
                "password": password,
                "passwordRepeat": password,
                "securityQuestion": {
                    "id": 2,
                    "question": "Mother's maiden name?",
                },
                "securityAnswer": "Smith"
            }
        )

        if reg_response.status_code != 201:
            sys.exit(f"Registration failed with error {reg_response.status_code}: {reg_response.text}")

        login_response = self.client.post(
            "/rest/user/login",
            json={
                "email": email,
                "password": password,
            }
        )

        if login_response.status_code != 200:
            sys.exit(f"Login failed with error {login_response.status_code}: {login_response.text}")

    def search_products(self):
        response = self.client.get("/rest/products/search?q=")
        if response.status_code != 200:
            sys.exit(f"Product search failed with error {response.status_code}: {response.text}")
        return json.loads(response.text)

    def get_basket_id(self):
        response = self.client.get("/rest/basket/6")
        if response.status_code != 200:
            sys.exit(f"Basket retrieval failed with error {response.status_code}: {response.text}")
        return json.loads(response.text)['id']

    def add_to_basket(self, basket_id, product_id):
        response = self.client.post(f"/api/BasketItems/", json={"BasketId": basket_id, "ProductId": product_id, "quantity": 1})
        if response.status_code != 201:
            sys.exit(f"Adding to basket failed with error {response.status_code}: {response.text}")

    def add_credit_card(self):
        credit_card = self.random_credit_card()
        response = self.client.post("/api/CreditCards/", json={"cardNumber": credit_card, "expiry": "12/23", "owner": "User"})
        if response.status_code != 201:
            sys.exit(f"Adding credit card failed with error {response.status_code}: {response.text}")

    def add_address(self):
        response = self.client.post("/api/Addresss/", json={"street": "123 Elm St", "zipcode": "12345", "country": "US"})
        if response.status_code != 201:
            sys.exit(f"Adding address failed with error {response.status_code}: {response.text}")

    def finalize_purchase(self, basket_id):
        response = self.client.post("/api/Purchase/", json={"BasketId": basket_id})
        if response.status_code != 201:
            sys.exit(f"Finalizing purchase failed with error {response.status_code}: {response.text}")
    
    def get_basket_id(self):
        response = self.client.get("/api/BasketId/")  # Replace with actual API for fetching Basket ID
        if response.status_code != 200:
            print(f"Basket retrieval failed with error {response.status_code}: {response.text}")
            return None
        return json.loads(response.text)['id']
    
    @task
    def complete_user_journey(self):
        response = self.client.get("/rest/products/search?q=")
        if response.status_code == 200:
            response_json = json.loads(response.text)
            products = response_json.get('data', [])  # Fetching 'data' field from response
            if isinstance(products, list) and all(isinstance(p, dict) for p in products):
                available_products = [p for p in products if p['quantity'] >= 1]
                if available_products:
                    selected_products = random.sample(available_products, min(3, len(available_products)))
                    basket_id = self.get_basket_id()
                    if basket_id:
                        for product in selected_products:
                            self.add_to_basket(basket_id, product['id'])
                        self.add_credit_card()
                        self.add_address()
                        self.finalize_purchase(basket_id)
                    else:
                        print("Could not fetch basket ID.")
                else:
                    print("No available products.")
            else:
                print(f"Unexpected data type. Expected list of dictionaries, got: {type(products)}")
        else:
            print(f"Failed to list products. HTTP status code: {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2.5)
    host = "http://localhost:3000"
