from django.urls import path
from . import views

urlpatterns = [
    path('api/customers/', views.customer_list, name='customer_list'),
]