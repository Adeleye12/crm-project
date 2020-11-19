from django.contrib import admin
from .models import Customer, Product, Order


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")


admin.site.register(Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("product", "price", "category")


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("status", "date_created")


admin.site.register(Order, OrderAdmin)