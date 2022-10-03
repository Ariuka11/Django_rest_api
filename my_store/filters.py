from django_filters.rest_framework import FilterSet
from .models import Product


# "I want to filter products by collection_id and unit_price."
# 
# The first line of the class definition is the most important. It tells Django that this class is a
# filter for the Product model
class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"collection_id": ["exact"], "unit_price": ["gt", "lt"]}
