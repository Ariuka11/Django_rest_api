from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal

"""
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
"""


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


# Explicit version of defining fields in serializer
"""
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source="unit_price"
    )
    price_with_tex = serializers.SerializerMethodField(method_name="calculate_tax")
    # Getting Related object options:

    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(), view_name="collection-detail"
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
"""

# Implicit version of defining fields in serializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
        ]

    # Can override defualt collection representation by below code
    """
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(), view_name="collection-detail"
    )
    """
    price_with_tax = serializers.SerializerMethodField(
        method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "date",
            "name",
            "description",
        ]

    # Grabbing the product id from the URL
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'quantity', 'total_price'
        ]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = [
            'id', 'items', 'total_price'
        ]
