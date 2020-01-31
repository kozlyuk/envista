from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput(attrs={'class': 'form-control'}), strip=False)

    class Meta:
        model = User
        fields = ('email', 'mobile_number', 'password1', 'password2', 'is_active')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error('email', _("User with such email already exist"))
        return cleaned_data


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'mobile_number', 'is_active')
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': ' form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error('email', _("User with such email already exist"))
        return cleaned_data

    password = ReadOnlyPasswordHashField(label= _("Password"),
            help_text= _("Raw passwords are not stored, so there is no way to see "
                        "this user's password, but you can change the password "
                        "using <a href=\"../password/\">this form</a>."))
