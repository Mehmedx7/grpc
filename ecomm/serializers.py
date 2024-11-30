from django_socio_grpc import proto_serializers
from rest_framework import serializers
from .models import Product

class ProductSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Product
        fields = '__all__'