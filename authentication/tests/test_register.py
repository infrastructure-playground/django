from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from utils import constants

from . import create_user_data, registration_data


# Create your tests here.
class RegistrationTest(APITestCase):
    url = reverse('authentication:registration')

    def test_get(self):
        """
        Get requests not allowed
        """
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_no_username(self):
        """
        Check response message when username is not included in API request
        """
        # Remove the username field in the request
        _registration_data = registration_data.copy()
        del _registration_data['username']
        response = self.client.post(
            self.url, _registration_data, format='json'
        )
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # A response message of “This field is required” on username key
        self.assertIn('This field is required', response.json()['username'][0])

    def test_no_password(self):
        """
        Check response message when password is not included in API request
        """
        # Remove the password field in the request
        _registration_data = registration_data.copy()
        del _registration_data['password']
        response = self.client.post(
            self.url, _registration_data, format='json'
        )
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # A response message of “This field is required” on password key
        self.assertIn('This field is required', response.json()['password'][0])

    def test_no_confirm_password(self):
        """
        Check response message when confirm password is not included in API request
        """
        # Remove the password field in the request
        _registration_data = registration_data.copy()
        del _registration_data['confirm_password']
        response = self.client.post(
            self.url, _registration_data, format='json'
        )
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # A response message of “This field is required” on confirm_password key
        self.assertIn(
            constants.ERROR_PASSWORD_CONFIRMATION, response.json()['error']
        )

    def test_diff_ERROR_PASSWORD_CONFIRMATION(self):
        """
        Check response message when confirmed password is not the same as password in API request
        """
        # Remove the password field in the request
        _registration_data = registration_data.copy()
        _registration_data['confirm_password'] = 'pass5678'
        response = self.client.post(
            self.url, _registration_data, format='json'
        )
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # A response message of “This field is required” on confirm_password key
        self.assertIn(
            constants.ERROR_PASSWORD_CONFIRMATION, response.json()['error']
        )

    def test_register(self):
        """
        Check response message when valid registration data is entered
        """
        # Client sends a POST request with the input data
        response = self.client.post(self.url, registration_data, format='json')
        # A new User must be created in the database
        self.assertEqual(User.objects.filter(username='armadadean').count(), 1)
        # Status Code returned by the API must be 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Token must be returned in a successful registration
        token = response.data.get('token', None)
        self.assertNotEqual(token, None)

    def test_register_existing_username(self):
        """
        Check response message when existing username
        """
        # Create a username
        User.objects.create_user(**create_user_data)
        # Client sends a POST request with the input data
        response = self.client.post(self.url, registration_data, format='json')
        # Status Code returned by the API must be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'username already exists', response.json()['username'][0]
        )
