# Define GraphQL schema
import graphene

class Query(graphene.ObjectType):
    # Declare single string field
    # Name: hello
    # Type: String
    hello = graphene.String(description="A typical hello world")

    # String should return a default value "Hello, GraphQL!"
    def resolve_hello(self, info):
        return "Hello, GraphQL!"