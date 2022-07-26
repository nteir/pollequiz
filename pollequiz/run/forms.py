from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from pollequiz.run.models import QuizTake


class TakeForm(forms.ModelForm):
    class Meta:
        model = QuizTake
        fields = [
            'taker_name',
        ]


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [(ans.id, ans.text) for ans in question.get_answers_list()]
        if question.q_type == 'sing':
            self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)
        elif question.q_type == 'mult':
            self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=CheckboxSelectMultiple)
