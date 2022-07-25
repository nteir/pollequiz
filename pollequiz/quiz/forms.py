from django import forms
from pollequiz.quiz.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'name',
            'is_poll',
            'description',
        ]
