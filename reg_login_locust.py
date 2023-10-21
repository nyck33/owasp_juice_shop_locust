import locust
from locust import HttpUser, task, between
import random
import string

class ShopperUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 2.5)
    # rest of your code

    def random_email(self):
        # Generate a random email address
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    @task
    def register_and_login(self):
        # Generate unique email for new user registration
        email = self.random_email()
        password = "Password123!"

        # Step 1: Register a new user
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

        # Check for a successful registration
        assert reg_response.status_code == 201, f"Unexpected error {reg_response.status_code}: {reg_response.text}"

        # Step 2: Login
        login_response = self.client.post(
            "/rest/user/login",
            json={
                "email": email,
                "password": password,
            }
        )

        # Check for a successful login
        assert login_response.status_code == 200, f"Unexpected error {login_response.status_code}: {login_response.text}"

        # Extract the token
        token = login_response.json()['authentication']['token']
        print(f"User {email} logged in with token: {token}")

# Save this script in a file, for example, locust_script.py
