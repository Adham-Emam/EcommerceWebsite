from rest_framework import serializers
from .models import Product, ProductVariant, Cart


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)  # Nested serializer

    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Nested product serializer

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        """Ensure that the cart item is unique for the user and product."""
        user = self.context[
            "request"
        ].user  # Get the logged-in user from the request context
        product = attrs["product"]

        # Check if the product is already in the user's cart
        if Cart.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("This product is already in your cart.")

        return attrs
