from django.test import TestCase
from pollequiz.quiz.models import Answer
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class AnswerTestCase(TestCase):

    fixtures = ['quiz.json', 'question.json', 'answer.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.model = Answer
        self.object = self.model.objects.get(pk=1)
        self.object_list = self.model.objects.all().order_by('a_number')
        self.context_name = 'objects'
        self.new_data = {
            'a_number': 100,
            'text': 'new test item',
            'correct': False,
        }

    def test_list_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:question_card', kwargs={'quiz_id': 1, 'q_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_list = self.object_list.filter(question=1)
        self.assertQuerysetEqual(response.context[self.context_name], expected_list)

    def test_create_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy('quiz:answer_new', kwargs={'quiz_id': 1, 'q_id': 1})
        response = self.client.post(url, self.new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(**self.new_data).count(), 1)

    def test_update_view(self):
        self.client.force_login(self.user)
        url = reverse_lazy(
            'quiz:answer_update',
            kwargs={'quiz_id': self.object.question.quiz.id, 'q_id': self.object.question.id, 'pk': self.object.id}
        )
        response = self.client.post(url, self.new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(**self.new_data).count(), 1)

    def test_status_delete(self):
        self.client.force_login(self.user)
        url = reverse_lazy(
            'quiz:answer_delete',
            kwargs={'quiz_id': self.object.question.quiz.id, 'q_id': self.object.question.id, 'pk': self.object.id}
        )
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model.objects.filter(id=self.object.id).count(), 0)
