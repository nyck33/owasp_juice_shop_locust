from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def browse_products(self):
        query = """
        query {
          products(first: 10) {
            edges {
              node {
                id
                name
              }
            }
          }
        }
        """
        self.client.post("/graphql", json={"query": query})