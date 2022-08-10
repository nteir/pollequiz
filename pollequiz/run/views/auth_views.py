from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from pollequiz.run.models import QuizTake, QuizTakeLog
from pollequiz.quiz.models import Quiz
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class ResultsListForAuthors(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = QuizTake
    template_name = "run/takes_list.html"
    context_object_name = 'objects'
    redirect_url = reverse_lazy('users:login')

    def get_queryset(self):
        quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        qs = super().get_queryset()
        qs = qs.filter(quiz=quiz)
        return qs

    def test_func(self):
        quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return self.request.user == quiz.author


class ResultsForAuthors(TemplateView):
    template_name = "run/take_detail.html"

    def get_context_data(self, **kwargs):
        take = QuizTake.objects.get(id=self.kwargs['pk'])
        # quiz = take.quiz

        log = QuizTakeLog.objects.filter(take_id=self.kwargs['pk']).select_related('q_id', 'a_id')

        context = super().get_context_data(**kwargs)
        context['take'] = take
        context['log'] = log
        return context
