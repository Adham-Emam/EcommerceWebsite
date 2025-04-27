from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path(
        "cart/", views.CartView.as_view(), name="cart-list"
    ),  # Handles both GET and POST for cart
    path("cart/<int:pk>/", views.CartItemDetailView.as_view(), name="cart-item-detail"),
]
