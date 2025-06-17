from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Adds a CSS class to a form field widget.
    Usage: {{ field|add_class:"my-class" }}
    """
    existing_classes = field.field.widget.attrs.get('class', '')
    if existing_classes:
        css_class = existing_classes + ' ' + css_class
    field.field.widget.attrs['class'] = css_class
    return field
