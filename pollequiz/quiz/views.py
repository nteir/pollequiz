from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from pollequiz.quiz.models import Quiz
from pollequiz.quiz.forms import QuizForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
import pollequiz.pq_objects as pq_objects
import pollequiz.text_constants as txt

User = get_user_model()


# Create your views here.
class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "quiz/quiz_card.html"
    context_object_name = 'quiz'
    redirect_url = reverse_lazy('users:login')


class QuizListView(pq_objects.FailedAccessMixin, LoginRequiredMixin, ListView):
    model = Quiz
    ordering = ['id']
    redirect_url = reverse_lazy('users:login')
    template_name = 'quiz/list.html'
    context_object_name = 'objects'


class QuizCreateView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    CreateView
):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('users:login')
    title_text = txt.CREATE_QUIZ_TITLE
    btn_text = txt.CREATE_BTN

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class QuizUpdateView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('users:login')
    title_text = txt.UPDATE_QUIZ_TITLE
    btn_text = txt.UPDATE_BTN

    def test_func(self):
        return self.request.user == self.get_object().author


class QuizDeleteView(
    pq_objects.FailedAccessMixin,
    pq_objects.PQFormContextMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Quiz
    template_name = "quiz/delete.html"
    success_url = reverse_lazy('quiz:list_my')
    redirect_url = reverse_lazy('quiz:list_my')
    title_text = txt.DELETE_QUIZ_TITLE
    btn_text = txt.DELETE_BTN

    def test_func(self):
        return self.request.user == self.get_object().author
