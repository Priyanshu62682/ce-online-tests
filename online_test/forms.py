from django import forms
from .models import *
from django.forms import inlineformset_factory
from django.forms import ModelForm
from django.forms import modelformset_factory


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class CreateSectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = ['exam','part','section_type','positive_marks','negative_marks','section_instructions']

    def __init__(self, exam, part, *args, **kwargs):
        self.exam = exam
        self.part = part
        super(CreateSectionForm, self).__init__(*args, **kwargs)

class QuestionForm(ModelForm):
    class Meta:
        model = SingleChoiceCorrect
        exclude = ()



QuestionFormset = modelformset_factory(Question, fields=['content','figure'], extra=2, form = QuestionForm)
#QuestionInlineFormSet = inlineformset_factory(Question,SingleChoiceCorrect,extra=1,form = QuestionForm)

