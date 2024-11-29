from django.contrib import admin
from .models import Customer, Product, Order, OrderItem

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'updated_at')
    search_fields = ('customer__name', 'customer__email')
    list_filter = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)