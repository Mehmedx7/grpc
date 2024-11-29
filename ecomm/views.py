from django.shortcuts import render
from django.utils import timezone
from faker import Faker
import random
import pandas as pd
import numpy as np
from django.http import JsonResponse
from .models import Customer, Product, Order, OrderItem
from django.db import IntegrityError

# Create your views here.

def customer_list(request):
    """
    HTTP view that can be used alongside gRPC service
    """
    customers = Customer.objects.all().values('id', 'name', 'email')
    return JsonResponse(list(customers), safe=False)


class DummyData:

    fake = Faker()

    def create_customers(self, n):
        data = {
            'name': [self.fake.name() for _ in range(n)],
            'email': [self.fake.unique.email() for _ in range(n)],
            'created_at': [timezone.now() for _ in range(n)],
            'updated_at': [timezone.now() for _ in range(n)],
        }
        df = pd.DataFrame(data)
        customers = [Customer(**row) for row in df.to_dict(orient='records')]
        try:
            Customer.objects.bulk_create(customers, ignore_conflicts=True, batch_size=10000)
        except IntegrityError as e:
            print(f"Error creating customers: {e}")

    def create_products(self, n):
        data = {
            'name': [self.fake.word() for _ in range(n)],
            'description': [self.fake.text() for _ in range(n)],
            'price': [round(random.uniform(10.0, 1000.0), 2) for _ in range(n)],
            'stock': [random.randint(0, 100) for _ in range(n)],
            'created_at': [timezone.now() for _ in range(n)],
            'updated_at': [timezone.now() for _ in range(n)],
        }
        df = pd.DataFrame(data)
        products = [Product(**row) for row in df.to_dict(orient='records')]
        try:
            Product.objects.bulk_create(products, batch_size=10000)
        except IntegrityError as e:
            print(f"Error creating products: {e}")

    def create_orders(self, n, customers):
        data = {
            'customer': [random.choice(customers) for _ in range(n)],
            'created_at': [timezone.now() for _ in range(n)],
            'updated_at': [timezone.now() for _ in range(n)],
        }
        df = pd.DataFrame(data)
        orders = [Order(**row) for row in df.to_dict(orient='records')]
        try:
            Order.objects.bulk_create(orders, batch_size=10000)
        except IntegrityError as e:
            print(f"Error creating orders: {e}")

    def create_order_items(self, n, orders, products):
        data = {
            'order': [random.choice(orders) for _ in range(n)],
            'product': [random.choice(products) for _ in range(n)],
            'quantity': [random.randint(1, 10) for _ in range(n)],
        }
        df = pd.DataFrame(data)
        order_items = [OrderItem(**row) for row in df.to_dict(orient='records')]
        try:
            OrderItem.objects.bulk_create(order_items, batch_size=10000)
        except IntegrityError as e:
            print(f"Error creating order items: {e}")

    def create_dummy_data(self):
        # Number of records to create
        num_customers = 100000
        num_products = 10000
        num_orders = 1000000
        num_order_items = 5000000

        # Create data
        print("Creating customers...")
        self.create_customers(num_customers)
        print("Creating products...")
        self.create_products(num_products)
        print("Creating orders...")
        customers = list(Customer.objects.all())
        self.create_orders(num_orders, customers)
        print("Creating order items...")
        orders = list(Order.objects.all())
        products = list(Product.objects.all())
        self.create_order_items(num_order_items, orders, products)

        print("Dummy data added successfully!")