from locust import HttpUser, task, between
import random
import string
import json

class ShopperUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 2.5)

    def random_email(self):
        return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'

    def random_string(self, length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def random_credit_card(self):
        return ''.join(random.choices(string.digits, k=16))

    @task
    def register_browse_and_checkout(self):
        # Step 1: Register a new user
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

        # Step 2: Login
        login_response = self.client.post(
            "/rest/user/login",
            json={
                "email": email,
                "password": password,
            }
        )
        assert login_response.status_code == 200, f"Unexpected error {login_response.status_code}: {login_response.text}"
        token = login_response.json()['authentication']['token']

        # Step 3: Browse products
        browse_response = self.client.get(
            "/api/Products/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert browse_response.status_code == 200, f"Unexpected error {browse_response.status_code}: {browse_response.text}"
        #print(f'Products: {json.dumps(browse_response.json(), indent=4)}')

        products = browse_response.json()
        # Extract the list of products from the dictionary
        products_list = products['data']

        # Now choose a random product from the list
        random_product = random.choice(products_list)

        # Extract the product ID
        product_id = random_product['id']
        #print(f"Product ID: {product_id}")


        # Step 4: Add product to cart
        cart_response = self.client.post(
            "/api/BasketItems/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "productId": product_id,
                "quantity": 1
            }
        )
        assert cart_response.status_code == 200, f"Unexpected error {cart_response.status_code}: {cart_response.text}"

        # Step 5: Checkout
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
        assert checkout_response.status_code == 201, f"Unexpected error {checkout_response.status_code}: {checkout_response.text}"
