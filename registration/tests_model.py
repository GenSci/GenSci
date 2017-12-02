from django.test import TestCase
from registration.models import UserReg
"""
Test_models.py - This file contains class and functions to test the proper functioning of the models in the registration application.
"""

class TestRegister(TestCase):
    """
    Testing whether our application will allow users to register for 'Go Live' notifications.
    """
    user = {'name': 'John Doe', 'email': 'jdo@boringname.net'}

    def test_register_name(self):
        UserReg.objects.create(name=self.user['name'], email=self.user['email'])
        rec = UserReg.objects.first()
        self.assertEqual(self.user['name'], rec.name)
