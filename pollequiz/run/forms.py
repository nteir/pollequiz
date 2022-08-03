from django import forms
from pollequiz.run.models import QuizTake


class TakeForm(forms.ModelForm):
    class Meta:
        model = QuizTake
        fields = [
            'taker_name',
        ]
