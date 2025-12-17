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