from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Create Profile objects for users without one'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        count = users_without_profile.count()
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(f'Created profile for user: {user.username}')
        self.stdout.write(self.style.SUCCESS(f'Created {count} profiles for users without one.'))
