from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserLoginForm
from .views import RegisterView, UserProfileView, UserUpdateView, email_verification
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
]
