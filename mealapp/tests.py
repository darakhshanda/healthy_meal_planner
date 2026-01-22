import sys
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.test import TestCase


class UserCreationTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser', password='testpass')
        self.assertTrue(User.objects.filter(username='testuser').exists())
