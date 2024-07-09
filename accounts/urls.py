from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CreateUserView, LoginUserView, UserView


urlpatterns = [
    path('register', CreateUserView.as_view(), name='create_user'),
    path('login', LoginUserView.as_view(), name='login'),
    path('user/<int:pk>', UserView.as_view(), name='get_user'),
]
