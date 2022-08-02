from django.contrib.auth.mixins import AccessMixin
from django.views.generic.base import ContextMixin
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import redirect
from pollequiz.quiz.models import Quiz


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
    Adds title and button text to forms.
    """
    title_text = ''
    btn_text = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_text
        context['button_text'] = self.btn_text
        return context


class PQQuerySetMixin(MultipleObjectMixin):
    """
    Get the list of quiz questions or one question's
    answers for a quiz created by current user.
    """
    def get_queryset(self):
        if self.kwargs.get('quiz_id'):
            author = Quiz.objects.get(id=self.kwargs['quiz_id']).author
            if self.request.user != author:
                return []
            queryset = super().get_queryset()
            if self.kwargs.get('q_id'):
                queryset = queryset.filter(question=self.kwargs['q_id'])
            else:
                queryset = queryset.filter(quiz=self.kwargs['quiz_id'])
            return queryset
        return []
