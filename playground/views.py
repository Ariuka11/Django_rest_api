from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import requests


# Function based cache view
'''
@cache_page(5*60)
def say_hello(request):
    res = requests.get('https://httpbin.org/delay/2')
    data = res.json()
    return render(request, 'emails/hello.html', {'name': data})
'''


class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        res = requests.get('https://httpbin.org/delay/2')
        data = res.json()
        return render(request, 'emails/hello.html', {'name': data})
