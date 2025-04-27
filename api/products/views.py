from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import Product, ProductVariant, Cart
from .serializers import ProductSerializer, ProductVariantSerializer, CartSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(status="active")

        # Get filter params
        category = self.request.query_params.get("category")

        filters = {}

        if category:
            filters["category"] = category

        # Apply filters
        queryset = queryset.filter(**filters).distinct()

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.get(user=self.request.user)

    def perform_create(self, serializer):
        # Get product ID from the request
        product_id = self.request.data.get("product")
        product = Product.objects.get(id=product_id)

        # Save the cart item with the logged-in user
        serializer.save(user=self.request.user, product=product)


class CartItemDetailView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user, id=self.kwargs["pk"])
