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

# View to create and retrieve a Community User Profile
class CommunityUserView(APIView):
  
    permission_classes = [IsPublicOrReadOnly]
    
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
  





