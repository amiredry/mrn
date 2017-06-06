__author__ = 'ShadowTrader'
from django import forms
from models import UserProfile, User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from django.utils.translation import ugettext, ugettext_lazy as _


class UserProfileForm(forms.ModelForm):

    captcha = CaptchaField()

    class Meta:
        model = UserProfile
        exclude = ('user', 'activation_key')


class ExtendedUserCreationForm(UserCreationForm):

    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                    "@/./+/-/_ characters.")})

    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
