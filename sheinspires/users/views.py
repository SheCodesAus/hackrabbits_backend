from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RoleModelSerializer, CommunityUserSerializer
from .permissions import IsPublicOrReadOnly, IsRoleModelUser, IsCommunityUser

from rest_framework import generics, permissions

# Create your views here.

# View to create and retrieve a Role Model Profile
class RoleModelView(APIView):
    
    #   non register user can only see limited version of role model profile.
    # registered user (including community user and role model users ) can see full details of profile

    
    permission_classes = [IsPublicOrReadOnly]

    def get(self, request):
        users = CustomUser.objects.filter(user_type="ROLE_MODEL")  # Filter by user type
        serializer = RoleModelSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  

    def post(self, request):
        serializer = RoleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )


class RoleModelDetail(APIView):

    # every registered user can see full details of role model profile
# each role model can see their own profile and every role model profile out there
# each role model can create, edit , delete their own profile, also admin can do delete their profile
    permission_classes = [IsRoleModelUser]


    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk, user_type="ROLE_MODEL")
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = RoleModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = RoleModelSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# View to create and retrieve a Community User Profile
class CommunityUserView(APIView):
  
#   each communti user can view their own profile, 
#   only role models can see every community user profile 
    permission_classes = [IsRoleModelUser]
    
    def get(self, request):
        users = CustomUser.objects.filter(user_type="COMMUNITY_USER")  # Filter by user type
        serializer = CommunityUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommunityUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )


class CommunityUserDetail(APIView):
# role model user can view each community user profile
# each community user only can see their own profile, can create, edit or delete it 
# also admin can do this.
    permission_classes = [IsCommunityUser]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk, user_type="COMMUNITY_USER")
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CommunityUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = CommunityUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# View to retrieve details of a Profile using a primary key
class CustomUserDetail(APIView):
  
  def get_object(self, pk):
      try:
          return CustomUser.objects.get(pk=pk)
      except CustomUser.DoesNotExist:
          raise Http404

# View to validate user token
class CustomAuthToken(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(
          data=request.data,
          context={'request': request}
      )
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)

      return Response({
          'token': token.key,
          'user_id': user.id,
          'email': user.email
      })
  





