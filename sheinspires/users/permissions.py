from rest_framework import permissions
from users.models import CustomUser



class IsPublicOrReadOnly(permissions.BasePermission):
    """
     general user who are not signed in can see main page, 
     can see only limited details of role model profile

    """

    def has_permission(self, request, view):
        # Allow access if the user is not authenticated (general user)
        return not request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow access to role model profiles with limited details
        return obj.user_type == CustomUser.USER_TYPES["ROLE_MODEL_USER"]


class IsRoleModelUser(permissions.BasePermission):
    """
    role model user can see all community user profile. 
    can create, update , delete their own profile

    """

    def has_permission(self, request, view):
        # Ensure the user is an authenticated role model user
        return (
            request.user.is_authenticated
            and request.user.user_type == CustomUser.USER_TYPES["ROLE_MODEL_USER"]
        )

    def has_object_permission(self, request, view, obj):
        # Allow role model users to edit, delete their own profile
        if request.method not in permissions.SAFE_METHODS:
            return obj == request.user
        # Allow viewing community user profiles
        return obj.user_type == CustomUser.USER_TYPES["COMMUNITY_USER"]


class IsCommunityUser(permissions.BasePermission):
    """
   community user can see all the role model profile with all details, 
   they can create edit and delete their own profile. 
   they can't see other community user profiles 

    """

    def has_permission(self, request, view):
        # Ensure the user is an authenticated community user
        return (
            request.user.is_authenticated
            and request.user.user_type == CustomUser.USER_TYPES["COMMUNITY_USER"]
        )

    def has_object_permission(self, request, view, obj):
        # Allow community users to edit, delete their own profile
        if request.method not in permissions.SAFE_METHODS:
            return obj == request.user
        
        # Allow viewing all role model profiles
        return obj.user_type == CustomUser.USER_TYPES["ROLE_MODEL_USER"]
