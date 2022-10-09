from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import requests
import logging


# Function based cache view
'''
@cache_page(5*60)
def say_hello(request):
    res = requests.get('https://httpbin.org/delay/2')
    data = res.json()
    return render(request, 'emails/hello.html', {'name': data})
'''
'''
# This is for Caching result from 3rd API

class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        res = requests.get('https://httpbin.org/delay/2')
        data = res.json()
        return render(request, 'emails/hello.html', {'name': data})
'''
logger = logging.getLogger(__name__)


class HelloView(APIView):

    def get(self, request):
        try:
            logger.info('Calling HttpBin')
            res = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = res.json()
        except requests.ConnectionError:
            logger.critical("HttpBin is offline")
        return render(request, 'emails/hello.html', {'name': data})
