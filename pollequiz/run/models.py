from django.db import models
from django.utils.translation import gettext as _
from pollequiz.quiz.models import Quiz, Question, Answer


# Create your models here.
class QuizTake(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_('Quiz'))
    taker_name = models.CharField(max_length=250, blank=False, verbose_name=_('Taker name'))
    quiz_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Quiz date'))


class QuizTakeLog(models.Model):
    take_id = models.ForeignKey(QuizTake, on_delete=models.CASCADE)
    q_id = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    a_id = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
