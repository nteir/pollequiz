# from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from django_filters.views import FilterView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pollequiz.quiz.models import Quiz, Question
from pollequiz.quiz.forms import QuestionForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
import pollequiz.pq_objects as pq_objects
import pollequiz.text_constants as txt

User = get_user_model()


class QuestionsListView(pq_objects.FailedAccessMixin, LoginRequiredMixin, ListView):
    model = Question
    ordering = ['q_number']
    redirect_url = reverse_lazy('users:login')
    template_name = 'quiz/quiz_questions.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['quiz_id']:
            context['quiz'] = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return context

    def get_queryset(self):
        if self.kwargs['quiz_id']:
            author = Quiz.objects.get(id=self.kwargs['quiz_id']).author
            if self.request.user != author:
                return []
            qset = Question.objects.filter(quiz=self.kwargs['quiz_id']).order_by('q_number')
            return qset
        return []


class QuestionCreateView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    CreateView
):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('users:login')
    title_text = txt.CREATE_QUIZ_TITLE
    btn_text = txt.CREATE_BTN

    def get_success_url(self):
        return reverse_lazy('quiz:quiz_card', kwargs={'pk': self.object.quiz.id})

    def form_valid(self, form):
        form.instance.quiz_id = self.kwargs['quiz_id']
        return super().form_valid(form)
