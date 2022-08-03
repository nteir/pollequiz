from django_filters.views import FilterView
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from pollequiz.run.forms import TakeForm, QuestionForm
from pollequiz.quiz.models import Quiz, Question
from pollequiz.quiz.filter import QuizFilter
from pollequiz.run.models import QuizTake
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
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
    success_url = reverse_lazy
    title = txt.TAKE_QUIZ_TITLE
    btn_text = txt.TAKE_QUIZ_BTN

    def get_success_url(self):
        quiz_id = self.object.quiz.id
        first_q_id = Question.objects.filter(quiz=quiz_id).order_by('q_number').first().id
        return reverse_lazy('run:quiz_take', kwargs={'quiz_id': quiz_id, 'pk': self.object.id, 'q_id': first_q_id})

    def get_initial(self):
        if self.request.user:
            uname = ' '.join((self.request.user.first_name, self.request.user.last_name))
            uname = uname.strip()
            if not uname:
                uname = self.request.user.username
        return {'taker_name': uname}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = Quiz.objects.get(id=self.kwargs['quiz_id']).name
        return context

    def form_valid(self, form):
        form.instance.quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        return super().form_valid(form)


class TakeQuestion(FormView):
    form_class = QuestionForm
    template_name = 'run/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        q_list = list(Question.objects.filter(quiz=quiz.id).order_by('q_number'))
        return context

    def get_form(self, form_class=QuestionForm):
        q_id = self.kwargs.get('q_id')
        if q_id:
            self.question = Question.objects.get(id=q_id)
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return dict(kwargs, question=self.question)
