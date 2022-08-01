from django import forms
from pollequiz.quiz.models import Quiz, Question, Answer


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


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'a_number',
            'text',
            'correct',
        ]
