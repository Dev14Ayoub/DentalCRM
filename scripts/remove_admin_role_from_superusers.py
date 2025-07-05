#!/usr/bin/env python3
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from administrator.models import UserRole, Role

def remove_admin_role_from_superusers():
    admin_role = Role.objects.filter(name='administrator').first()
    if not admin_role:
        print("Administrator role not found.")
        return

    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        user_roles = UserRole.objects.filter(user=user, role=admin_role)
        if user_roles.exists():
            user_roles.delete()
            print(f"Removed administrator role from superuser: {user.username}")
        else:
            print(f"Superuser {user.username} does not have administrator role assigned.")

if __name__ == '__main__':
    remove_admin_role_from_superusers()
