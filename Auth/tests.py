from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserRoleTests(TestCase):
    def test_role_assignment_updates_role_flags(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='roleuser',
            email='role@example.com',
            password='pass1234'
        )

        user.assign_role('pastor')
        user.save()

        self.assertEqual(user.role, 'pastor')
        self.assertTrue(user.is_pastor)
        self.assertFalse(user.is_treasurer)
