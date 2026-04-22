from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)


class UserLoginForm(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get('username') or self.data.get('username')

        if email:
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                raise forms.ValidationError(
                    "Пользователь с такой почтой не найден. Пожалуйста, зарегистрируйтесь!"
                )
        return super().clean()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'avatar', 'country')
