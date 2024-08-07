# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check_auth/', views.check_auth, name='check_auth'),
]
    # Add other user-related URLs here in the future
