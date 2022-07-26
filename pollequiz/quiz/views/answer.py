from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from pollequiz.quiz.models import Quiz, Question, Answer
from pollequiz.quiz.forms import AnswerForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
import pollequiz.pq_objects as pq_objects
import pollequiz.text_constants as txt

User = get_user_model()


class AnswerListView(pq_objects.FailedAccessMixin, pq_objects.PQQuerySetMixin, LoginRequiredMixin, ListView):
    model = Answer
    ordering = ['a_number']
    redirect_url = reverse_lazy('users:login')
    template_name = 'quiz/quiz_answers.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('quiz_id'):
            context['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if self.kwargs.get('q_id'):
            context['question'] = Question.objects.get(id=self.kwargs['q_id'])
        return context


class AnswerCreateView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    pq_objects.PQSuccessRedirectMixin,
    CreateView
):
    model = Answer
    form_class = AnswerForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('users:login')
    title_text = txt.CREATE_ANSWER_TITLE
    btn_text = txt.CREATE_BTN

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['q_id']
        return super().form_valid(form)


class AnswerUpdateView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    pq_objects.PQUserTestMixin,
    pq_objects.PQSuccessRedirectMixin,
    UpdateView
):
    model = Answer
    form_class = AnswerForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('users:login')
    title_text = txt.UPDATE_ANSWER_TITLE
    btn_text = txt.UPDATE_BTN


class AnswerDeleteView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    pq_objects.PQUserTestMixin,
    pq_objects.PQSuccessRedirectMixin,
    DeleteView
):
    model = Answer
    template_name = "quiz/delete.html"
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('quiz:list_my')
    title_text = txt.DELETE_ANSWER_TITLE
    btn_text = txt.DELETE_BTN
