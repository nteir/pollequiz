from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name=_('Quiz name'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Created by'))
    is_poll = models.BooleanField(default=False, verbose_name=_('It\'s a poll (no points for questions)'))
    description = models.TextField(blank=True, verbose_name=_('Description (optional)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Last modified'))

    def get_questions_list(self):
        return list(Question.objects.filter(quiz=self.id).order_by('q_number'))


class Question(models.Model):

    TYPES = (
        ('sing', _('Single choice')),
        ('mult', _('Multiple choice')),
        # ('open', _('Open ended')),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_('Quiz'))
    q_number = models.IntegerField(verbose_name=_('Question number'))
    q_type = models.CharField(choices=TYPES, max_length=4)
    text = models.TextField()
    points = models.IntegerField(default=0, verbose_name=_('Points for correct answer'))
    ordering = ['q_number']

    def get_answers_list(self):
        return list(Answer.objects.filter(question=self.id).order_by('a_number'))


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Question'))
    a_number = models.IntegerField(verbose_name=_('Answer number'))
    text = models.TextField()
    correct = models.BooleanField(default=False, verbose_name=_('This answer is correct'))
    ordering = ['a_number']


@receiver(post_save, sender=Question)
def question_save_handler(instance, *args, **kwargs):
    quiz = instance.quiz
    quiz.modified_at = timezone.now()
    quiz.save()


@receiver(post_save, sender=Answer)
def answer_save_handler(instance, *args, **kwargs):
    quiz = instance.question.quiz
    quiz.modified_at = timezone.now()
    quiz.save()
