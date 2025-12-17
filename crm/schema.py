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
    

# Add mutations that allow PUT/POST/PATCH/DELETE actions on datasets
class CreateCustomer(graphene.Mutation):
    # After the client runs the mutation, the output fields: customer and message are returned.
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    # Arguments/Input expected from client to create a new customer
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()
        
    def mutate(self, info, name, email, phone=None):
        # Check if provided email already exists
        # This prevents duplicate customer creation
        if Customer.objects.filter(email=email).exist():
            raise Exception("Email already exists")
        
        # Validate phone number format
        if phone:
            pattern = r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$'
            if not re.match(pattern, phone):
                raise Exception("Invalid phone format")
            
        customer = Customer.object.create(
            name=name,
            email=email,
            phone=phone
        )
        
        return CreateCustomer(
            customer=customer,
            message="Customer created successfully"
        )


# For Bulk Creation of Customers
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()
    
class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)
    
    class Arguments:
        input = graphene.List(CustomerInput, required=True)
        
    def mutate(self, info, input):
        created_customers = []
        errors = []
        
        for idx, data in enumerate(input):
            try:
                if Customer.objects.filter(email=data.email).exist():
                    raise Exception("Email already exists")
                
                if data.phone:
                    pattern = r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$'
                    
                customer = Customer.object.create(
                    name = data.name,
                    email = data.email,
                    phone = data.phone
                )
                
                created_customers.append(customer)
            
            except Exception as e:
                return errors.append(f"Record {idx + 1}: {str(e)}")
            
        return BulkCreateCustomers(
            customers = created_customers,
            errors = errors
        )
        

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)
    message = graphene.String()
    
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()
        
    def mutate(self, info, name, price, stock):
        # Ensure that price is positive
        if price <= 0:
            raise Exception("Price must be positive")
        
        # Ensure that stock is not negative
        if stock < 0:
            raise Exception("Stock cannot be negative")
        
        product = Product.objects.create(
            name = name,
            price = price,
            stock = stock
        )
        
        return CreateProduct(
            product = product,
            message="Product added successfully"
        )
        

class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)
    message = graphene.String()
    
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.Date(required=True)
        
    def mutate(self, info, customer_id, product_ids, order_date, total_amount):
        if not product_ids:
            raise Exception("At least one product must be selected")
        
        try:
            customer = Customer.objects.get(id=customer_id) 
        except Customer.DoesNotExist:
            raise Exception("Invalid Customer ID.")
        
        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("One or more Product IDs are invalid.")
        
        total_amount = sum(product.price for product in products)
        
        order = Order.objects.create(
            customer=customer,
            order_date=order_date or timezone.now(),
            total_amount=total_amount
        )
        
        order.products.set(products)
        
        return CreateOrder(
            order=order,
            message = "Order created successfully"
        )
        
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
