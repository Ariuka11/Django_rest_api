from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


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


@api_view()
def collection_detail(request, pk):
    return Response("ok")
