from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, UserForm,  CustomerForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated, allowed_user, admin_only

from .filters import OrderFilter


@login_required(login_url="accounts:login")
@admin_only
def customer(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {"customers": customers, "orders": orders, "total_orders": total_orders, "delivered": delivered, "pending": pending}
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="accounts:login")
@allowed_user(allowed_role=["admin"])
def products(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "accounts/products.html", context)


@login_required(login_url="accounts:login")
@allowed_user(allowed_role=["admin"])
def customer_profile(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    total_orders = orders.count()
    context = {"orders": orders, "customer": customer, "total_orders": total_orders, "myfilter": myfilter}
    return render(request, "accounts/customer.html", context)


@login_required(login_url="accounts:login")
def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}
    return render(request, "accounts/update_order.html", context)


@login_required(login_url="accounts:login")
def delete_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {}
    return render(request, "accounts/delete_order.html", context)


@login_required(login_url="accounts:login")
@allowed_user(allowed_role=["admin"])
def create_order(request, id):
    customer = Customer.objects.get(id=id)
    formset = OrderForm(initial={"customer": customer})
    if request.method == "POST":
        formset = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {"form": formset, "customer": customer}
    return render(request, "accounts/create_order.html", context)


@unauthenticated
def register_form(request):
    form = UserForm
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            messages.success(request, f"Account is created for {username}")
            return redirect("accounts:login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated
def login_form(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("accounts:dashboard")
        else:
            messages.warning(request, f"Username or Password is not correct")

    context = {}

    return render(request, "accounts/login.html", context)


def logout_form(request):
    logout(request)
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
@allowed_user(allowed_role=["customer"])
def user_page(request):
    customer = Customer.objects.get(user=request.user)
    orders = customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {"customer": customer, "orders": orders, "total_orders": total_orders, "delivered": delivered, "pending": pending}
    return render(request, "accounts/user.html", context)


def settings(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "accounts/settings.html", context)