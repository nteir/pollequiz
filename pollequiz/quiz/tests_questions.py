from django.test import TestCase
from pollequiz.quiz.models import Question
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class QuestionTestCase(TestCase):

    fixtures = ['quiz.json', 'question.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.model = Question
        self.object = self.model.objects.get(pk=1)
        self.object_list = self.model.objects.all().order_by('q_number')
        self.context_name = 'objects'
        self.new_data = {
            'q_number': 100,
            'q_type': 'sing',
            'text': 'new test item',
            'points': 0,
        }

    def test_list_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:quiz_card', kwargs={'quiz_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_list = self.object_list.filter(quiz=1)
        self.assertQuerysetEqual(response.context[self.context_name], expected_list)

    def test_create_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:question_new', kwargs={'quiz_id': 1})
        response = self.client.post(url, self.new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(**self.new_data).count(), 1)

    def test_update_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:question_update', kwargs={'quiz_id': self.object.quiz.id, 'pk': self.object.id})
        response = self.client.post(url, self.new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(**self.new_data).count(), 1)

    def test_status_delete(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:question_delete', kwargs={'quiz_id': self.object.quiz.id, 'pk': self.object.id})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(id=self.object.id).count(), 0)
