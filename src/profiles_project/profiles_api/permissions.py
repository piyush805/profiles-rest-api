#django rest framework uses this class to determine if the user has
#the permission to make the changes they are asking
#TO CHECK FOR LEGAL PERSMISION

from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Alllow users to edit their own profile"""
#has a  funtion inside it to check
#hasobjectpermission => Boolean Value
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""
        #making viewing other's profile as safe [safe_method_list]
        if request.method in permissions.SAFE_METHODS:
            #if the method that was used to request is in SAFE_METHODS
            return True
        #if goes further, it means that user is trying to request
        # with methods that are not SAFE_MRTHODS
        return obj.id == request.user.id
        #True if it's their own profile, else False


class PostOwnStatus(permissions.BasePermission):
    """Allow users to update their own status."""

    def has_object_permission(self, request, view,obj):
        """Checks the user is trying to update their own status"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
        #similar to previous class functioning
