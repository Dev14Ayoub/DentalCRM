from django.core.management.base import BaseCommand
from administrator.models import Role, Permission, RolePermission

class Command(BaseCommand):
    help = 'Assign all permissions to the administrator role'

    def handle(self, *args, **options):
        admin_role, created = Role.objects.get_or_create(name='administrator')
        all_permissions = Permission.objects.all()
        assigned_count = 0
        for perm in all_permissions:
            rp, created = RolePermission.objects.get_or_create(role=admin_role, permission=perm)
            if created:
                assigned_count += 1
        self.stdout.write(self.style.SUCCESS(f'Assigned {assigned_count} permissions to administrator role.'))
