from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(QuestionChoices)
admin.site.register(Dynamic)
admin.site.register(Exam)
admin.site.register(Part)
admin.site.register(Question)
admin.site.register(Section)
admin.site.register(SingleChoiceCorrect)
admin.site.register(Student)
admin.site.register(Result)