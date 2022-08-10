import django_filters
from pollequiz.quiz.models import Quiz
import pollequiz.text_constants as txt


class QuizFilter(django_filters.FilterSet):
    POLL_CHOICES = (
        (False, 'Quiz'),
        (True, 'Poll'),
    )

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')
    is_poll = django_filters.ChoiceFilter(field_name='is_poll', choices=POLL_CHOICES, label=txt.POLL_FILTER_LABEL)

    class Meta:
        model = Quiz
        fields = ['name', 'author', 'is_poll']


class MyQuizFilter(QuizFilter):
    class Meta:
        model = Quiz
        fields = ['name', 'is_poll']
