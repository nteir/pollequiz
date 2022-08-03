from django_filters.views import FilterView
from django.views.generic.edit import CreateView
from pollequiz.run.forms import TakeForm
from pollequiz.quiz.models import Quiz
from pollequiz.quiz.filter import QuizFilter
from pollequiz.run.models import QuizTake
from django.contrib.auth import get_user_model
import pollequiz.pq_objects as pq_objects
import pollequiz.text_constants as txt

User = get_user_model()


class QuizListView(pq_objects.PQFormContextMixin, FilterView):
    model = Quiz
    filterset_class = QuizFilter
    template_name = 'run/quiz_list.html'
    ordering = ['-created_at']
    context_object_name = 'objects'
    btn_text = txt.FILTER_BTN


class TakeFirstPage(pq_objects.PQFormContextMixin, CreateView):
    model = QuizTake
    form_class = TakeForm
    template_name = 'quiz/quiz_form.html'
    title = txt.TAKE_QUIZ_TITLE
    btn_text = txt.TAKE_QUIZ_BTN

    def get_initial(self):
        if self.request.user:
            uname = ' '.join((self.request.user.first_name, self.request.user.last_name))
            if not uname:
                uname = self.request.user.username
        return {'taker_name': uname}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = Quiz.objects.get(id=self.kwargs['quiz_id']).name
        return context


class TakeQuestion():
    pass
