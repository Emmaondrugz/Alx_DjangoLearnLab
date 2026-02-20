from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegistraionView, FollowUserView, UnfollowUserView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("register/", RegistraionView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("follow/<int:user_id>", FollowUserView.as_view()),
    path("unfollow/<int:user_id>", UnfollowUserView.as_view())
]