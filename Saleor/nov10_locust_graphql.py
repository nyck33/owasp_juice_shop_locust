from locust import HttpLocust, TaskSet, task, between
from locustgraphqlclient import GraphQLLocust

class UserBehavior(TaskSet):
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
        result = self.client.execute("getProductVariantDetails", query, variables)

class WebsiteUser(GraphQLLocust):
    task_set = UserBehavior
    #tasks = [UserBehavior]
    #wait_time = between(5, 15)
    min_wait = 5000
    max_wait = 9000