from django.test import TestCase
from django.contrib import auth
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class UsersTestCase(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user_list = [self.user1, self.user2]

    def test_user_create(self):
        new_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'tuser',
            'email': 'test@test.com',
            'password1': 'qwerty78',
            'password2': 'qwerty78',
        }
        url = reverse_lazy('users:signup')
        response = self.client.post(url, new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        test_object = User.objects.filter(username='tuser')
        self.assertEqual(test_object.count(), 1)
        current_user = auth.get_user(self.client)
        self.assertEqual(current_user, test_object.get())

    def test_user_update(self):
        user = self.user1
        self.client.force_login(user)
        url = reverse_lazy('users:profile', kwargs={'pk': user.id})
        new_data = {
            'first_name': user.first_name,
            'last_name': 'Sidorov',
            'username': user.username,
            'email': user.email,
            'password1': user.password,
            'password2': user.password,
        }
        response = self.client.post(url, new_data, follow=True)
        self.assertRedirects(response, reverse_lazy('home'))
        test_object = User.objects.filter(last_name='Sidorov')
        self.assertEqual(test_object.count(), 1)
        current_user = auth.get_user(self.client)
        self.assertEqual(current_user, test_object.get())
