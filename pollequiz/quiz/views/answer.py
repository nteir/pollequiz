from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from pollequiz.quiz.models import Quiz, Question, Answer
# from pollequiz.quiz.forms import AnswerForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
import pollequiz.pq_objects as pq_objects
# import pollequiz.text_constants as txt

User = get_user_model()


class AnswerListView(pq_objects.FailedAccessMixin, LoginRequiredMixin, ListView):
    model = Answer
    ordering = ['a_number']
    redirect_url = reverse_lazy('users:login')
    template_name = 'quiz/quiz_answers.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['quiz_id']:
            context['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if self.kwargs['q_id']:
            context['question'] = Question.objects.get(id=self.kwargs['q_id'])
        return context

    def get_queryset(self):
        if self.kwargs['quiz_id'] and self.kwargs['q_id']:
            author = Quiz.objects.get(id=self.kwargs['quiz_id']).author
            if self.request.user != author:
                return []
            qset = Answer.objects.filter(question=self.kwargs['q_id']).order_by('a_number')
            return qset
        return []
