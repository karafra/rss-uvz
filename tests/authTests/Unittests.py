from unittest import mock
from django.contrib import auth
from uvz.auth.functions import generate_auth_token
from unittest import TestCase
class AuthTests(TestCase):

    def test_test(self):
        # Given 
        auth.authenticate = mock.Mock(return_value="")
        username = "username"
        password = "password"
        # When 
        response = generate_auth_token(username, password)
        # Then
        self.assertEqual(response, "")