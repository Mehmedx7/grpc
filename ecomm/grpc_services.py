import grpc
from google.protobuf import wrappers_pb2, timestamp_pb2, empty_pb2
from django.db import transaction
from django.utils import timezone

from .protos import ecommerce_pb2, ecommerce_pb2_grpc
from .models import Customer

class CustomerServicer(ecommerce_pb2_grpc.CustomerServiceServicer):
    def CreateCustomer(self, request, context):
        try:
            customer = Customer.objects.create(
                name=request.name,
                email=request.email
            )
            return self._convert_customer_to_proto(customer)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return ecommerce_pb2.CustomerModel()

    def GetCustomer(self, request, context):
        try:
            customer = Customer.objects.get(id=request.value)
            return self._convert_customer_to_proto(customer)
        except Customer.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Customer not found')
            return ecommerce_pb2.CustomerModel()

    def UpdateCustomer(self, request, context):
        try:
            with transaction.atomic():
                customer = Customer.objects.get(id=request.id)
                
                if request.name.value:
                    customer.name = request.name.value
                if request.email.value:
                    customer.email = request.email.value
                
                customer.save()
                return self._convert_customer_to_proto(customer)
        except Customer.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Customer not found')
            return ecommerce_pb2.CustomerModel()

    def DeleteCustomer(self, request, context):
        try:
            customer = Customer.objects.get(id=request.value)
            customer.delete()
            return empty_pb2.Empty()
        except Customer.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Customer not found')
            return empty_pb2.Empty()

    def ListCustomers(self, request, context):
        customers = Customer.objects.all()
        for customer in customers:
            yield self._convert_customer_to_proto(customer)

    def _convert_customer_to_proto(self, customer):
        created_at = timestamp_pb2.Timestamp()
        created_at.FromDatetime(customer.created_at)
        
        updated_at = timestamp_pb2.Timestamp()
        updated_at.FromDatetime(customer.updated_at)
        
        return ecommerce_pb2.CustomerModel(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            updated_at=updated_at,
            created_at=created_at,
        )