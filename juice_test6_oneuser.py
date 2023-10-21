from locust import HttpUser, TaskSet, task, between
import json
import random
import string
import logging

class UserBehavior(TaskSet):
    def on_start(self):
        self.register_and_login()

    def api_request(self, method, endpoint, **kwargs):
        response = getattr(self.client, method)(endpoint, **kwargs)
        if response.status_code not in [200, 201]:
            logging.error(f"{method.upper()} {endpoint} failed with error {response.status_code}: {response.text}")
            return None
        return json.loads(response.text)

    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    def register_and_login(self):
        email = self.random_email()
        password = "Password123!"
        
        reg_data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {
                "id": 2,
                "question": "Mother's maiden name?",
            },
            "securityAnswer": "Smith"
        }
        
        self.api_request('post', "/api/Users/", json=reg_data)
        
        login_data = {
            "email": email,
            "password": password,
        }

        self.api_request('post', "/rest/user/login", json=login_data)

    @task
    def complete_user_journey(self):
        products_data = self.api_request('get', "/rest/products/search?q=")
        if not products_data:
            return

        available_products = [p for p in products_data.get('data', []) if p['quantity'] >= 1]
        if not available_products:
            logging.info("No available products.")
            return

        selected_products = random.sample(available_products, min(3, len(available_products)))
        
        basket_id = self.get_basket_id()
        if not basket_id:
            logging.error("Could not fetch basket ID.")
            return

        self.add_to_basket_and_finalize(basket_id, selected_products)

    def get_basket_id(self):
        basket_data = self.api_request('get', "/api/BasketId/")  # Replace with actual API for fetching Basket ID
        return basket_data.get('id') if basket_data else None

    def add_to_basket_and_finalize(self, basket_id, selected_products):
        for product in selected_products:
            add_basket_data = {"BasketId": basket_id, "ProductId": product['id'], "quantity": 1}
            self.api_request('post', "/api/BasketItems/", json=add_basket_data)
        
        self.api_request('post', "/api/CreditCards/", json={"cardNumber": self.random_credit_card(), "expiry": "12/23", "owner": "User"})
        self.api_request('post', "/api/Addresss/", json={"street": "123 Elm St", "zipcode": "12345", "country": "US"})
        self.api_request('post', "/api/Purchase/", json={"BasketId": basket_id})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2.5)
    host = "http://localhost:3000"
