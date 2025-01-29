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


from django.urls import path
from . import views 
from .views import SendInvitationView

urlpatterns = [
    # Role Model Sign-Up and Profile Creation
    path('role-models/', views.FullRoleModelView.as_view(), name='full_role_models'),
    
    # Community User Sign-Up and Profile Creation
    path('community-user/signup/', views.CommunityUserView.as_view(), name='community_user_signup'),
    
    # Public Role Model Profiles (Limited View)
    path('role-models/public/', views.PublicRoleModelListView.as_view(), name='public_role_models'),
    
    # Public Role Model Profiles details (Limited View)
    path('role-models/public/<int:pk>/', views.PublicRoleModelListView.as_view(), name='public_role_model_detail'),
    
    # Role Model Profile Detail (View, Update, Delete)
    path('role-models/<int:pk>/', views.RoleModelDetail.as_view(), name='role_model_detail'),
    
    # Community User Profiles List (For Role Models)
    path('community-users/', views.CommunityUserView.as_view(), name='community_user_list'),
    
    # Community User Profile Detail (View, Update, Delete)
    path('community-users/<int:pk>/', views.CommunityUserDetail.as_view(), name='community_user_detail'),
    
    # Token Authentication (Login/Validate User)
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    
    # Invitations
    path('invitations/send', views.SendInvitationView.as_view(), name='send-invitation'),
    
    # Role Model Signup (with invitation)
    path('role-model/signup/', views.FullRoleModelView.as_view(), name='role_model_signup'),
]