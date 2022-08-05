from django_filters.views import FilterView
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from pollequiz.run.forms import TakeForm, QuestionForm
from pollequiz.quiz.models import Quiz, Question, Answer
from pollequiz.quiz.filter import QuizFilter
from pollequiz.run.models import QuizTake, QuizTakeLog
from django.http import HttpResponseRedirect
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
        first_q_id = Question.objects.filter(quiz=quiz_id).order_by('q_number', 'id').first().id
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

    def get_form(self, form_class=QuestionForm):
        q_id = self.kwargs.get('q_id')
        if q_id:
            self.question = Question.objects.get(id=q_id)
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs['q_id'])
        context['question'] = question
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return dict(kwargs, question=self.question)

    def get_success_url(self):
        quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        q_list = list(Question.objects.values('id').filter(quiz=quiz.id).order_by('q_number', 'id'))
        q_list = [q['id'] for q in q_list]
        curr_id = self.kwargs.get('q_id')
        curr_index = q_list.index(curr_id)
        if curr_index + 1 >= len(q_list):
            url = reverse_lazy('home')
        else:
            next = q_list[curr_index + 1]
            url = reverse_lazy('run:quiz_take', kwargs={'quiz_id': quiz.id, 'pk': self.kwargs['pk'], 'q_id': next})
        return url

    def form_valid(self, form):
        log_entry = QuizTakeLog()
        log_entry.take_id = QuizTake.objects.get(id=self.kwargs.get('pk'))
        log_entry.q_id = self.question
        log_entry.a_id = Answer.objects.get(id=form.data.get('answers'))
        log_entry.save()
        return HttpResponseRedirect(self.get_success_url())
