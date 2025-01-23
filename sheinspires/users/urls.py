from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),  # Sign up page
    path('login/', views.LoginView.as_view(), name='login'),  # Login page
    path('logout/', views.LogoutView.as_view(), name='logout'),  # Logout page
    path('invite/', views.InviteView.as_view(), name='invite'),  # Invite role model page
    path('rolemodelprofile/<int:pk>/', views.RoleModelView.as_view(), name='profile'),  # Role Model profile page 
    path('communityuserprofile/<int:pk>/', views.CommunityUserView.as_view(), name='profile'),  # Community User profile page
]

# Note:
# We can use the role model profile view to get a list of role models for our role model cards to display on the homepage - no need for a secondary url for 'all users'
# aka = 'rolemodelprofile/<int:pk>/'
# instead of = 'users/'