from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("", views.customer, name="dashboard"),
    path("products/", views.products, name="products"),
    path("customer/<int:id>/", views.customer_profile, name="customer-id"),
    path("<int:id>/update/", views.update_order, name="update-order"),
    path("<int:id>/delete/", views.delete_order, name="delete-order"),
    path("<int:id>/create/", views.create_order, name="create-order"),
    path("register/", views.register_form, name="register"),
    path("login/", views.login_form, name="login"),
    path("logout/", views.logout_form, name="logout"),
    path("user/", views.user_page, name="user-page"),
    path("settings/", views.settings, name="settings"),
]