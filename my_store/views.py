from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter

'''
# Class Based Mixin View
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    # Use below code to add logic to the queryset and serializer
    """
    def get_queryset(self):
        return Product.objects.select_related("collection").all()

    def get_serializer_class(self):
        return ProductSerializer
    """

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "Product is assiocated with existing Order. Can not delete"},
                status=status.HTTP_409_CONFLICT,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
"""
# Class Based View
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "Product is assiocated with existing Order. Can not delete"},
                status=status.HTTP_409_CONFLICT,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# Function Based View
'''
@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        # select_related field helps with serializer by prefetching related object
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)
    elif request.method == "POST":
        # This is a deserialization process from incoming data
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # .save() automatically deserialize the validated data
        serializer.save()
        # serializer.validated_data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Below code is same as above
        """
        if serializer.is_valid():
            serializer.validated_data()
            return Response("ok")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    # This function does the same thing as get_object_or_404
    """
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    """

    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == "DELETE":
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "Product is assiocated with existing Order. Can not delete"},
                status=status.HTTP_409_CONFLICT,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''

"""
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}
"""


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    # Below code used when no filter_backend is deifined\
    """
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get("collection_id")
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

        return super().get_queryset()
    """

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]) > 0:
            return Response(
                {"error": "Product is assiocated with existing Order. Can not delete"},
                status=status.HTTP_409_CONFLICT,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Products.objects.filter(collection_id=kwargs["pk"]) > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it includes one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Changing to queryset to match the product id
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    # Passing the product it to serializer
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
