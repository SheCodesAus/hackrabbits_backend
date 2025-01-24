from rest_framework import permissions
from users.models import CustomUser



class IsPublicOrReadOnly(permissions.BasePermission):
    
    #  Allow public (unauthenticated) users to view limited details of role model profiles.
    #  Allow registered (authenticated) users to view the full profile of role model profiles.
    #  Only role model profiles (user_type == 'ROLE_MODEL') are accessible.


    def has_permission(self, request, view):
        
        #  Allow SAFE (read-only) methods for all users (authenticated or not).
        
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
    
        # Allow access only to role model profiles (user_type == 'ROLE_MODEL').
        # Public users can see limited details.
        # Registered users can see full details.
        
        if obj.user_type != "ROLE_MODEL":
            # Deny access if the object is not a role model profile
            return False

        # Allow public (unauthenticated) users to see limited details
        if not request.user.is_authenticated:
            return True  # Public users can access SAFE methods with limited details

        # Allow authenticated (registered) users to access the full profile
        return True


class IsRoleModelUser(permissions.BasePermission):
    """
    role model user can see all community user profile. 
    can create, update , delete their own profile

    """

    def has_permission(self, request, view):
        # Ensure the user is an authenticated role model user
        return (
            request.user.is_authenticated and
            request.user.user_type == "ROLE_MODEL"
        )

    def has_object_permission(self, request, view, obj):
        # Allow role model users to edit, delete their own profile
        if request.method not in permissions.SAFE_METHODS:
            return obj == request.user
        # Allow viewing community user profiles
        return obj.user_type == "COMMUNITY_USER"


class IsCommunityUser(permissions.BasePermission):
    """
   community user can see all the role model profile with all details, 
   they can create edit and delete their own profile. 
   they can't see other community user profiles 

    """

    def has_permission(self, request, view):
        # Ensure the user is an authenticated community user
        return (
            request.user.is_authenticated and
            request.user.user_type == "COMMUNITY_USER"
            )

    def has_object_permission(self, request, view, obj):
        # Allow community users to edit, delete their own profile
        if request.method not in permissions.SAFE_METHODS:
            return obj == request.user
        
        # Allow viewing all role model profiles
        return obj.user_type == "ROLE_MODEL"
