from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
