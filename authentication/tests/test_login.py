from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from utils import constants

from . import create_user_data, login_credentials


class LoginTest(APITestCase):
    url = reverse('authentication:login')

    def setUp(self):
        User.objects.create_user(**create_user_data)

    def test_get(self):
        """
        Get requests not allowed
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_username(self):
        """
        Check response message when username is not included in API request
        """
        # Remove the username field in the request
        _login_credentials = login_credentials.copy()
        del _login_credentials['username']
        # Client sends a POST request with the credentials
        response = self.client.post(self.url, _login_credentials, format='json')
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # An error response message is expected
        self.assertIn(constants.AUTH_ERROR, response.json()['error'])

    def test_no_password(self):
        """
        Check response message when password is not included in API request
        """
        # Remove the username field in the request
        _login_credentials = login_credentials.copy()
        del _login_credentials['password']
        # Client sends a POST request with the credentials
        response = self.client.post(self.url, _login_credentials, format='json')
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # An error response message is expected
        self.assertIn(constants.AUTH_ERROR, response.json()['error'])

    def test_login(self):
        """
        Login the user
        """
        # Client sends a POST request with the credentials
        response = self.client.post(self.url, login_credentials, format='json')
        # Status Code returned by the API must be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Token must be returned in a successful registration
        token = response.data.get('token', None)
        self.assertNotEqual(token, None)

    def test_login_with_wrong_credentials(self):
        """
        Login the user
        """
        _login_credentials = login_credentials.copy()
        _login_credentials['password'] =  'pass5678'
        # Client sends a POST request with the credentials
        response = self.client.post(self.url, _login_credentials, format='json')
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # An error response message is expected
        self.assertIn(constants.AUTH_ERROR, response.json()['error'])


class SetLogin(APITestCase):

    def setUp(self):
        """
        Login the user
        """
        User.objects.create_user(**create_user_data)
        response = self.client.post(LoginTest.url,
                                    login_credentials,
                                    format='json')
        token = response.data['token']
        return token