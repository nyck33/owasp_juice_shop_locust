from locust import HttpUser, TaskSet, task, between
import json

class UserBehavior(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 2.5)
    @task
    def get_product_variant_details(self):
        query = """
        query ProductVariantsByID($ids: [ID!]!, $channel: String!, $first: Int) {
          productVariants(ids: $ids, channel: $channel, first: $first) {
            edges {
              node {
                id
                name
                pricing {
                  price {
                    gross {
                      amount
                      currency
                    }
                  }
                }
                # ... other fields you need ...
              }
            }
          }
        }
        """
        variables = {
            "ids": ["UHJvZHVjdFZhcmlhbnQ6MzQ2"],  # Replace with actual product variant IDs
            "channel": "default-channel",  # Replace with the actual channel identifier
            "first": 10  # Adjust based on how many items you want to fetch
        }
        query_json = {
            "query": query,
            "variables": variables
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # Assuming your GraphQL endpoint is at /graphql
        response = self.client.post("/graphql/", data=json.dumps(query_json), headers=headers)

        print(response.text)
        # log response to log file
        #self.log_response(response)
    
    def log_response(self, response):
        #self.environment.runner.logger.info(f"Response: {response.text}")
        pass
'''
class WebsiteUser(HttpUser):
    task_set = [UserBehavior]
    wait_time = between(5, 15)
''' 
