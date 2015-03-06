from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login

from account.models import BaseUser, UserManager


class LoginForm(forms.Form):
    username = forms.EmailField(label=_("Email Address"))
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def authenticate(self, request):
        if self.is_valid():
            try:
                user = BaseUser.objects.get(email=self.cleaned_data['username'],
                                            type__in=(UserManager.UT_OWNER, UserManager.UT_BOK))
                self.user = authenticate(username=user.email, password=self.cleaned_data['password'])
                if self.user:
                    login(request, self.user)
            except:
                pass

            if not self.user:
                self.custom_errors.append("Invalid user name or password")
        return self.user