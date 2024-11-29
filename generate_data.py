import os
import django
import random
from faker import Faker
from ecomm.models import Customer, Product, Order, OrderItem
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

fake = Faker()

def create_customers(n):
    customers = []
    for _ in range(n):
        customer = Customer(
            name=fake.name(),
            email=fake.email(),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        customers.append(customer)
    Customer.objects.bulk_create(customers)

def create_products(n):
    products = []
    for _ in range(n):
        product = Product(
            name=fake.word(),
            description=fake.text(),
            price=round(random.uniform(10.0, 1000.0), 2),
            stock=random.randint(0, 100),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        products.append(product)
    Product.objects.bulk_create(products)

def create_orders(n, customers):
    orders = []
    for _ in range(n):
        order = Order(
            customer=random.choice(customers),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        orders.append(order)
    Order.objects.bulk_create(orders)

def create_order_items(n, orders, products):
    order_items = []
    for _ in range(n):
        order_item = OrderItem(
            order=random.choice(orders),
            product=random.choice(products),
            quantity=random.randint(1, 10)
        )
        order_items.append(order_item)
    OrderItem.objects.bulk_create(order_items)

# Number of records to create
num_customers = 100000
num_products = 10000
num_orders = 1000000
num_order_items = 5000000

# Create data
print("Creating customers...")
create_customers(num_customers)
print("Creating products...")
create_products(num_products)
print("Creating orders...")
customers = list(Customer.objects.all())
create_orders(num_orders, customers)
print("Creating order items...")
orders = list(Order.objects.all())
products = list(Product.objects.all())
create_order_items(num_order_items, orders, products)

print("Dummy data added successfully!")