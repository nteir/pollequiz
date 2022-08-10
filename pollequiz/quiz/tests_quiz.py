from django.test import TestCase
from pollequiz.quiz.models import Quiz
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class QuizTestCase(TestCase):

    fixtures = ['quiz.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.model = Quiz
        self.object = self.model.objects.get(pk=1)
        self.object_list = self.model.objects.all().order_by('-modified_at')
        self.context_name = 'objects'
        self.new_data = {
            'name': 'tquiz',
            'is_poll': False,
            'description': 'test description',
        }

    def test_list_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:list_all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context[self.context_name], self.object_list)

    def test_create_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:new')
        response = self.client.post(url, self.new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(**self.new_data).count(), 1)

    def test_update_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:quiz_update', kwargs={'pk': self.object.id})
        response = self.client.post(url, self.new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(**self.new_data).count(), 1)

    def test_status_delete(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:quiz_delete', kwargs={'pk': self.object.id})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(id=self.object.id).count(), 0)
