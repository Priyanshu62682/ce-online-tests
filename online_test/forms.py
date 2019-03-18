from django import forms
from .models import *
from django.forms import inlineformset_factory
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms.models import BaseModelFormSet   
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EditSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = []

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','password1', 'password2', )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student 
        fields=('birth_date', 'name', 'batch','Address' ) 


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class CreateSectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = ['exam','part','section_type', 'positive_marks','per_option_positive_marks','negative_marks','section_instructions']

    def __init__(self, exam, part, *args, **kwargs):
        self.exam = exam
        self.part = part
        super(CreateSectionForm, self).__init__(*args, **kwargs)

class QuestionForm(ModelForm):
    class Meta:
        model = SingleChoiceCorrect
        exclude = ()



QuestionFormset = modelformset_factory(Question, fields=['serial','content','figure'], extra=2, form = QuestionForm)



# class QuestionAddForm(forms.ModelForm):

#     class Meta:
#         model = Question
#         fields = ('serial','content', 'figure')
#         extra=2




# QuestionAddFormset=modelformset_factory(Question, fields=['serial','content','figure'], extra=2, form=QuestionAddForm)

# class ChoiceAddForm(forms.ModelForm):

#     class Meta:
#         model = QuestionChoices
#         fields = ('choices',)
#         extra=2

# ChoiceAddFormset=modelformset_factory(QuestionChoices, fields=['choices',], extra=2, form=ChoiceAddForm)

class QuestionAddForm(forms.ModelForm):
    class Meta:
        model = QuestionChoices
        exclude = ('choices','question_id','section','correct_choice')

    extra_field_count = forms.CharField(widget=forms.HiddenInput())
     

    def __init__(self, *args, **kwargs):
        extra_fields =kwargs.pop('extra', 0)


        super(QuestionAddForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        
        
        print(extra_fields)    
        if extra_fields == 4:
            print('entered')
            SOME_CHOICES = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4','4')
                          )
            self.fields['correct_choice']=forms.MultipleChoiceField(choices=SOME_CHOICES, widget=forms.CheckboxSelectMultiple())
            print('exit')

        else:
            if extra_fields == 5:
                SOME_CHOICES = (
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4','4'),
                ('5','5')  
                                )

                self.fields['correct_choice']=forms.MultipleChoiceField(choices=SOME_CHOICES, widget=forms.CheckboxSelectMultiple())

            else:
                if extra_fields == 0:
                    self.fields['correct_choice']=forms.CharField()

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['choice_{index}'.format(index=index+1)] = \
                forms.CharField()


     




    
    



 



QuestionAddFormset = inlineformset_factory(Question, QuestionChoices, fields = ['question_id', 'section', 'choices'], exclude = [], extra=1,can_delete = False)






