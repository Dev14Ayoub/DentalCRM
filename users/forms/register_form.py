from string import ascii_letters as letters

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], _('Enter your first name'))
        add_placeholder(self.fields['last_name'], _('Enter your last name'))
        add_placeholder(self.fields['email'], _('email@address.com'))
        add_placeholder(self.fields['username'], _('Enter a username'))
        
        add_placeholder(self.fields['phone_number'], _('2499999999'))
        add_placeholder(self.fields['password'], _('Enter your password'))
        add_placeholder(self.fields['password2'],
                        _('Enter your password again'))

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
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        help_text=_(
            'Password must contain at least one uppercase character, '
            'one lowercase character and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={
            'required': _('Password must not be empty'),
        },
        validators=[strong_password],
        label=_('Password'),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        validators=[strong_password],
        label=_('Repeat Password'),
        error_messages={
            'required': _('Please repeat your password'),
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
            'password',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                _('User email is already in use'), code='unique'
            )
        return email

    

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        if any(char in phone_number for char in letters):
            raise ValidationError(
                _('The phone number provided is invalid'), code='invalid'
            )
        return phone_number

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if 'admin' in data:
            raise ValidationError(
                _('Forbidden username'),
                code='invalid',
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            password_error = ValidationError(
                _('Passwords must match'),
                code='invalid',
            )
            raise ValidationError({
                'password2': [
                    password_error,
                ],
            })
        return cleaned_data
