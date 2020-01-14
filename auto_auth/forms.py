# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from auto_auth.models import UserActivationKey

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username",)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            _("A user with that email already exists."))

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])

        if User.objects.filter(is_superuser=True).count() == 0:
            user.is_superuser = True

        if commit:
            user.save()
            # initiate_user_with_default_setups(user)
        return user

    def set_activation_key(self):
        return UserActivationKey.set_random_key_for_user(user=self.instance)
