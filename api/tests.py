from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import status
from .models import Tutorial
from .serializer import TutorialSerializer
from model_bakery import baker


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



## Test Cases for Viewsets

class TutorialApiTest(APITestCase):
    def test_tutorial_list_view(self):
        self.list_url = reverse('tutorialList-list')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tutorials = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorials, many=True)
        self.assertEqual(response.data, serializer.data)


class TutorialViewsetTest(APITestCase):
    def setUp(self):
        # Create a user for authenticated tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some tutorial instances for testing using model_bakery
        self.tutorial1 = baker.make(Tutorial, title='Tutorial 1', content='Content 1')
        self.tutorial2 = baker.make(Tutorial, title='Tutorial 2', content='Content 2')

        # Urls for the viewsets
        self.list_url = reverse('tutorialList-list')
        self.detail_url = reverse('tutorialDetail-list')

    def authenticate(self):
        self.client.login(username='testuser', password='testpassword')

    def test_tutorial_list_view(self):
        # Test that unauthenticated users can access the list
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test the data returned
        tutorials = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorials, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_tutorial_viewset_list_unauthenticated(self):
        # Test that unauthenticated users cannot access the viewset list
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tutorial(self):
        self.authenticate()
        data = {'tutorialNo': 3, 'title': 'Tutorial 3', 'content': 'Content 3'}

        response = self.client.post(self.detail_url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutorial.objects.count(), 3)

    def test_update_tutorial_authenticated(self):
        self.authenticate()

        url = reverse('tutorialDetail-detail', kwargs={'pk': self.tutorial1.pk})
        data = {'tutorialNo': 1, 'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tutorial1.refresh_from_db()
        self.assertEqual(self.tutorial1.title, 'Updated Title')
        self.assertEqual(self.tutorial1.content, 'Updated Content')

    def test_delete_tutorial_authenticated(self):
        self.authenticate()

        url = reverse('tutorialDetail-detail', kwargs={'pk': self.tutorial1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tutorial.objects.count(), 1)




