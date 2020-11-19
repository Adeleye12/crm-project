from django.forms import ModelForm, Form
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ("customer", "product", "status")


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "phone", "email", "profile_pic")