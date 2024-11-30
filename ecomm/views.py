from django.shortcuts import render
from django_socio_grpc import generics
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

class ProductService(generics.AsyncModelService):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
