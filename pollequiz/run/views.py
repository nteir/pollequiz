# from django.views.generic.list import ListView
from django_filters.views import FilterView
from pollequiz.quiz.models import Quiz
from pollequiz.quiz.filter import QuizFilter
import pollequiz.pq_objects as pq_objects
import pollequiz.text_constants as txt


class QuizListView(pq_objects.PQFormContextMixin, FilterView):
    model = Quiz
    filterset_class = QuizFilter
    template_name = 'run/quiz_list.html'
    ordering = ['-created_at']
    context_object_name = 'objects'
    btn_text = txt.FILTER_BTN
