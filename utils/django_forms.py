import re

from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    # Updated regex to allow any number of lowercase letters, but require at least one uppercase and one number
    regex = re.compile(r'^(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'Password must contain at least one uppercase character, '
            'and at least one number. The length should be at least 8 characters.'
        ),
            code='invalid'
        )
