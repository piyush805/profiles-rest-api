from rest_framework import serializers

from . import models




class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serilizer for our user profile objects"""

    class Meta:
        #need to define model pointing at
        model = models.UserProfile
        #what fields in our model we want to use in serializer
        fields = ('id','email','name','password')
        #extra attributees to apply to these passwords
        extra_kwargs = {'password':{'write_only': True}}#password shouild be write onlu, not read only
        #special function that overrides create functionlaity
        #we want ot be able to assign passwords correctly, calling the set function
    def create(self, validated_data):
        """Create and return a new user"""
        user  = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )
        #sets the validated passsword as password in userprofile
        user.set_password(validated_data['password'])
        user.save()

        return user
