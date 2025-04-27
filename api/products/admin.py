from django.contrib import admin
from .models import Product, ProductVariant, Cart


# Register the Variant model (nested within Product)
class VariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # This will allow adding at least one variant inline


# Register the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "get_image_url",
    )  # Use get_image_url method for image field
    search_fields = ("name", "category")
    list_filter = ("category", "price", "stock")
    inlines = [VariantInline]  # Include variants inline with the product

    def get_image_url(self, obj):
        """Method to display the product image URL"""
        if obj.image:
            return obj.image.url
        return "No Image"

    get_image_url.short_description = "Image"


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product_variant",
        "quantity",
        "added_at",
    )  # Use 'added_at', not 'created_at'
    list_filter = ("added_at",)  # Use 'added_at' in the filter


# Register the models
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
