from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.django_forms import add_placeholder


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label=_('New Password'),
        help_text=_(
            'Password must contain at least one uppercase character, '
            'one lowercase character and one number. The length should be '
            'at least 8 characters.'
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label=_('Repeat New Password'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['password'], _('Enter your new password'))
        add_placeholder(self.fields['password2'], _('Repeat your new password'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError(_('Passwords must match'), code='invalid')
        return cleaned_data
