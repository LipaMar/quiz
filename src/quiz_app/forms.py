from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CreateNewQuizForm(forms.Form):
    quiz_name = forms.CharField(max_length=30, label="Quiz Name")
    num_questions = forms.IntegerField(label="Number of Questions")

    def clean_name(self):
        data = self.cleaned_data['quiz_name']

        if data == "Default_Name":
            raise ValidationError(_('Invalid name! Quiz name must be unique.'))

        return data

    def clean_num_questions(self):
        data = self.cleaned_data['num_questions']

        if (isinstance(data, int) is False) or (data < 1):
            raise ValidationError(_('Invalid number of questions! Must be positive integer.)'))

        return data
