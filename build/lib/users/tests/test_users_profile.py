from django.test import TestCase

from tests.mixins import ProfileMixin, TestAssertionsMixin


class UserProfileTest(TestCase, ProfileMixin, TestAssertionsMixin):
    def test_profile_extra_info_goes_to_user_correctly(self):
        user = self.make_user(phone_number='2199999998')
        self.assertEqual(user.profile.phone_number, '2199999998')
