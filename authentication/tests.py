from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User


registration_data = {'username': 'armadadean',
                     'password': 'pass1234',
                     'confirm_password': 'pass1234',
                     'email': 'armadadean@yahoo.com',
                     'first_name': 'Dean Christian',
                     'last_name': 'Armada'}
create_user_data = registration_data.copy()
del create_user_data['confirm_password']
login_credentials = {'username': 'armadadean', 'password': 'pass1234'}


# Create your tests here.
class RegistrationTest(APITestCase):
    url = reverse('authentication:registration')

    def test_get(self):
        """
        Get requests not allowed
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register(self):
        """
        Registers a new user
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
