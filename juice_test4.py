import random
import string
from locust import HttpUser, task, between

class ShopperUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 2.5)

    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    def random_string(self, length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    def register_user(self):
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
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="Register User",
                response_time=reg_response.elapsed.total_seconds(),
                response_length=0,
                exception=f"Unexpected error {reg_response.status_code}: {reg_response.text}"
            )
        return email, password

    def login_user(self, email, password):
        login_response = self.client.post(
            "/rest/user/login",
            json={
                "email": email,
                "password": password,
            }
        )
        if login_response.status_code != 200:
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="Login User",
                response_time=login_response.elapsed.total_seconds(),
                response_length=0,
                exception=f"Unexpected error {login_response.status_code}: {login_response.text}"
            )
            return None
        return login_response.json()['authentication']['token']

    def browse_products(self, token):
        browse_response = self.client.get(
            "/api/Products/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if browse_response.status_code != 200:
            self.environment.events.request_failure.fire(
                request_type="GET",
                name="Browse Products",
                response_time=browse_response.elapsed.total_seconds(),
                response_length=0,
                exception=f"Unexpected error {browse_response.status_code}: {browse_response.text}"
            )
            return None
        return browse_response.json()['data']

    def add_to_cart(self, token, product_id):
        cart_response = self.client.post(
            "/api/BasketItems/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "productId": product_id,
                "quantity": 1
            }
        )
        if cart_response.status_code != 200:
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="Add to Cart",
                response_time=cart_response.elapsed.total_seconds(),
                response_length=0,
                exception=f"Unexpected error {cart_response.status_code}: {cart_response.text}"
            )

    def checkout(self, token):
        name_on_card = self.random_string(5) + " " + self.random_string(8)
        credit_card_number = self.random_credit_card()
        checkout_response = self.client.post(
            "/api/Checkouts/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "nameOnCard": name_on_card,
                "creditCardNumber": credit_card_number,
                "creditCardExpiry": "12/23",
                "creditCardCVV": "123"
            }
        )
        if checkout_response.status_code != 201:
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="Checkout",
                response_time=checkout_response.elapsed.total_seconds(),
                response_length=0,
                exception=f"Unexpected error {checkout_response.status_code}: {checkout_response.text}"
            )

    @task
    def register_browse_and_checkout(self):
        # Step 1: Register a new user
        email, password = self.register_user()

        # Step 2: Login
        token = self.login_user(email, password)
        if token is None:
            return

        # Step 3: Browse products
        products_list = self.browse_products(token)
        if products_list is None:
            return

        # Choose a random product from the list
        random_product = random.choice(products_list)
        product_id = random_product['id']

        # Step 4: Add product to cart
        self.add_to_cart(token, product_id)

        # Step 5: Checkout
        self.checkout(token)
