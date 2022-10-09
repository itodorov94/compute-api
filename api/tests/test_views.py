"""REST API Test cases"""

import tempfile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class BaseTestCase(APITestCase):
    """
    Base class for defining urls and sample data
    """

    def setUp(self):
        self.register_url = reverse('register')
        self.get_token_url = reverse('api-token-auth')
        self.file_upload_url = reverse('file-upload')
        self.data = {
            'email':'test@test.bg',
            'username': 'testusername',
            'password': 'testpassword123',
            'password_confirmed': 'testpassword123'
        }
        self.tmp_file_no_extension = tempfile.NamedTemporaryFile(suffix = '')
        self.tmp_file_wrong_extension = tempfile.NamedTemporaryFile(suffix = '.xml')


class TestRegisterView(BaseTestCase):
    """
    Class with views test cases
    """

    def test_user_can_register(self):
        """
        Test user can register with valid data provided
        """

        resp = self.client.post(self.register_url, self.data)
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)


    def test_user_cannot_register_with_no_data(self):
        """
        Test user cannot register with no data provided
        """

        resp = self.client.post(self.register_url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_token_request(self):
        """
        Test auth token is returned from API
        """

        # First register user
        self.client.post(self.register_url, self.data)

        resp = self.client.post(self.get_token_url, data={'username': self.data['username'], 'password': self.data['password']}, format='json')
        self.assertIn('token', resp.data)


class TestFileUploadView(BaseTestCase):
    """
    Class with File upload test cases
    """

    def authenticate(self):
        """
        Method to authenticate user needed for upload view
        """
        self.client.post(self.register_url, self.data)
        resp = self.client.post(self.get_token_url, data={'username':self.data['username'], 'password':self.data['password']})
        self.token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)


    def test_requires_authentication(self):
        """
        Test upload view requires authentication
        """

        with open(self.tmp_file_no_extension.name) as fp:
            resp = self.client.post(self.file_upload_url, {'file': fp})

        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_file_without_extension(self):
        """
        Test provided file with no extension
        """

        self.authenticate()
        with open(self.tmp_file_no_extension.name) as fp:
            resp = self.client.post(self.file_upload_url, {'file': fp})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_file_with_wrong_extension(self):
        """
        Test provided file with not supported extension
        """

        self.authenticate()
        with open(self.tmp_file_wrong_extension.name) as fp:
            resp = self.client.post(self.file_upload_url, {'file': fp})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
