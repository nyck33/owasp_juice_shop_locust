'''
# run for 10 min
locust -f juice_shop_test.py --headless -u 100 -r 10 --host http://localhost:3000 --run-time 10m
locust -f locustfile.py --headless -u 100 -r 10 --host http://localhost:3000

'''

from locust import HttpUser, task, between
import random

class JuiceShopUser(HttpUser):
    wait_time = between(1, 5)  # Users wait between 1 and 5 seconds between tasks

    @task(3)
    def browse_products(self):
        self.client.get("/#/search")

    @task(2)
    def view_product(self):
        # Assuming product IDs 1 through 10 are valid
        product_id = random.randint(1, 10)
        self.client.get(f"/#/product/{product_id}")

    @task(1)
    def add_to_cart(self):
        # You'll need to handle authentication and session management
        # to successfully add a product to the cart.
        # This is a simplified example:
        product_id = random.randint(1, 10)
        self.client.post(f"/api/BasketItems/", json={"ProductId": product_id, "quantity": 1})

# Run this script with Locust using the following command:
# locust -f locustfile.py --headless -u 100 -r 10 --host http://localhost:3000
