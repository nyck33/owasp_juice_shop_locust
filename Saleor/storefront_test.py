from locust import HttpUser, task, between
from extracted_mutations import *

class SaleorStorefrontUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Use the actual mutation for user registration
        self.client.post("http://localhost:3000/graphql", json={
            "query": USERREGISTER_MUTATION,
            "variables": {
                "input": {
                    "email": "user@example.com",
                    "password": "Password123!"
                }
            }
        })

    @task
    def browse_products(self):
        self.client.get("http://localhost:3000/products")

    @task
    def add_to_cart(self):
        # Use the actual mutation for adding a product to the cart
        self.client.post("http://localhost:3000/graphql", json={
            "query": CHECKOUTADDLINE_MUTATION,
            "variables": {
                "id": "<checkout_id>", # Replace with the actual checkout ID
                "productVariantId": 1 # Replace with the actual product variant ID
            }
        })

    @task
    def proceed_to_checkout(self):
        self.client.get("http://localhost:3000/checkout")

    @task
    def complete_checkout(self):
        # Use the actual mutation for completing the checkout
        self.client.post("http://localhost:3000/graphql", json={
            "query": CHECKOUTCOMPLETE_MUTATION,
            "variables": {
                "checkoutId": "<checkout_id>" # Replace with the actual checkout ID
            }
        })

    @task
    def browse_more_products(self):
        self.client.get("http://localhost:3000/products/category/some-category")

# Start the test
if __name__ == "__main__":
    #import os
    #os.system("locust -f this_script.py")
    pass
