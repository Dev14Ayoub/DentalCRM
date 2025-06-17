from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserRole, Role

@receiver(post_save, sender=User)
def update_is_staff_on_user_save(sender, instance, created, **kwargs):
    if created:
        # Check if user has administrator role
        admin_role = Role.objects.filter(name='administrator').first()
        if admin_role and UserRole.objects.filter(user=instance, role=admin_role).exists():
            instance.is_staff = True
            instance.save()

@receiver(m2m_changed, sender=User.groups.through)
def update_is_staff_on_role_change(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        admin_role = Role.objects.filter(name='administrator').first()
        if admin_role:
            has_admin_role = UserRole.objects.filter(user=instance, role=admin_role).exists()
            if has_admin_role and not instance.is_staff:
                instance.is_staff = True
                instance.save()
            elif not has_admin_role and instance.is_staff:
                instance.is_staff = False
                instance.save()
