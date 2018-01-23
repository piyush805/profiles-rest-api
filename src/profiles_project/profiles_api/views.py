from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from . import serializers


from rest_framework import viewsets
from . import models

from . import permissions
from rest_framework.authentication import TokenAuthentication
#gives user a temporary toekn to insert in the header of Http request to authenticate them

from rest_framework import filters

from rest_framework.authtoken.serializers import AuthTokenSerializer
#rest api login authentication
from rest_framework.authtoken.views import ObtainAuthToken
#will trick api into using above but customized

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.permissions import IsAuthenticated
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
    #adding authentication class varible
    authentication_classes = (TokenAuthentication,)
    #tuple contains all the authentication types| object will be created as tuple hence immutable
    permission_classes = (permissions.UpdateOwnProfile,)
    #tuples, incase you want to add more than one authentication method

    #indicate all the filter that you want to  have on this viewset
    filter_backends = (filters.SearchFilter,)
    #which field we want the user to filter by
    search_fields = ('name', 'email',)





class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer
    #create is what is called when you make HTTP POST to the viewset
    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and creatre a token."""

        return ObtainAuthToken().post(request)
        #obtained token, then post funxtion of the obtained token class

        #now add this voeiewset to URL Router

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed ones"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    #will allow both (can only post their own, also can't edit other's under authenticated)

    def perform_create(self, serializer):
        """Sets the user preofile to the logged in user"""

        serializer.save(user_profile=self.request.user)
