import re
import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.utils import timezone

from .models import Customer, Product, Order


# Create GraphQL objecttypes for safe querying
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"
        
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
        
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"
        

# Basic Query to determine the data that can be read from the GraphQL endpoint
class Query(graphene.ObjectType):
    # Every read operation starts from the query
    # If a dataset is not defined here, the client cannot fetch it
    customers = graphene.List(CustomerType)             # List all CustomerTypes
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)
    
    # Next, we use resolvers tell GraphQL where to get this data from
    def resolve_customers(root, info):
        return Customer.objects.all()
    
    def resolve_products(root, info):
        return Product.objects.all()
    
    def resolve_orders(root, info):
        return Order.object.all()