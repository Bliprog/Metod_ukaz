from django.contrib.auth.forms import *
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
class CreateUserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),
    }
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Придумайте свой пароль",
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Введите пароль повторно"),
    )

    class Meta:
        model = User
        fields = ("username",'email','first_name','last_name')
        field_classes = {'username': UsernameField,
                         'email': forms.EmailField,
                         'first_name': forms.CharField,
                         'last_name': forms.CharField}

class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('otchestvo',)
        field_classes = {'otchestvo': forms.CharField}



class DateForm(forms.Form):
    date_start = forms.DateField(label='Начальная дата', widget=forms.DateInput)
    date_end = forms.DateField(label='Дата окончания', widget=forms.DateInput)