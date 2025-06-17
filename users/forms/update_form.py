from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.django_forms import add_placeholder


class UpdateForm(forms.ModelForm):
    photo = forms.ImageField(
        required=False,
        label=_('Profile Photo'),
        help_text=_('Upload a profile photo'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], _('Enter your first name'))
        add_placeholder(self.fields['last_name'], _('Enter your last name'))
        add_placeholder(self.fields['email'], _('email@address.com'))
        add_placeholder(self.fields['username'], _('Enter a username'))
        add_placeholder(self.fields['phone_number'], _('2499999999'))

    first_name = forms.CharField(
        error_messages={
            'required': _('First name cannot be empty'),
        },
        required=True,
        label=_('First Name'),
    )
    last_name = forms.CharField(
        error_messages={
            'required': _('Last name cannot be empty'),
        },
        required=True,
        label=_('Last Name'),
    )
    email = forms.EmailField(
        error_messages={
            'required': _('Email is required'),
            'invalid': _('The email must be valid'),
        },
        required=True,
        label=_('Email'),
        help_text=_('Enter a valid email'),
    )
    username = forms.CharField(
        label=_('Username'),
        help_text=_('Username must have letters, numbers or symbols. '
                    'The length should be between 4 and 150 characters.'),
        error_messages={
            'required': _('Username is required'),
            'min_length': _('Username must have at least 4 characters'),
            'max_length': _('Username must have 150 characters or less'),
        },
        min_length=4, max_length=150,
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        required=False,
        error_messages={
            'invalid': _('The phone number provided is invalid'),
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'photo',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if exists:
            raise ValidationError(
                _('User email is already in use'), code='unique'
            )
        return email

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if 'admin' in data:
            raise ValidationError(
                _('Forbidden username'),
                code='invalid',
            )
        return data
