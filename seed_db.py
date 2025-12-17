import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

Customer.objects.get_or_create(
    name="Seed User",
    email="seed@example.com",
    phone="+1234567890"
)

Product.objects.get_or_create(
    name="Phone",
    price=500,
    stock=5
)

Product.objects.get_or_create(
    name="Tablet",
    price=800,
    stock=3
)

print("Database seeded successfully")
