from django.db import models
from datetime import datetime  
from model_utils import Choices
from model_utils.fields import StatusField
from online_test.models import *

# Create your models here.

class Subscriptions(models.Model):
	student = models.ForeignKey(
		Student,
		on_delete=models.CASCADE,
		)
	exam = models.ForeignKey(
		Exam,
		on_delete=models.CASCADE,
		)
	
	event_status = Choices('Upcoming','Running','Halted','History')
	
	event = StatusField(choices_name='event_status')
	
	registered_on = models.DateTimeField(
		default = datetime.now,
		blank = True,
		)
	def __str__(self):
		return str(self.student.name)
