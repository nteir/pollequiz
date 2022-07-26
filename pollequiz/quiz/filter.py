import django_filters
from django import forms
from pollequiz.quiz.models import Quiz


class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = ['name', 'author', 'is_poll']


class MyQuizFilter(QuizFilter):
    self_tasks = django_filters.filters.BooleanFilter(
        widget=forms.CheckboxInput(),
        method='get_my_quizes',
    )

    def get_my_quizes(self, queryset, name, value):
        author = getattr(self.request, "user", None)
        queryset = queryset.filter(author=author)
        return queryset
