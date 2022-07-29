from django import forms
from pollequiz.quiz.models import Quiz, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'name',
            'is_poll',
            'description',
        ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'q_number',
            'q_type',
            'text',
            'points',
        ]
