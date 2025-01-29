from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser, Invitation
from .serializers import (
    RoleModelSerializer, 
    CommunityUserSerializer,
    InvitationSerializer
)
from .permissions import IsPublicOrReadOnly, IsRoleModelUser, IsCommunityUser
from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.utils import timezone
import uuid

# from django.urls import path
# from . import views

# urlpatterns = [
# temporary comment out the path to sign up, it's blocking the migration and the block is not defined yet
    # path('signup/', views.SignUpView.as_view(), name='signup'),  # Sign up page 
    # path('login/', views.LoginView.as_view(), name='login'),  # Login page 
    # path('logout/', views.LogoutView.as_view(), name='logout'),  # Logout page
    # path('invite/', views.InviteView.as_view(), name='invite'),  # Invite role model page
#     path('rolemodelprofile/<int:pk>/', views.RoleModelView.as_view(), name='profile'),  # Role Model profile page
#     path('communityuserprofile/<int:pk>/', views.CommunityUserView.as_view(), name='profile'),  # Community User profile page
# ]

# Note:
# We can use the role model profile view to get a list of role models for our role model cards to display on the homepage - no need for a secondary url for 'all users'
# aka = 'rolemodelprofile/<int:pk>/'
# instead of = 'users/'

class FullRoleModelView(APIView):
    #   non register user can only see limited version of role model profile.
    # registered user (including community user and role model users ) can see full details of profile
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Check for invitation token
        token = request.query_params.get('token')
        if token:
            try:
                invitation = Invitation.objects.get(token=token)
                if invitation.is_expired:
                    return Response({
                        "status": "error",
                        "message": "Invitation has expired"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if invitation.is_accepted:
                    return Response({
                        "status": "error",
                        "message": "Invitation has already been used"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    "status": "success",
                    "data": {
                        "email": invitation.email,
                        "first_name": invitation.full_name.split()[0],
                        "last_name": invitation.full_name.split()[-1] if len(invitation.full_name.split()) > 1 else "",
                        "industry": invitation.industry,
                        "current_role": invitation.current_role
                    }
                })
            except Invitation.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Invalid invitation token"
                }, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response(
                {"error": "You need to log in to see full details."},
                status=status.HTTP_403_FORBIDDEN,
            )
        users = CustomUser.objects.filter(user_type="ROLE_MODEL")
        serializer = RoleModelSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # anyone can sign up
    def post(self, request):
        token = request.data.get('invitation_token')
        if token:
            try:
                invitation = Invitation.objects.get(token=token)
                if not invitation.is_expired and not invitation.is_accepted:
                    invitation.is_accepted = True
                    invitation.save()
            except Invitation.DoesNotExist:
                pass

        serializer = RoleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="ROLE_MODEL")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PublicRoleModelListView(APIView):
    permission_classes = [IsPublicOrReadOnly]
    
    def get(self, request, pk=None):
        if pk:
            # Fetch and return limited details for a single role model profile
            try:
                user = CustomUser.objects.get(pk=pk, user_type="ROLE_MODEL")
            except CustomUser.DoesNotExist:
                raise Http404
            limited_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "image": user.image,
                "current_role": user.current_role,
                "industry": user.industry,  
                "location": user.location,  
                "skills": user.skills,  
            }
            return Response(limited_data, status=status.HTTP_200_OK)
        else:
            # Fetch and return the list of all role models 
            users = CustomUser.objects.filter(user_type="ROLE_MODEL").only(
                'first_name', 'last_name', 'image', 'current_role'
            )
            data = [
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "image": user.image,
                    "current_role": user.current_role,
                    "location": user.location,
                    # "industry": user.industry,  
                    # "skills": user.skills  
                }
                for user in users
            ]
            return Response(data, status=status.HTTP_200_OK)

class SendInvitationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # First just try to save the invitation
                invitation = serializer.save()
                
                # Add debug logging
                print("Invitation saved successfully:", invitation.id)
                
                try:
                    signup_link = f"{settings.FRONTEND_URL}/role-model/signup/?token={invitation.token}"
                    
                    # Debug print
                    print("Signup link generated:", signup_link)

                    subject = "You're Invited to Join as a Role Model!"
                    html_content = f"""
                        <h2>Hello {invitation.full_name}!</h2>
                        <p>Someone thinks you would be a great role model on our platform.</p>
                        <p>Why they think you're inspiring:</p>
                        <p>{invitation.why_inspiring}</p>
                        <p>Click the button below to create your role model account:</p>
                        <a href="{signup_link}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">Create Your Account</a>
                        <p>Link expires in 7 days.</p>
                    """
                    
                    plain_message = strip_tags(html_content)
                    
                    # Debug print before sending email
                    print("Attempting to send email to:", invitation.email)

                    # For testing, first check if email settings are configured
                    print("Email settings:", {
                        "backend": settings.EMAIL_BACKEND,
                        "host": settings.EMAIL_HOST,
                        "port": settings.EMAIL_PORT,
                        "use_tls": settings.EMAIL_USE_TLS,
                        "from_email": settings.DEFAULT_FROM_EMAIL,
                    })

                    send_mail(
                        subject=subject,
                        message=plain_message,
                        html_message=html_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[invitation.email],
                        fail_silently=False,
                    )

                    return Response({
                        "status": "success",
                        "message": "Invitation sent successfully"
                    }, status=status.HTTP_201_CREATED)

                except Exception as email_error:
                    # Log the specific email error
                    print("Email error:", str(email_error))
                    return Response({
                        "status": "error",
                        "message": f"Failed to send email: {str(email_error)}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                # Log any other errors
                print("General error:", str(e))
                return Response({
                    "status": "error",
                    "message": "Failed to send invitation. Please try again."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

class CommunityUserView(APIView):
    #   each communti user can view their own profile, 
    #   only role models can see every community user profile 
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "You need to log in to see this data."},
                status=status.HTTP_403_FORBIDDEN,
            )
        users = CustomUser.objects.filter(user_type="COMMUNITY_USER")
        serializer = CommunityUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Allow unauthenticated users to sign up
        serializer = CommunityUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="COMMUNITY_USER")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class CustomUserDetail(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

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