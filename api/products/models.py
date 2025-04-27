from django.db import models
from django.conf import settings


# Product Category Choices
class ProductCategory(models.TextChoices):
    SHIRT = "shirt", "shirt"
    TSHIRT = "T-shirt", "T-shirt"
    JEANS = "Jeans", "Jeans"
    SHOES = "Shoes", "Shoes"
    JACKET = "Jacket", "Jacket"
    ACCESSORY = "Accessory", "Accessory"
    HOODIE = "Hoodie", "Hoodie"


class Product(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("archived", "Archived"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField()
    category = models.CharField(
        max_length=255, choices=ProductCategory.choices, blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def discounted_price(self):
        return self.discount_price if self.discount_price else self.price


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    colors = models.CharField(max_length=5, choices=SIZE_CHOICES, blank=True, null=True)
    size = models.CharField(
        max_length=50, blank=True
    )  # Free-form size input (e.g., custom sizes)
    size_choice = models.CharField(
        max_length=2, choices=SIZE_CHOICES, blank=True, null=True
    )  # Predefined sizes
    image = models.ImageField(upload_to="product_variants/", null=True, blank=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size or self.size_choice}"

    def is_in_stock(self):
        return self.stock > 0

    def total_price(self):
        return (
            self.product.discounted_price()
            if self.product.discount_price
            else self.product.price
        )


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart Item - {self.user.email} - {self.product_variant.product.name} - {self.product_variant.color} - {self.product_variant.size}"

    def total_price(self):
        return self.product_variant.total_price() * self.quantity
