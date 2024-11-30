from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from .views import ProductService

def grpc_handlers(server):
    app_registry = AppHandlerRegistry("ecomm", server)
    app_registry.register(ProductService)