from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from . import serializers


from rest_framework import viewsets
from . import models
# Create your views here.

class HelloApiView(APIView):
    """Test api view """

    serializer_class = serializers.HelloSerializer

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


    #a method to post to our API
    #request contains info about request that was made in API call, including data that was posted
    def post(seslf, request):
        """Create a hello message with out name."""
        #when you make a post to API it returns the name posted

        serializer = serializers.HelloSerializer(data=request.data) #we're gonna pass in the data
        # handed over to this post request

        if serializer.is_valid():
            #check if data is valid amd return hello with the name posted
            name = serializer.data.get("name")
            message = "Hello {0}".format(name)
            return Response({'message': message})
        else:
            #else 404 with status of what went wrong
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



# IN A REAL API YOU'D BUILD THE LOGIC TO ACTUALLY PUT, PATCH AND DELETE

    def put(self, request, pk=None):
        """Handles updating an object"""

        return Response({'method':'put'})

    def patch(self, request, pk=None):
        """Patch request ony updates fields provided in the request"""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Deletes an object"""

        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet """

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions )list, create, retrieve, update, partial_update',
            'Automatically maps to URLs usion Routers',
            'Providers more functionality with less code',
        ]

        return Response({'message':'Hello','a_viewset':a_viewset})


    def create(self, request):
        """Create a new hello message"""
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            #if valid, add the same functionality as APIView
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else :
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting  an object by its ID"""
        #no logic , simply response
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an object """

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method':'PATCH'})
        #again, needs a primary key to know which object it is destroying
    def destroy(self, request, pk=None):
        """Handles removing an object"""

        return Response({'http_method':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet): #modeLviewset takes care of the followin
    """Handles creating, reading and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    #this serailizer has model class in metadata set
    #it knows what to look for
    queryset = models.UserProfile.objects.all()
