from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from config import settings
from .forms import UserRegisterForm, UserProfileForm
from .models import User
from django.core.mail import send_mail
import secrets
from django.contrib import messages


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True
        )

        messages.success(self.request,
                         'Регистрация почти завершена! Мы отправили письмо для подтверждения на вашу почту.')
        return super().form_valid(form)


def email_verification(request, token):
    users = get_object_or_404(User, token=token)
    users.is_active = True
    users.save()
    messages.success(request, 'Ваша почта успешно подтверждена! Теперь вы можете войти в систему.')
    return redirect(reverse("users:login"))


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
