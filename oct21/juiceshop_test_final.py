# Refactored Locust code based on actual API requests made to OWASP Juice Shop
from locust import HttpUser, TaskSet, task, between
import json
import random
import string
import logging

class UserBehavior(TaskSet):
    
    # Called when a simulated user starts executing this TaskSet class
    def on_start(self):
        self.register_and_login()

    # Function to handle API requests and log errors
    def api_request(self, method, endpoint, **kwargs):
        response = getattr(self.client, method.lower())(endpoint, **kwargs)
        if response.status_code not in [200, 201]:
            logging.error(f"{method.upper()} {endpoint} failed with error {response.status_code}: {response.text}")
            return None
        return json.loads(response.text)

    # Function to generate a random email address
    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'
    
    # Function to generate a random credit card number
    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    # Function to handle user registration and login
    def register_and_login(self):
        # Generate random email and password
        email = self.random_email()
        password = "Password123!"
        
        # Corrected the API endpoint for user registration based on actual logs
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
        
        # Corrected the API endpoint for user login based on actual logs
        login_data = {
            "email": email,
            "password": password,
        }
        self.api_request('POST', "/rest/user/login", json=login_data)

    # Task to simulate a user journey
    @task
    def complete_user_journey(self):
        # Fetch available products
        products_data = self.api_request('GET', "/rest/products/search?q=")
        if not products_data:
            return
        print(f'type: {type(products_data)}\nproducts_data: {products_data}')
        # Filter products that are available for purchase
        available_products = products_data.get('data', [])
        
        if not available_products:
            logging.info("No available products. Performing non-buying behaviors.")
            self.non_buying_behaviors()
            return

        # Randomly select up to 3 products
        selected_products = random.sample(available_products, min(3, len(available_products)))

        # Get the basket ID
        basket_id = self.get_basket_id()
        if not basket_id:
            logging.error("Could not fetch basket ID.")
            return

        # Add selected products to basket and finalize the purchase
        self.add_to_basket_and_finalize(basket_id, selected_products)

    def non_buying_behaviors(self):
        # Visiting the homepage of the application: A common action that almost every user would do.
        self.api_request('GET', "/")
        
        # Accessing the REST API root: This could be a programmatic way to discover available API routes.
        # It's a normal behavior often carried out by client-side code to understand the capabilities of the backend.
        self.api_request('GET', "/rest")
        
        # Fetching localization information: This is typically done to support multiple languages in the UI.
        # It's a standard call made by the frontend to adapt the UI based on user preferences or default settings.
        self.api_request('GET', "/assets/i18n/en.json")


    # Function to get the basket ID
    def get_basket_id(self):
        # Corrected the API endpoint for fetching Basket ID based on actual logs
        basket_data = self.api_request('GET', "/api/BasketId/")  
        return basket_data.get('id') if basket_data else None

    def add_to_basket_and_finalize(self, basket_id, selected_products):
        for product in selected_products:
            add_basket_data = {"BasketId": basket_id, "ProductId": product['id'], "quantity": 1}
            add_basket_response = self.api_request('POST', "/api/BasketItems/", json=add_basket_data)
            # Added check for successful addition to basket
            if not add_basket_response:
                logging.error("Failed to add product to basket.")
                return

        # Added checks for successful credit card and address creation
        if not self.api_request('POST', "/api/CreditCards/", json={"cardNumber": self.random_credit_card(), "expiry": "12/23", "owner": "User"}):
            logging.error("Failed to add credit card.")
            return

        if not self.api_request('POST', "/api/Addresss/", json={"street": "123 Elm St", "zipcode": "12345", "country": "US"}):
            logging.error("Failed to add address.")
            return

        # Proceed to purchase
        self.api_request('POST', "/api/Purchase/", json={"BasketId": basket_id})


# Locust user class that specifies the user behavior and other configurations
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2.5)
    host = "http://localhost:3000"  # This should match the Juice Shop instance you are testing against

# End of refactored code

# Note: API endpoints have been corrected based on the actual logs from OWASP ZAP.
# Logging has been added for better debugging and understanding of the script's behavior.
