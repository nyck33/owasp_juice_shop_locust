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
    
    def add_random_items_to_cart(driver):
        num_items = random.randint(1, 10)  # Picks a random number of items to add to the cart (1 to 10)
        for _ in range(num_items):
            item_id = random.randint(1, 43)  # Picks a random item ID (1 to 43)
            # Assume there's a function to add an item to the cart by its ID
            add_item_to_cart(driver, item_id)

    def add_item_to_cart(self, driver, item_id):
        # ... (your logic to add an item to the cart by its ID)
        add_item_response = self.client.post(f"/api/BasketItems/", json={"ProductId": item_id, "quantity": 1})
        # check for a successful add
        assert add_item_response.status_code == 201, f"Unexpected error {add_item_response.status_code}: {reg_response.text}"

    def enter_payment_info(driver):
        driver.find_element_by_id("address").send_keys(fake.address())  # Generates a random address
        driver.find_element_by_id("card_number").send_keys(fake.credit_card_number())  # Generates a random credit card number





import random
import string
from faker import Faker
from selenium import webdriver

fake = Faker()

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def register_user(driver):
    # ... (rest of the registration logic remains the same)
    driver.find_element_by_id("name").send_keys(fake.name())  # Generates a random name

def add_random_items_to_cart(driver):
    num_items = random.randint(1, 10)  # Picks a random number of items to add to the cart (1 to 10)
    for _ in range(num_items):
        item_id = random.randint(1, 43)  # Picks a random item ID (1 to 43)
        # Assume there's a function to add an item to the cart by its ID
        add_item_to_cart(driver, item_id)

def add_item_to_cart(driver, item_id):
    # ... (your logic to add an item to the cart by its ID)
    self.client.post(f"/api/BasketItems/", json={"ProductId": product_id, "quantity": 1})


def enter_payment_info(driver):
    driver.find_element_by_id("address").send_keys(fake.address())  # Generates a random address
    driver.find_element_by_id("card_number").send_keys(fake.credit_card_number())  # Generates a random credit card number

# Main script
driver = webdriver.Chrome()
register_user(driver)
add_random_items_to_cart(driver)
enter_payment_info(driver)
# ... (rest of your script)
