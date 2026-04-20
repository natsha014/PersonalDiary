from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm
from .models import User
from django.contrib.auth import login


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('diary:note_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
