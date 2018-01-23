from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class HelloApiView(APIView):
    """Test api view """
    #APIViews work by defining  func that matchees std http func
    def get(self, request, format=None):
        """Returns a list of APIView feature"""
        #list of features that APIView offers
        an_apiview = [
            "Uses HTTP methods as function(get, post, patch, put, delete)",
            "It is similar to traditional Djnago View",
            "Gives you the most control over your logic",
            "Is mapped manually to URLs"
        ]
        #return object must be passed like a dictionary to the
        #dictionary converted to JSON
        return Response({"message": 'Hello', "an_apiview": an_apiview})
