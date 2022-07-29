from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name=_('Quiz name'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Created by'))
    is_poll = models.BooleanField(default=False, verbose_name=_('It\'s a poll (no points for questions)'))
    description = models.TextField(blank=True, verbose_name=_('Description (optional)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('Last modified'))


class Question(models.Model):

    TYPES = (
        ('sing', _('Single choice')),
        ('mult', _('Multiple choice')),
        ('open', _('Open ended')),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_('Quiz'))
    q_number = models.IntegerField()
    q_type = models.CharField(choices=TYPES, max_length=4)
    text = models.TextField()
