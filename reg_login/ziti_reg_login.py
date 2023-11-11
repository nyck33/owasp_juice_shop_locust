'''
Based on the README files for the Ziti-enabled urllib3 and requests examples, there are a couple of key points to consider when integrating Ziti with your Locust script:

Environment Variables: The ZITI_IDENTITIES environment variable needs to be set to the path of the identity file. This is crucial for Ziti to know which identity to use when making requests.

Optional Service Address: Both examples accept an optional service address as a command-line argument. If none is provided, they default to a service from ZEDS (Ziti Edge Developer Services).

Here's how you could adapt your Locust script to include these considerations:

export ZITI_IDENTITIES="/path/to/id.json"
locust -f locust_script_with_ziti.py --host http://localhost:3000 --users 100 --spawn-rate 10

'''

import os
import sys
import locust
from locust import HttpUser, task, between
import random
import string
import openziti

# Set ZITI_IDENTITIES environment variable
os.environ['ZITI_IDENTITIES'] = "/path/to/id.json"

class ShopperUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 2.5)

    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    @task
    def register_and_login(self):
        with openziti.monkeypatch():
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

            assert reg_response.status_code == 201, f"Unexpected error {reg_response.status_code}: {reg_response.text}"

            login_response = self.client.post(
                "/rest/user/login",
                json={
                    "email": email,
                    "password": password,
                }
            )

            assert login_response.status_code == 200, f"Unexpected error {login_response.status_code}: {login_response.text}"

            token = login_response.json()['authentication']['token']
            print(f"User {email} logged in with token: {token}")
