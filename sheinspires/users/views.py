
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RoleModelSerializer, CommunityUserSerializer

from rest_framework import generics, permissions
from .serializers import RoleModelSerializer, CommunityUserSerializer
from .permissions import IsPublicOrReadOnly, IsRoleModelUser, IsCommunityUser


# Create your views here.

# View to create and retrieve a Role Model Profile
class RoleModelView(APIView):
  def get(self, request):
      users = CustomUser.objects.all()
      serializer = RoleModelSerializer(users, many=True)
      return Response(serializer.data)

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
  def get(self, request):
      users = CustomUser.objects.all()
      serializer = CommunityUserSerializer(users, many=True)
      return Response(serializer.data)

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

<<<<<<< HEAD
  def get(self, request, pk):
      user = self.get_object(pk)
      serializer = CustomUserSerializer(user)
      return Response(serializer.data)
  


class CommunityUserList(APIView):
    permission_classes = [IsPublicOrReadOnly]
# I need to test community user being filtered by user type
    def get(self, request):
        community_users = CustomUser.objects.filter(user_type=CustomUser.USER_TYPES["COMMUNITY_USER"])
        serializer = CommunityUserSerializer(community_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommunityUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type=CustomUser.USER_TYPES["COMMUNITY_USER"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityUserDetail(APIView):
    permission_classes = [IsCommunityUser]

    def get_object(self, pk):
        try:
            obj = CustomUser.objects.get(pk=pk, user_type=CustomUser.USER_TYPES["COMMUNITY_USER"])
            self.check_object_permissions(self.request, obj)
            return obj
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        community_user = self.get_object(pk)
        serializer = CommunityUserSerializer(community_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        community_user = self.get_object(pk)
        serializer = CommunityUserSerializer(community_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        community_user = self.get_object(pk)
        community_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
=======
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
  





>>>>>>> b757c48fcc435bd2a6be40ffff872e919a056ecf
