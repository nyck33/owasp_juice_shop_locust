'''
locust -f user_story_test.py --headless -u 100 -r 10 --host http://localhost:3000 --csv="locust_reports/full_path_user$(date +\%Y\%m\%d\%H\%M\%S)"
#web gui
locust -f user_story_test.py -u 100 -r 10 --host http://localhost:3000

'''

from locust import HttpUser, TaskSet, task, between
import json
import random
import string
import logging
import time
from datetime import datetime

# Create a logging handler that flushes after each write
class FlushingHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

# Set up logging with the custom handler
logger = logging.getLogger()
handler = FlushingHandler('user_journey.log', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Print out the list of all handlers to debug
print(f"List of all handlers: {logger.handlers}")

logger.info('Starting script')
logger.handlers[0].flush()  # Explicitly flush the logs


class UserBehavior(TaskSet):

    def on_start(self):
        self.token = None  # Initialize token for this user instance
        logger.info("User instance started.")
        self.register_and_login()

    def api_request(self, method, endpoint, headers=None, **kwargs):

        timestamp = datetime.now().isoformat()
        logger.info(f"{timestamp} - Sending{method.upper()} request to {endpoint})")

        
        if headers is None:
            headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = getattr(self.client, method.lower())(endpoint, headers=headers, **kwargs)
        
        # Log the response details using the response_time attribute
        if response.status_code not in [200, 201]:
            logger.error(f"Response took {response.elapsed.total_seconds()}s - {method.upper()} {endpoint} failed with error {response.status_code}: {response.text}")
            return None
        else:
            logger.info(f"Response took {response.elapsed.total_seconds()}s - Received {response.status_code} response from {endpoint}")

        return json.loads(response.text)


    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    def register_and_login(self):
        logger.info("Registering and logging in.")
        logger.handlers[0].flush()  # Explicitly flush the logs
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
        self.api_request('POST', "/api/Users/", json=reg_data)
        time.sleep(random.uniform(0.5, 1.5))  # Random sleep time

        login_data = {
            "email": email,
            "password": password,
        }
        login_response = self.api_request('POST', "/rest/user/login", json=login_data)

        if login_response:
            self.token = login_response.get('authentication', {}).get('token')
            self.basket_id = login_response.get('authentication', {}).get('bid')
            logger.info(f"Logged in with basket ID: {self.basket_id}")

    @task
    def complete_user_journey(self):
        logger.info("Starting user journey.")
        
        products_data = self.api_request('GET', "/rest/products/search?q=")
        if not products_data:
            logger.error("Failed to get products.")
            return

        time.sleep(random.uniform(0.2, 1.0))  # Random sleep time

        available_products = products_data.get('data', [])
        
        if not available_products:
            logger.info("No available products.")
            return

        selected_products = random.sample(available_products, min(3, len(available_products)))
        logger.info(f"Selected products: {selected_products}")

        if not self.basket_id:
            logger.error("Could not fetch basket ID.")
            return

        for product in selected_products:
            basket_item_data = {
                "BasketId": self.basket_id,
                "ProductId": product['id'],
                "quantity": 1
            }
            self.api_request('POST', "/api/BasketItems/", json=basket_item_data)
            time.sleep(random.uniform(0.5, 1.5))  # Random sleep time

        logger.info("Added items to basket.")

        if random.choice([True, False]):
            self.api_request('POST', "/api/Addresss/", json={"street": "123 Elm St", "zipcode": "12345", "country": "US"})
            logger.info("Added address.")
        
        time.sleep(random.uniform(0.2, 1.0))  # Random sleep time

        self.api_request('POST', "/api/Cards/", json={"cardNumber": self.random_credit_card(), "expiry": "12/23", "owner": "User"})
        logger.info("Added credit card.")
        
        time.sleep(random.uniform(0.2, 1.0))  # Random sleep time

        if random.choice([True, False]):
            self.api_request('POST', f"/rest/basket/{self.basket_id}/checkout", json={})
            logger.info("Completed checkout.")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2.5)
    host = "http://localhost:3000"
