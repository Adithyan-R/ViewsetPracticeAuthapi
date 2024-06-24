from django.test import TestCase

# Create your tests here.


from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import model_bakery


class RegisterApiTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_with_invalid_data(self):
        url = reverse('register')
        data = {
            'username': '',  # Invalid username
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())



class LoginApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')


    def test_login_user_with_valid_data(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post(url,data,format='json')

        self.assertIn('detail', response.data)
        self.assertIn('Login successful', response.data['detail'])

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')







from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tutorial

from .serializer import TutorialSerializer
from django.contrib.auth.models import User


class TutorialApiTest(APITestCase):
    def test_tutorial_list_view(self):
        self.list_url = reverse('tutorialList-list')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tutorials = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorials, many=True)
        self.assertEqual(response.data, serializer.data)






