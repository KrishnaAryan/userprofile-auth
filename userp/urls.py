
from django.urls import path
from .views import *
urlpatterns = [
   path('register/',UserRegistrationView.as_view(),name='register'),
   path('login/',UserLoginView.as_view(),name='login'),
   path('profile/',UserProfileView.as_view(),name='profile'),
   path('change-password/',UserChangePasswordView.as_view(),name='change-password'),
   path('send-link-reset-password/',SendPasswordEmailView.as_view(),name='change-password'),
   path('password-reset/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),
]

