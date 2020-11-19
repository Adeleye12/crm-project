from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=90, null=True)
    phone = models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor"),
    )
    product = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=30, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Out of Delivery", "Out of Delivery"),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, null=True, choices=STATUS, default="Pending")
    date_created = models.DateTimeField(null=True, auto_now_add=True)
