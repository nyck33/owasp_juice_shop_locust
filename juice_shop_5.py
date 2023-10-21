import locust
from locust import HttpUser, task, between
import random
import string
import sys

class ShopperUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 2.5)

    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    def register_user(self, email, password):
        response = self.client.post(
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

        if response.status_code != 201:
            sys.exit(f"Registration failed with error {response.status_code}: {response.text}")

        return response

    def login_user(self, email, password):
        response = self.client.post(
            "/rest/user/login",
            json={
                "email": email,
                "password": password,
            }
        )

        if response.status_code != 200:
            sys.exit(f"Login failed with error {response.status_code}: {response.text}")

        return response.json()['authentication']['token']

    @task
    def register_and_login(self):
        email = self.random_email()
        password = "Password123!"
        credit_card = self.random_credit_card()

        # Step 1: Register a new user
        self.register_user(email, password)

        # Step 2: Login
        token = self.login_user(email, password)
        
        print(f"User {email} logged in with token: {token} and credit card: {credit_card}")

# Save this script in a file, for example, locust_script.py
