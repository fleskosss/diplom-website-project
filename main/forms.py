from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import LeadRequest, UserProfile


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'пароль'})
    )


class AdminProfileForm(forms.Form):
    avatar = forms.ImageField(required=False, label='Аватар')
    first_name = forms.CharField(max_length=150, required=False, label='Имя')
    email = forms.EmailField(required=False, label='Эл. почта')
    password = forms.CharField(
        required=False,
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Новый пароль'})
    )
    password_confirm = forms.CharField(
        required=False,
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')

        return cleaned_data

    def save(self, user):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        avatar = self.cleaned_data.get('avatar')
        first_name = self.cleaned_data.get('first_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if avatar:
            profile.avatar = avatar
            profile.save()

        if first_name is not None:
            user.first_name = first_name
        if email is not None:
            user.email = email
        if password:
            user.set_password(password)
        user.save()


class LeadRequestForm(forms.Form):
    question = forms.CharField(max_length=2000)
    phone = forms.CharField(max_length=40)
    consent = forms.BooleanField(required=True)

    def save(self, source):
        return LeadRequest.objects.create(
            source=source,
            question=self.cleaned_data['question'],
            phone=self.cleaned_data['phone'],
        )
