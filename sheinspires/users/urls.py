from django.urls import path
from . import views

# urlpatterns = [
#   path('users/', views.CustomUserList.as_view()),
#   path('users/<int:pk>/', views.CustomUserDetail.as_view()),
#   path('signup/', views.UserSignup.as_view(), name='signup'),
#   path('login/', views.UserLogin.as_view(), name='login'),
#   path('invite/', views.UserInvitation.as_view(), name='invite'),
#   path('categories/', views.CategoryList.as_view()),  # List all categories
#   path('skills/', views.SkillList.as_view()),  # List all skills
#  ]

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),  # Sign up page
    path('login/', views.LoginView.as_view(), name='login'),  # Login page
    path('logout/', views.LogoutView.as_view(), name='logout'),  # Logout page
    path('invite/', views.InviteView.as_view(), name='invite'),  # Invite role model page
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),  # User profile page (for both Role Models and Community Users)
]