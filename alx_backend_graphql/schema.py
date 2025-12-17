# Define GraphQL schema
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    # Declare single string field
    # Name: hello
    # Type: String
    # String should return a default value "Hello, GraphQL!"
    hello = graphene.String(default_value="Hello, GraphQL!")
    

class Mutation(CRMMutation, graphene.ObjectType):
    pass
    
schema = graphene.Schema(query=Query, mutation=Mutation)