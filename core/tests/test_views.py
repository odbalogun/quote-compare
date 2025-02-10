from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Country


class CountryListViewTests(APITestCase):
    def setUp(self):
        super().setUp()
        Country.objects.create(name="Test Country", code="TC", nationality="Test Nationality")

    def test_get_countries(self):
        url = reverse('country-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Country")

class CreateUserViewTests(APITestCase):
    def test_create_user(self):
        url = reverse('register-user')
        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")

class EditUserProfileViewTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_edit_user_profile(self):
        url = reverse('edit-user-profile', kwargs={'pk': self.user.pk})
        data = {
            "first_name": "Updated",
            "last_name": "User"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")

class FetchAllUsersViewTests(APITestCase):
    def setUp(self):
        super().setUp()
        User.objects.create_user(email="test1@example.com", password="testpassword")
        User.objects.create_user(email="test2@example.com", password="testpassword")

    def test_get_all_users(self):
        url = reverse('fetch-all-users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

# class RequestPasswordResetTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email="test@example.com", password="testpassword")

#     def test_request_password_reset(self):
#         url = reverse('request-password-reset')
#         data = {"email": "test@example.com"}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)