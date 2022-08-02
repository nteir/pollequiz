from django.contrib.auth.mixins import AccessMixin
from django.views.generic.base import ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from pollequiz.quiz.models import Quiz, Question


class FailedAccessMixin(AccessMixin):
    """
    Overrides handle_no_permission to redirect
    instead of sending err code response.
    """
    redirect_url = ''

    def handle_no_permission(self):
        return redirect(self.redirect_url)


class PQFormContextMixin(ContextMixin):
    """
    Adds title and button text to forms,
    and some other situational context elements.
    """
    title_text = ''
    btn_text = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_text
        context['button_text'] = self.btn_text
        if self.kwargs.get('q_id'):
            context['subtitle'] = Question.objects.get(id=self.kwargs['q_id']).text
        return context


class PQQuerySetMixin(MultipleObjectMixin):
    """
    Get the list of quiz questions or one question's
    answers for a quiz created by current user.
    """
    def get_queryset(self):
        if self.kwargs.get('quiz_id') is None:
            return []
        author = Quiz.objects.get(id=self.kwargs['quiz_id']).author
        if self.request.user != author:
            return []
        queryset = super().get_queryset()
        if self.kwargs.get('q_id'):
            queryset = queryset.filter(question=self.kwargs['q_id'])
        else:
            queryset = queryset.filter(quiz=self.kwargs['quiz_id'])
        return queryset


class PQUserTestMixin(UserPassesTestMixin):
    """
    See that the current user is the author
    of selected quiz.
    """
    def test_func(self):
        if self.kwargs.get('quiz_id'):
            author = Quiz.objects.get(id=self.kwargs['quiz_id']).author
            return self.request.user == author
        else:
            return False


class PQSuccessRedirectMixin(SingleObjectMixin):
    """
    Form redirect url for Answer edit views.
    """
    def get_success_url(self):
        return reverse_lazy(
            'quiz:question_card',
            kwargs={'quiz_id': self.object.question.quiz_id, 'q_id': self.object.question.id}
        )
